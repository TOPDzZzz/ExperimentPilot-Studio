import streamlit as st
from expilot.core.agent import AgentEngine
from expilot.i18n import t

lang = st.session_state.get("lang", "zh")

st.title(f"💻 {t('code_title', lang)}")
st.info(t("code_info", lang))
task = st.text_input(t("code_task", lang), t("code_task_default", lang))
if st.button(t("code_analyze", lang)):
    with st.spinner(t("code_scanning", lang)):
        res = AgentEngine(profile="code").run(task)
        st.markdown(res["answer"])
