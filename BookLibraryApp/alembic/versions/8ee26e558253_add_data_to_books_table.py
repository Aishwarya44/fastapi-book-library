"""Add data to books table

Revision ID: 8ee26e558253
Revises: 3d860b7b7fe0
Create Date: 2025-09-16 10:54:57.939454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ee26e558253'
down_revision: Union[str, Sequence[str], None] = '3d860b7b7fe0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    books_table = (
        sa.table("books",
                 sa.column("id"),
                 sa.column("title"),
                 sa.column("author"),
                 sa.column("published_year"),
                 sa.column("available"),
                 sa.column("owner_id"),
                 )
    )
    conn.execute(
        books_table.insert(),[
            {"id":1, "title":"Book 1", "author":"author 1", "published_year":1999, "available":True, "owner_id":1},
            {"id":2, "title":"Book 2", "author":"author 2", "published_year":2000, "available":True, "owner_id":2},
            {"id":3, "title":"Book 3", "author":"author 3", "published_year":2001, "available":True, "owner_id":3},
            {"id":4, "title":"Book 4", "author":"author 4", "published_year":2002, "available":True, "owner_id":2},
            {"id":5, "title":"Book 5", "author":"author 5", "published_year":2003, "available":True, "owner_id":1},
            {"id":6, "title":"Book 6", "author":"author 6", "published_year":2004, "available":True, "owner_id":1},

        ]
    )

def downgrade() -> None:
    """Downgrade schema."""
    pass
