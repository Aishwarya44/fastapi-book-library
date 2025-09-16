"""Add data to users table

Revision ID: 3d860b7b7fe0
Revises: b9216e774065
Create Date: 2025-09-16 10:35:31.066000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d860b7b7fe0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    user_table = sa.table('users',
                          sa.column('id', sa.Integer),
                          sa.column('username', sa.String),
                          sa.column('email', sa.String),
                          sa.column('password', sa.String),
                          sa.column('first_name', sa.String),
                          sa.column('last_name', sa.String),
                          sa.column('active', sa.Boolean)
                          )
    conn.execute(user_table.insert(),
                 [
                     {"id":1,"username":"admin","email":"admin@user.com","password":"password", "first_name":"admin","last_name":"bhai","active":True},
                     {"id":2,"username":"one","password":"password","email":"one@user.com", "first_name":"aish","last_name":"bharambe","active":True},
                     {"id":3,"username":"two","password":"password","email":"two@user.com", "first_name":"sonuli","last_name":"bharambe","active":True},
                     {"id":4,"username":"three","password":"password","email":"three@user.com", "first_name":"viraj","last_name":"bhoge","active":True},
                     {"id":5,"username":"four","password":"password","email":"four@user.com", "first_name":"Abcd","last_name":"xyz","active":True},
                     {"id":6,"username":"five","password":"password","email":"five@user.com", "first_name":"John","last_name":"Doe","active":True},
                 ])




def downgrade() -> None:
    """Downgrade schema."""
    pass
