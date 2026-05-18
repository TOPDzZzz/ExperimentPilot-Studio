import streamlit as st
import json
from pathlib import Path
from dotenv import load_dotenv
from expilot.core.agent import AgentEngine
from expilot.i18n import t

load_dotenv()

st.set_page_config(
    page_title="ExperimentPilot Studio",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Refined Modern Theme ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400&display=swap');

:root {
    --bg-primary: #fafaf8;
    --bg-secondary: #ffffff;
    --bg-sidebar: #f7f6f3;
    --accent: #6366f1;
    --accent-light: #818cf8;
    --accent-glow: rgba(99, 102, 241, 0.12);
    --accent-subtle: rgba(99, 102, 241, 0.06);
    --text-primary: #1a1a2e;
    --text-secondary: #64648c;
    --text-muted: #9898b0;
    --border: #e8e8f0;
    --border-focus: #6366f1;
    --success: #10b981;
    --warning: #f59e0b;
    --error: #ef4444;
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.05), 0 2px 4px rgba(0,0,0,0.04);
    --shadow-lg: 0 8px 24px rgba(0,0,0,0.08);
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    --font-mono: 'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;
}

/* ── Global ── */
.stApp {
    background-color: var(--bg-primary) !important;
    font-family: var(--font-sans);
}

.main .block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 860px !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--bg-sidebar) 0%, var(--bg-secondary) 100%) !important;
    border-right: 1px solid var(--border) !important;
}

section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: var(--font-sans) !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

/* ── Typography ── */
h1 {
    font-family: var(--font-sans) !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em;
    font-size: 1.75rem !important;
}

h2, h3 {
    font-family: var(--font-sans) !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em;
}

p, span, div, label {
    font-family: var(--font-sans);
    color: var(--text-secondary);
    line-height: 1.6;
}

code, pre {
    font-family: var(--font-mono) !important;
}

/* ── Chat Messages ── */
.stChatMessage {
    background-color: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1rem 1.25rem !important;
    margin-bottom: 0.75rem !important;
    box-shadow: var(--shadow-sm) !important;
    transition: box-shadow 0.2s ease, border-color 0.2s ease !important;
}

.stChatMessage:hover {
    box-shadow: var(--shadow-md) !important;
}

/* User message — subtle left accent */
.stChatMessage[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    border-left: 3px solid var(--accent) !important;
    background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--accent-subtle) 100%) !important;
}

/* Assistant message — clean border */
.stChatMessage[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    border-left: 3px solid var(--border) !important;
}

/* ── Avatars ── */
[data-testid="chatAvatarIcon-user"],
[data-testid="chatAvatarIcon-assistant"] {
    border-radius: 50% !important;
    width: 36px !important;
    height: 36px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 1.1rem !important;
    flex-shrink: 0 !important;
}

[data-testid="chatAvatarIcon-user"] {
    background: linear-gradient(135deg, var(--accent), var(--accent-light)) !important;
    color: white !important;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.25) !important;
}

[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, #e0e7ff, #c7d2fe) !important;
    color: var(--accent) !important;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.12) !important;
}

/* ── Buttons ── */
.stButton > button {
    background-color: var(--bg-secondary) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--font-sans) !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: var(--shadow-sm) !important;
}

.stButton > button:hover {
    background-color: var(--accent-subtle) !important;
    color: var(--accent) !important;
    border-color: var(--accent) !important;
    box-shadow: var(--shadow-md) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

.stButton > button[kind="primary"],
.stFormSubmitButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent-light)) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3) !important;
}

.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button:hover {
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.4) !important;
    transform: translateY(-1px) !important;
}

/* ── Input Fields ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    border-color: var(--border) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--font-sans) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}

/* ── Chat Input ── */
.stChatInput {
    border-radius: var(--radius-lg) !important;
}

/* ── Status Widget ── */
.stStatus {
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    font-family: var(--font-sans) !important;
    font-weight: 500 !important;
    color: var(--text-primary) !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1rem 0 !important;
}

