import json
import os

DEFAULT_SBERT_MODEL = "BAAI/bge-m3"

# Known model dimensions to avoid loading just to check size
_MODEL_DIMENSIONS = {
    "BAAI/bge-m3": 1024,
    "sentence-transformers/all-MiniLM-L6-v2": 384,
    "all-MiniLM-L6-v2": 384,
    "sentence-transformers/all-mpnet-base-v2": 768,
    "all-mpnet-base-v2": 768,
}


def _get_default_vector_size() -> int:
    """Determine the vector size from the configured SBERT model."""
    model_name = os.getenv("SBERT_MODEL", DEFAULT_SBERT_MODEL)
    return _MODEL_DIMENSIONS.get(model_name, 1024)


VECTOR_SIZE = _get_default_vector_size()


class EmbeddingService:
    """Create dense vectors from CV JSON and job text using SBERT."""

    def __init__(self):
        self.model = None
        self.model_name = os.getenv("SBERT_MODEL", DEFAULT_SBERT_MODEL)
        self.vector_size = VECTOR_SIZE
        try:
            from sentence_transformers import SentenceTransformer

            self.model = SentenceTransformer(self.model_name)
            dim = None
            if hasattr(self.model, 'get_embedding_dimension'):
                dim = self.model.get_embedding_dimension()
            elif hasattr(self.model, 'get_sentence_embedding_dimension'):
                dim = self.model.get_sentence_embedding_dimension()
            self.vector_size = int(dim or VECTOR_SIZE)
            # Update module-level VECTOR_SIZE so DB models pick it up
            import app.core.embedding_engine as _self_module
            _self_module.VECTOR_SIZE = self.vector_size
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
