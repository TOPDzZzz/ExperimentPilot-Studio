import time
import json
from pathlib import Path

TRACE_PATH = Path("expilot/storage/traces.json")
TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)

def log_trace(step_type: str, name: str, input_data: dict, output_data: str):
    trace = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "step_type": step_type,
        "name": name,
        "input": input_data,
        "output_preview": output_data[:500]
    }

    if TRACE_PATH.exists():
        traces = json.loads(TRACE_PATH.read_text(encoding="utf-8"))
    else:
        traces = []

    traces.append(trace)
    TRACE_PATH.write_text(json.dumps(traces, ensure_ascii=False, indent=2), encoding="utf-8")

def load_traces():
    if not TRACE_PATH.exists():
        return []
    return json.loads(TRACE_PATH.read_text(encoding="utf-8"))