/* ── Caption / Metrics ── */
.stCaption, .stMetric {
    font-family: var(--font-sans) !important;
    color: var(--text-muted) !important;
}

/* ── Alert Boxes ── */
.stAlert {
    border-radius: var(--radius-sm) !important;
    font-family: var(--font-sans) !important;
    border: 1px solid var(--border) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0 !important;
    background: var(--bg-primary) !important;
    border-radius: var(--radius-sm) !important;
    padding: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    font-family: var(--font-sans) !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    border-radius: 6px !important;
    transition: all 0.2s ease !important;
}

.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    background: var(--bg-secondary) !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--text-muted);
}

/* ── Sidebar Buttons ── */
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--accent-subtle) !important;
    border-color: var(--accent) !important;
}

/* ── Selectbox / Slider ── */
.stSelectbox > div > div,
.stSlider > div > div {
    font-family: var(--font-sans) !important;
}

/* ── Success / Warning / Error badges ── */
.stSuccess {
    border-left: 3px solid var(--success) !important;
}
.stWarning {
    border-left: 3px solid var(--warning) !important;
}
.stError {
    border-left: 3px solid var(--error) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session State Init ──
HISTORY_DIR = Path("expilot/storage/conversations")
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

if "lang" not in st.session_state:
    st.session_state.lang = "zh"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "profile" not in st.session_state:
    st.session_state.profile = "general"
if "max_steps" not in st.session_state:
    st.session_state.max_steps = 8
if "conv_id" not in st.session_state:
    st.session_state.conv_id = None
if "conversations" not in st.session_state:
    # Load conversation index
    idx_path = HISTORY_DIR / "_index.json"
    if idx_path.exists():
        st.session_state.conversations = json.loads(idx_path.read_text(encoding="utf-8"))
    else:
        st.session_state.conversations = []


lang = st.session_state.lang


def save_conversation():
    """Save current conversation to disk."""
    if not st.session_state.messages:
        return
    conv_id = st.session_state.conv_id
    if not conv_id:
        import uuid
        conv_id = f"conv_{uuid.uuid4().hex[:12]}"
        st.session_state.conv_id = conv_id

    conv_path = HISTORY_DIR / f"{conv_id}.json"
    title = st.session_state.messages[0]["content"][:50] if st.session_state.messages else "Empty"
    data = {
        "id": conv_id,
        "title": title,
        "messages": st.session_state.messages,
        "profile": st.session_state.profile,
    }
    conv_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # Update index
    idx = [c for c in st.session_state.conversations if c["id"] != conv_id]
    idx.insert(0, {"id": conv_id, "title": title, "profile": st.session_state.profile})
    idx = idx[:50]  # keep last 50
    st.session_state.conversations = idx
    (HISTORY_DIR / "_index.json").write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")


def load_conversation(conv_id: str):
    """Load a conversation from disk."""
    conv_path = HISTORY_DIR / f"{conv_id}.json"
    if conv_path.exists():
        data = json.loads(conv_path.read_text(encoding="utf-8"))
        st.session_state.messages = data.get("messages", [])
        st.session_state.profile = data.get("profile", "general")
        st.session_state.conv_id = conv_id


def new_chat():
    """Start a new conversation."""
    save_conversation()
    st.session_state.messages = []
    st.session_state.conv_id = None


def delete_conversation(conv_id: str):
    """Delete a conversation from disk."""
    conv_path = HISTORY_DIR / f"{conv_id}.json"
    if conv_path.exists():
        conv_path.unlink()
    st.session_state.conversations = [c for c in st.session_state.conversations if c["id"] != conv_id]
    idx_path = HISTORY_DIR / "_index.json"
    idx_path.write_text(json.dumps(st.session_state.conversations, ensure_ascii=False, indent=2), encoding="utf-8")
    if st.session_state.conv_id == conv_id:
        st.session_state.messages = []
        st.session_state.conv_id = None


# ── Sidebar ──
with st.sidebar:
    # Language toggle
    col_en, col_zh = st.columns(2)
    with col_en:
        if st.button("English", key="lang_en", use_container_width=True,
                      type="primary" if lang == "en" else "secondary"):
            st.session_state.lang = "en"
            st.rerun()
    with col_zh:
        if st.button("简体中文", key="lang_zh", use_container_width=True,
                      type="primary" if lang == "zh" else "secondary"):
            st.session_state.lang = "zh"
            st.rerun()

    st.divider()
    st.markdown(f"### {t('sidebar_control', lang)}")

    # Agent mode
    mode_map = {
        "general": t("mode_general", lang),
        "file": t("mode_file", lang),
        "code": t("mode_code", lang),
        "data": t("mode_data", lang),
        "ml": t("mode_ml", lang),
        "research": t("mode_research", lang),
    }
    st.session_state.profile = st.selectbox(
        t("agent_mode", lang),
        list(mode_map.keys()),
        format_func=lambda x: mode_map[x],
    )

    # Max steps
    st.session_state.max_steps = st.slider(t("max_steps", lang), 3, 30, st.session_state.max_steps)
    st.info(t("sandbox_info", lang))

    st.divider()

    # Tool trace toggle
    if st.checkbox(t("show_trace", lang)):
        from expilot.core.trace import load_traces
        traces = load_traces()[-3:]
        for tr in traces[::-1]:
            with st.expander(f"{tr['name']} @ {tr['timestamp']}"):
                st.json(tr["input"])
                st.code(tr["output_preview"][:300], language="text")

    st.divider()

    # ── Conversation History ──
    st.markdown(f"### {t('history', lang)}")

    if st.button(f"+ {t('new_chat', lang)}", use_container_width=True):
        new_chat()
        st.rerun()

    for conv in st.session_state.conversations[:20]:
        col1, col2 = st.columns([5, 1])
        with col1:
            if st.button(conv["title"], key=f"h_{conv['id']}", use_container_width=True):
                load_conversation(conv["id"])
                st.rerun()
        with col2:
            if st.button("x", key=f"d_{conv['id']}", help=t("delete_chat", lang)):
                delete_conversation(conv["id"])
                st.rerun()


# ── Main Content ──
st.markdown(f"# {t('app_title', lang)}")
st.caption(t("app_subtitle", lang))


# Display messages
AVATAR_MAP = {"user": "👤", "assistant": "🧪"}
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=AVATAR_MAP.get(msg["role"], "💬")):
        st.markdown(msg["content"])


