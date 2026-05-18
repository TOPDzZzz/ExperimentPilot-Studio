import streamlit as st
import pandas as pd
from pathlib import Path
from expilot.core.agent import AgentEngine
from expilot.i18n import t

lang = st.session_state.get("lang", "zh")

st.title(f"📊 {t('data_title', lang)}")
uploaded = st.file_uploader(t("data_upload", lang), type=["csv", "xlsx"])
if uploaded:
    Path("uploads").mkdir(exist_ok=True)
    save_path = Path("uploads") / uploaded.name
    save_path.write_bytes(uploaded.getbuffer())
    df = pd.read_csv(save_path) if save_path.suffix == ".csv" else pd.read_excel(save_path)
    st.dataframe(df.head())
    task = st.text_input(t("data_task", lang), t("data_task_default", lang))
    if st.button(t("data_execute", lang)):
        with st.spinner(t("data_analyzing", lang)):
            res = AgentEngine(profile="data").run(f"{task}\nData file: {save_path}")
            st.markdown(res["answer"])
