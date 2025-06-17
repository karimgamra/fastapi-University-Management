"""new

Revision ID: f6c8d9e8eb55
Revises: 
Create Date: 2025-06-16 09:31:59.373709

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6c8d9e8eb55'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String(), nullable=True))



def downgrade() -> None:
   op.drop_column("users", "phone_number")
