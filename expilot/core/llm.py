import os
import json
import re
import time
import random
import functools
import threading
from collections import deque
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APITimeoutError, APIConnectionError, APIStatusError
from expilot.core.schema import AgentAction

load_dotenv()

MAX_RETRIES = 3
RETRY_BASE_DELAY = 5  # seconds


# ── Request Counter & Local Rate Limiter ──

class RequestCounter:
    """线程安全的请求计数器 + 本地限流。"""

    def __init__(self):
        self._lock = threading.Lock()
        self._window: deque = deque()  # 存放每次请求的时间戳
        self._rpm_limit = int(os.getenv("RPM_LIMIT", "60"))  # 每分钟最大请求数
        self._total = 0
        self._errors = 0
        self._rate_limit_hits = 0

    def _clean_window(self, now: float):
        """滑动窗口：移除 60 秒前的记录。"""
        while self._window and now - self._window[0] > 60:
            self._window.popleft()

    def acquire(self) -> float:
        """尝试获取一个请求配额。返回需要等待的秒数（0 表示无需等待）。"""
        with self._lock:
            now = time.monotonic()
            self._clean_window(now)

            if len(self._window) >= self._rpm_limit:
                # 超过限流，计算需要等待的时间
                wait = 60 - (now - self._window[0]) + 0.5
                return max(wait, 0.5)

            self._window.append(now)
            self._total += 1
            return 0

    def record_error(self, is_rate_limit: bool = False):
        with self._lock:
            self._errors += 1
            if is_rate_limit:
                self._rate_limit_hits += 1

    def stats(self) -> dict:
        with self._lock:
            now = time.monotonic()
            self._clean_window(now)
            return {
                "current_rpm": len(self._window),
                "rpm_limit": self._rpm_limit,
                "total_requests": self._total,
                "total_errors": self._errors,
                "rate_limit_hits": self._rate_limit_hits,
                "quota_remaining": max(0, self._rpm_limit - len(self._window)),
            }

    def quota_alert(self) -> Optional[str]:
        """配额监控：当剩余配额不足时返回告警信息。"""
        stats = self.stats()
        remaining = stats["quota_remaining"]
        if remaining <= 0:
            return "⚠️ API 请求配额已耗尽，请稍后再试。"
        if remaining <= 5:
            return f"⚠️ API 请求配额紧张，剩余 {remaining}/{stats['rpm_limit']} RPM。"
        if stats["rate_limit_hits"] > 3:
            return f"⚠️ 已触发 {stats['rate_limit_hits']} 次限流，建议降低请求频率。"
        return None


# 全局单例
_request_counter = RequestCounter()


# ── Retry Decorator ──

def retry_on_failure(max_retries: int = MAX_RETRIES, base_delay: float = RETRY_BASE_DELAY):
    """重试装饰器：指数退避 + 随机抖动，区分限流和普通错误。"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (RateLimitError, APITimeoutError, APIConnectionError) as e:
                    last_error = e
                    _request_counter.record_error(is_rate_limit=isinstance(e, RateLimitError))
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                        time.sleep(delay)
                        continue
                except APIStatusError as e:
                    if e.status_code == 403:
                        # 403 RPM 限流：友好提示，不崩溃
                        _request_counter.record_error(is_rate_limit=True)
                        return "⚠️ 请求被拒绝（403 RPM 限流）。API 提供商当前限制了请求频率，请稍后重试。"
                    if e.status_code >= 500:
                        last_error = e
                        _request_counter.record_error()
                        if attempt < max_retries - 1:
                            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                            time.sleep(delay)
                            continue
                    raise
            raise last_error
        return wrapper
    return decorator


# ── LLM Client ──

class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        )
        self.model = os.getenv("MODEL_NAME") or os.getenv("EXPILOT_MODEL", "gpt-4o-mini")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "800"))

    @retry_on_failure()
    def _call_api(self, messages: list) -> str:
        """统一的 API 调用入口，所有重试逻辑由装饰器处理。"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,
            max_tokens=self.max_tokens,
        )
        if not response.choices:
            raise ValueError("API returned empty choices")
        content = response.choices[0].message.content
        if content is None:
            raise ValueError("API returned None content")
        return content

    @staticmethod
    def _extract_answer(raw: str) -> str:
        """从模型响应中提取实际回答内容。

        支持格式：
        <think>...</think><answer>...</answer>
        <think>...</think>普通文本/JSON
        纯文本/JSON
        """
        # 优先从 <answer> 标签提取
        match = re.search(r"<answer>(.*?)</answer>", raw, re.DOTALL)
        if match:
            content = match.group(1).strip()
            content = re.sub(r"^```(?:json)?\s*", "", content)
            content = re.sub(r"\s*```$", "", content)
            return content

        # 剥离 <think>...</think> 块，取其后的内容
        cleaned = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
        if cleaned:
            return cleaned

        # 兜底：返回原始内容（剥离 <think> 块后为空的情况）
        return raw.strip()

    @staticmethod
    def _repair_json(raw: str) -> str:
        """尝试修复模型输出的常见 JSON 格式问题。"""
        s = raw.strip()
        # 修复缺失引号的键：{ key": "value"} → { "key": "value"}
        s = re.sub(r'(?<=[{,])\s*([a-zA-Z_]\w*)(?=\s*[":])', r' "\1"', s)
        # 去除尾部逗号
        s = re.sub(r',\s*([}\]])', r'\1', s)
        return s

    def decide(self, system_prompt: str, user_prompt: str, history: list = None):
        """主入口：构建消息、限流、调用 API、解析结果。返回 AgentAction 或错误提示字符串。"""
        # 配额监控
        alert = _request_counter.quota_alert()
        if alert:
            return alert

        # 本地限流：如果需要等待，先 sleep
        wait = _request_counter.acquire()
        if wait > 0:
            time.sleep(wait)

        # 构建消息
        messages = [{"role": "system", "content": system_prompt}]
        if history:
            for msg in history[-6:]:
                if isinstance(msg, dict) and "role" in msg and "content" in msg:
                    messages.append(msg)
        messages.append({"role": "user", "content": user_prompt})

        # 调用 API
        raw = self._call_api(messages)

        # 403 友好提示直接返回字符串
        if isinstance(raw, str) and raw.startswith("⚠️"):
            return raw

        # 提取 <answer> 标签内容（支持思维链模型）
        content = self._extract_answer(raw)
        try:
            return AgentAction.model_validate(json.loads(content))
        except (json.JSONDecodeError, ValueError):
            # 尝试修复常见 JSON 格式问题后再解析
            try:
                repaired = self._repair_json(content)
                return AgentAction.model_validate(json.loads(repaired))
            except (json.JSONDecodeError, ValueError):
                # 模型未输出 JSON，返回纯文本回答
                return content

    @staticmethod
    def get_stats() -> dict:
        return _request_counter.stats()
