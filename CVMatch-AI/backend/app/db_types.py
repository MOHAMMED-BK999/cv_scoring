import json
from typing import Any

from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB


class SQLiteVector(TypeDecorator):
    """Store vector values as JSON when running the local SQLite dev database."""

    impl = JSON
    cache_ok = True

    def process_bind_param(self, value: Any, dialect) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            return value
        return list(value)

    def process_result_value(self, value: Any, dialect) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            return json.loads(value)
        return value


def JsonList():
    return JSON().with_variant(JSONB, "postgresql")


def EmbeddingVector(dimensions: int = 768):
    return SQLiteVector().with_variant(Vector(dimensions), "postgresql")
