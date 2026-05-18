import streamlit as st
from expilot.core.trace import load_traces
from expilot.i18n import t

lang = st.session_state.get("lang", "zh")

st.title(f"🧭 {t('trace_title', lang)}")
traces = load_traces()
if not traces:
    st.info(t("trace_empty", lang))
else:
    for tr in traces[::-1]:
        with st.expander(f"{tr['step_type']} | {tr['name']} | {tr['timestamp']}"):
            st.json(tr["input"])
            st.text(t("trace_output", lang))
            st.code(tr["output_preview"], language="text")