# Chat input
if user_input := st.chat_input(t("chat_input", lang)):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🧪"):
        agent = AgentEngine(max_steps=st.session_state.max_steps, profile=st.session_state.profile)
        history = [m for m in st.session_state.messages if m["role"] == "assistant"]

        status = st.status(t("agent_thinking", lang), expanded=True)
        final_box = st.empty()
        step_count = 0

        for step_info in agent.run_stream(user_input, history):
            step_count += 1

            if step_info["type"] == "thought":
                status.update(label=f"Step {step_count}: {step_info['content'][:80]}")

            elif step_info["type"] == "tool_call":
                tool_name = step_info.get("tool_name", "")
                status.update(label=f"Step {step_count}: Using {tool_name}...")

            elif step_info["type"] == "observation":
                pass  # observation is internal, skip in UI

            elif step_info["type"] == "final":
                status.update(label=t("completed", lang), state="complete")
                final_box.markdown(step_info["content"])
                st.session_state.messages.append({"role": "assistant", "content": step_info["content"]})
                break

            elif step_info["type"] == "error":
                status.update(label=t("status_error", lang), state="error")
                final_box.error(step_info["content"])
                st.session_state.messages.append({"role": "assistant", "content": step_info["content"]})
                break

        st.caption(f"{t('steps', lang)}: {step_count}")

    save_conversation()
