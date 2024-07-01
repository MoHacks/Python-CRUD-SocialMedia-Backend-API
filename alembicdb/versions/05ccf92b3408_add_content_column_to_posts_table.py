"""add content column to posts table

Revision ID: 05ccf92b3408
Revises: abebab7ced25
Create Date: 2024-07-01 12:27:41.108919

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05ccf92b3408'
down_revision: Union[str, None] = 'abebab7ced25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    

def downgrade() -> None:
    op.drop_column('posts', 'content')
    
