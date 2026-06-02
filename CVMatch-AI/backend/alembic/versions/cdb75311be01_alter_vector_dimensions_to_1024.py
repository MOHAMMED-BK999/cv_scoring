"""alter_vector_dimensions_to_1024

Revision ID: cdb75311be01
Revises: 2f5b6c7d8e9a
Create Date: 2026-05-24 18:25:49.129971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdb75311be01'
down_revision: Union[str, Sequence[str], None] = '2f5b6c7d8e9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        # Drop the existing cosine indexes since their dimensions must match the column type
        op.execute("DROP INDEX IF EXISTS ix_candidate_profiles_embedding_vector_cosine")
        op.execute("DROP INDEX IF EXISTS ix_job_descriptions_embedding_vector_cosine")
        
        # Alter the column type to 1024 dimensions
        op.execute("ALTER TABLE job_descriptions ALTER COLUMN embedding_vector TYPE vector(1024) USING NULL")
        op.execute("ALTER TABLE candidate_profiles ALTER COLUMN embedding_vector TYPE vector(1024) USING NULL")
        
        # Recreate the cosine indexes for 1024 dimensions
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
    """Downgrade schema."""
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        # Drop the 1024 dimension cosine indexes
        op.execute("DROP INDEX IF EXISTS ix_candidate_profiles_embedding_vector_cosine")
        op.execute("DROP INDEX IF EXISTS ix_job_descriptions_embedding_vector_cosine")
        
        # Revert the column type to 768 dimensions
        op.execute("ALTER TABLE job_descriptions ALTER COLUMN embedding_vector TYPE vector(768) USING NULL")
        op.execute("ALTER TABLE candidate_profiles ALTER COLUMN embedding_vector TYPE vector(768) USING NULL")
        
        # Recreate the cosine indexes for 768 dimensions
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

