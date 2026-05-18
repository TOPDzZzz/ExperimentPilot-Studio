import streamlit as st
from pathlib import Path
from expilot.rag.loader import load_document
from expilot.rag.splitter import split_text
from expilot.rag.vector_store import ChromaStore
from expilot.rag.retriever import Retriever
from expilot.i18n import t

lang = st.session_state.get("lang", "zh")

st.title(f"📚 {t('kb_title', lang)}")
uploaded = st.file_uploader(t("kb_upload", lang), type=["txt", "md", "pdf", "docx", "csv", "xlsx"])
if uploaded:
    Path("uploads").mkdir(exist_ok=True)
    path = Path("uploads") / uploaded.name
    path.write_bytes(uploaded.getbuffer())
    if st.button(t("kb_add", lang)):
        text = load_document(str(path))
        chunks = split_text(text)
        ChromaStore().add_documents(chunks, source=uploaded.name)
        st.success(f"{t('kb_added', lang)} {len(chunks)} {t('kb_chunks', lang)}")

query = st.text_input(t("kb_query", lang))
if query and st.button(t("kb_search", lang)):
    context = Retriever().retrieve(query)
    with st.expander(t("kb_results", lang)):
        st.markdown(context)
