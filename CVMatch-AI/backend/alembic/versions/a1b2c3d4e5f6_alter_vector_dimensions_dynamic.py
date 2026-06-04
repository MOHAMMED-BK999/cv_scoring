"""alter_vector_dimensions_dynamic

Revision ID: a1b2c3d4e5f6
Revises: e4b341f
Create Date: 2026-06-04 22:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import os


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'e4b341f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Determine vector size from env or default to the model in use
_MODEL_DIMENSIONS = {
    "BAAI/bge-m3": 1024,
    "sentence-transformers/all-MiniLM-L6-v2": 384,
    "all-MiniLM-L6-v2": 384,
    "sentence-transformers/all-mpnet-base-v2": 768,
    "all-mpnet-base-v2": 768,
}
_SBERT_MODEL = os.getenv("SBERT_MODEL", "BAAI/bge-m3")
VECTOR_DIM = _MODEL_DIMENSIONS.get(_SBERT_MODEL, 1024)


def upgrade() -> None:
    """Resize embedding_vector columns to match the SBERT model in use."""
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        # Drop existing cosine indexes
        op.execute("DROP INDEX IF EXISTS ix_candidate_profiles_embedding_vector_cosine")
        op.execute("DROP INDEX IF EXISTS ix_job_descriptions_embedding_vector_cosine")

        # Alter column type to match current model dimensions
        # USING NULL clears existing data since old vectors have wrong dimensions
        op.execute(
            f"ALTER TABLE job_descriptions ALTER COLUMN embedding_vector TYPE vector({VECTOR_DIM}) USING NULL"
        )
        op.execute(
            f"ALTER TABLE candidate_profiles ALTER COLUMN embedding_vector TYPE vector({VECTOR_DIM}) USING NULL"
        )

        # Recreate cosine indexes
        op.execute(
            f"""
            CREATE INDEX IF NOT EXISTS ix_job_descriptions_embedding_vector_cosine
            ON job_descriptions
            USING ivfflat (embedding_vector vector_cosine_ops)
            WITH (lists = 100)
            WHERE embedding_vector IS NOT NULL
            """
        )
        op.execute(
            f"""
            CREATE INDEX IF NOT EXISTS ix_candidate_profiles_embedding_vector_cosine
            ON candidate_profiles
            USING ivfflat (embedding_vector vector_cosine_ops)
            WITH (lists = 100)
            WHERE embedding_vector IS NOT NULL
            """
        )


def downgrade() -> None:
    """Revert to 1024 dimensions."""
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("DROP INDEX IF EXISTS ix_candidate_profiles_embedding_vector_cosine")
        op.execute("DROP INDEX IF EXISTS ix_job_descriptions_embedding_vector_cosine")

        op.execute("ALTER TABLE job_descriptions ALTER COLUMN embedding_vector TYPE vector(1024) USING NULL")
        op.execute("ALTER TABLE candidate_profiles ALTER COLUMN embedding_vector TYPE vector(1024) USING NULL")

        op.execute(
            """
            CREATE INDEX IF NOT EXISTS ix_job_descriptions_embedding_vector_cosine
            ON job_descriptions
            USING ivfflat (embedding_vector vector_cosine_ops)
            WITH (lists = 100)
            WHERE embedding_vector IS NOT NULL
            """
        )
        op.execute(
            """
            CREATE INDEX IF NOT EXISTS ix_candidate_profiles_embedding_vector_cosine
            ON candidate_profiles
            USING ivfflat (embedding_vector vector_cosine_ops)
            WITH (lists = 100)
            WHERE embedding_vector IS NOT NULL
            """
        )
