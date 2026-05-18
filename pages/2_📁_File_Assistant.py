import streamlit as st
from pathlib import Path
from expilot.core.agent import AgentEngine
from expilot.i18n import t

lang = st.session_state.get("lang", "zh")

st.title(f"📁 {t('file_title', lang)}")

uploaded = st.file_uploader(t("file_upload", lang), type=["txt", "md", "pdf", "docx", "csv", "xlsx"])
if uploaded:
    Path("uploads").mkdir(exist_ok=True)
    save_path = Path("uploads") / uploaded.name
    save_path.write_bytes(uploaded.getbuffer())
    st.success(f"{t('file_saved', lang)}: {save_path}")

    # Show preview for text files
    if uploaded.name.endswith((".txt", ".md")):
        text = save_path.read_text(encoding="utf-8", errors="ignore")
        st.text_area("文件预览", text, height=300, disabled=True)

task = st.text_area(t("file_task", lang), t("file_task_default", lang))
if st.button(t("file_execute", lang)):
    if not uploaded:
        st.warning(t("file_upload_first", lang) if "file_upload_first" in dir() else "Please upload a file first.")
    else:
        with st.spinner(t("file_processing", lang)):
            agent = AgentEngine(profile="file")
            file_path = f"uploads/{uploaded.name}"
            res = agent.run(f"{task}\nFile path: {file_path}")
            st.markdown(res["answer"])
