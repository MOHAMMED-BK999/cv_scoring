"""Add pgvector cosine indexes

Revision ID: 2f5b6c7d8e9a
Revises: 9c7b1fd67c2a
Create Date: 2026-05-22 20:30:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = "2f5b6c7d8e9a"
down_revision: Union[str, Sequence[str], None] = "9c7b1fd67c2a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
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


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_candidate_profiles_embedding_vector_cosine")
    op.execute("DROP INDEX IF EXISTS ix_job_descriptions_embedding_vector_cosine")
