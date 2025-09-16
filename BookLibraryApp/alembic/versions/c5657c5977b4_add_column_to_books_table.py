"""add column to books table

Revision ID: c5657c5977b4
Revises: 
Create Date: 2025-09-16 09:50:53.895939

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5657c5977b4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("books", sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id")))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("books", "owner_id")
