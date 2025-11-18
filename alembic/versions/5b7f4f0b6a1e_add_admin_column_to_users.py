"""Add admin column to users

Revision ID: 5b7f4f0b6a1e
Revises: 2df915a8c6ec
Create Date: 2025-11-10 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b7f4f0b6a1e'
down_revision: Union[str, None] = '2df915a8c6ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add admin column with server default false for existing rows
    op.add_column('users', sa.Column('admin', sa.Boolean(), nullable=False, server_default=sa.false()))
    # Optional: drop the server default after backfilling to keep model default-only
    op.alter_column('users', 'admin', server_default=None)


def downgrade() -> None:
    op.drop_column('users', 'admin')

