def split_text(text: str, chunk_size: int = 800, overlap: int = 150) -> list:
    chunks, start = [], 0
    while start < len(text):
        chunk = text[start:start + chunk_size]
        if chunk.strip(): chunks.append(chunk)
        start += chunk_size - overlap
    return chunks