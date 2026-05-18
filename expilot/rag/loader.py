from pathlib import Path
from pypdf import PdfReader
import docx
import pandas as pd


def load_document(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    suffix = p.suffix.lower()
    if suffix in {".txt", ".md"}:
        return p.read_text(encoding="utf-8", errors="ignore")
    if suffix == ".pdf":
        return "\n".join([pg.extract_text() for pg in PdfReader(str(p)).pages if pg.extract_text()])
    if suffix == ".docx":
        paragraphs = docx.Document(str(p)).paragraphs
        return "\n".join([para.text for para in paragraphs])
    if suffix == ".csv":
        return pd.read_csv(str(p)).to_markdown(index=False)
    if suffix == ".xlsx":
        return pd.read_excel(str(p)).to_markdown(index=False)
    raise ValueError(f"Unsupported file type: {suffix}")
