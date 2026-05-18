import streamlit as st
import os
from pathlib import Path
from expilot.i18n import t

lang = st.session_state.get("lang", "zh")

st.title(f"⚙️ {t('settings_title', lang)}")

# ── API Configuration ──
st.markdown(f"### {t('settings_api_section', lang)}")

api_key = st.text_input(
    t("settings_api_key", lang),
    os.getenv("OPENAI_API_KEY", ""),
    type="password",
    help="sk-...",
)
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

base_url = st.text_input(
    t("settings_base_url", lang),
    os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    help="https://api.openai.com/v1",
)
os.environ["OPENAI_BASE_URL"] = base_url

model_name = st.text_input(
    t("settings_model_name", lang),
    os.getenv("MODEL_NAME") or os.getenv("EXPILOT_MODEL", "gpt-4o-mini"),
    help="gpt-4o-mini / gpt-4o / Pro/zai-org/GLM-4.7 / ...",
)
os.environ["MODEL_NAME"] = model_name

col1, col2 = st.columns(2)
with col1:
    max_tokens = st.number_input(
        t("settings_max_tokens", lang),
        min_value=100,
        max_value=16000,
        value=int(os.getenv("MAX_TOKENS", "800")),
        step=100,
    )
    os.environ["MAX_TOKENS"] = str(max_tokens)

with col2:
    rpm_limit = st.slider(
        t("settings_rpm_limit", lang),
        min_value=1,
        max_value=120,
        value=int(os.getenv("RPM_LIMIT", "60")),
    )
    os.environ["RPM_LIMIT"] = str(rpm_limit)

# ── Safety ──
st.divider()
allow_shell = st.toggle(
    t("settings_shell", lang),
    value=os.getenv("ALLOW_SHELL", "false").lower() == "true",
    help=t("settings_shell_help", lang),
)
os.environ["ALLOW_SHELL"] = "true" if allow_shell else "false"

# ── Clear Data ──
st.divider()
if st.button(t("settings_clear", lang)):
    Path("expilot/storage/memory.json").unlink(missing_ok=True)
    Path("expilot/storage/traces.json").unlink(missing_ok=True)
    st.success(t("settings_cleared", lang))

# ── Status ──
st.divider()
with st.expander(f"🔍 {t('status', lang)}"):
    st.code(
        f"API Key:  {'***' + api_key[-4:] if len(api_key) > 4 else '(not set)'}\n"
        f"Base URL: {base_url}\n"
        f"Model:    {model_name}\n"
        f"Tokens:   {max_tokens}\n"
        f"RPM:      {rpm_limit}\n"
        f"Shell:    {'ON' if allow_shell else 'OFF'}",
        language="text",
    )
