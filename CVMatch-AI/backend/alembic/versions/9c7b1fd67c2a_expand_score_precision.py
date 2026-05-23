"""Expand score precision

Revision ID: 9c7b1fd67c2a
Revises: 4eec5e321de7
Create Date: 2026-05-17 15:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9c7b1fd67c2a"
down_revision: Union[str, Sequence[str], None] = "4eec5e321de7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


SCORE_COLUMNS = (
    "semantic_score",
    "skills_score",
    "experience_score",
    "education_score",
)


def upgrade() -> None:
    for column in SCORE_COLUMNS:
        op.alter_column(
            "scoring_results",
            column,
            existing_type=sa.Numeric(precision=5, scale=4),
            type_=sa.Numeric(precision=5, scale=2),
            existing_nullable=True,
        )


def downgrade() -> None:
    for column in SCORE_COLUMNS:
        op.alter_column(
            "scoring_results",
            column,
            existing_type=sa.Numeric(precision=5, scale=2),
            type_=sa.Numeric(precision=5, scale=4),
            existing_nullable=True,
        )
