import chromadb

class ChromaStore:
    def __init__(self, persist_dir: str = "expilot/storage/chroma"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name="agenthub_knowledge")

    def add_documents(self, chunks: list, source: str):
        self.collection.add(documents=chunks, ids=[f"{source}_{i}" for i in range(len(chunks))], metadatas=[{"source": source, "chunk_id": i} for i in range(len(chunks))])

    def search(self, query: str, top_k: int = 5):
        return self.collection.query(query_texts=[query], n_results=top_k)