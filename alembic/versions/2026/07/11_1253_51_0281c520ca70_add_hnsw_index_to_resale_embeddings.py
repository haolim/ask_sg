"""add hnsw index to resale embeddings

Revision ID: 0281c520ca70
Revises: 99b94706a8a5
Create Date: 2026-07-11 12:53:51.747420

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0281c520ca70'
down_revision: Union[str, Sequence[str], None] = '99b94706a8a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_embeddings_hnsw "
        "ON resale_transactions_embeddings "
        "USING hnsw (embedding vector_cosine_ops) "
        "WITH (m = 16, ef_construction = 64)"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX IF EXISTS idx_embeddings_hnsw")
