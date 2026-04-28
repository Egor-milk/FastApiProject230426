"""Пересоздал базу

Revision ID: ef7dd735e258
Revises: 9554a7bcdba3
Create Date: 2026-04-28 16:24:03.399131

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "ef7dd735e258"
down_revision: Union[str, Sequence[str], None] = "9554a7bcdba3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass