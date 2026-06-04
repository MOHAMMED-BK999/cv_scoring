"""add scoring_weights table

Revision ID: e4b341f
Revises: 
Create Date: 2026-06-04 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e4b341f'
down_revision = 'cdb75311be01'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'scoring_weights',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('skills', sa.Float(), nullable=False, server_default='0.40'),
        sa.Column('experience', sa.Float(), nullable=False, server_default='0.30'),
        sa.Column('education', sa.Float(), nullable=False, server_default='0.20'),
        sa.Column('soft_skills', sa.Float(), nullable=False, server_default='0.10'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scoring_weights_id'), 'scoring_weights', ['id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_scoring_weights_id'), table_name='scoring_weights')
    op.drop_table('scoring_weights')
