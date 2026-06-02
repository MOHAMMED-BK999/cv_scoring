import json
import os

DEFAULT_SBERT_MODEL = "BAAI/bge-m3"
VECTOR_SIZE = 1024


class EmbeddingService:
    """Create dense vectors from CV JSON and job text using SBERT."""

    def __init__(self):
        self.model = None
        self.model_name = os.getenv("SBERT_MODEL", DEFAULT_SBERT_MODEL)
        self.vector_size = VECTOR_SIZE
        try:
            from sentence_transformers import SentenceTransformer

            self.model = SentenceTransformer(self.model_name)
            self.vector_size = int(self.model.get_sentence_embedding_dimension() or VECTOR_SIZE)
        except Exception as exc:
            print(f"WARNING: SBERT model is not available: {exc}")

    def get_embedding_from_profile(self, profile) -> list[float]:
        """Create a dense vector from the extracted CV profile JSON."""
        if hasattr(profile, "model_dump"):
            profile_json = profile.model_dump()
        elif hasattr(profile, "dict"):
            profile_json = profile.dict()
        elif isinstance(profile, dict):
            profile_json = profile
        else:
            profile_json = profile

        if isinstance(profile_json, dict):
            profile_json.pop("raw_text", None)

        return self.get_embedding_from_json(profile_json)

    def get_embedding_from_json(self, profile_json: dict) -> list[float]:
        """Create a dense vector from the extracted JSON profile."""
        json_str = json.dumps(profile_json, ensure_ascii=False)
        return self._encode(json_str)

    def get_embedding(self, text: str) -> list[float]:
        """Create a dense vector from plain text (used for job descriptions)."""
        return self._encode(text)

    def _encode(self, text: str) -> list[float]:
        if not text:
            return [0.0] * self.vector_size

        if self.model:
            vector = self.model.encode(text, normalize_embeddings=True)
            return vector.tolist()

        return [0.0] * self.vector_size


embedding_service = EmbeddingService()


def get_embedding(text: str) -> list[float]:
    return embedding_service.get_embedding(text)
