from expilot.rag.vector_store import ChromaStore

class Retriever:
    def __init__(self): self.store = ChromaStore()
    def retrieve(self, query: str, top_k: int = 5) -> str:
        results = self.store.search(query, top_k=top_k)
        docs, metas = results.get("documents", [[]])[0], results.get("metadatas", [[]])[0]
        return "\n\n---\n\n".join([f"来源：{m.get('source')}\n内容：{d}" for d, m in zip(docs, metas)])