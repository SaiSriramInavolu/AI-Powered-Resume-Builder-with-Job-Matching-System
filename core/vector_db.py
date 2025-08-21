import chromadb
from sentence_transformers import SentenceTransformer

class VectorDB:
    def __init__(self, path="./chroma_db"):
        self.client = chromadb.PersistentClient(path=path)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection = self.client.get_or_create_collection(name="resume_jd_collection")

    def add_document(self, document_id: str, text: str, metadata: dict = None):
        embedding = self.model.encode(text).tolist()
        self.collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata if metadata else {}],
            ids=[document_id]
        )

    def query_documents(self, query_text: str, n_results: int = 5):
        query_embedding = self.model.encode(query_text).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results

    def get_document(self, document_id: str):
        return self.collection.get(ids=[document_id])

    def delete_document(self, document_id: str):
        self.collection.delete(ids=[document_id])

    def count_documents(self):
        return self.collection.count()
