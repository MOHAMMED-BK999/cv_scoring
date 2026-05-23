VECTOR_SIZE = 768


class EmbeddingService:
    """Create 768-dimensional vectors from text."""
    
    def __init__(self):
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer("BAAI/bge-base-en-v1.5")
        except Exception as exc:
            self.model = None
            print(f"WARNING: embeddings model is not available: {exc}")

    def get_embedding(self, text: str) -> list[float]:
        if not text:
            return [0.0] * VECTOR_SIZE
            
        if self.model:
            vector = self.model.encode(text, normalize_embeddings=True)
            return vector.tolist()
            
        return [0.0] * VECTOR_SIZE


embedding_service = EmbeddingService()

def get_embedding(text: str) -> list[float]:
    return embedding_service.get_embedding(text)
