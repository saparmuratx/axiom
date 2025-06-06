"""add profile avatar

Revision ID: 47b76ef6b920
Revises: 3a9349c39ef0
Create Date: 2025-05-04 18:08:20.214979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47b76ef6b920'
down_revision: Union[str, None] = '3a9349c39ef0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('avatar', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('profiles', 'avatar')
    # ### end Alembic commands ###
