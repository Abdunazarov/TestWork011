"""Create transactions table

Revision ID: c510c3924787
Revises: 
Create Date: 2024-12-19 04:31:01.251991

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c510c3924787'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """
    Create the 'transactions' table
    """
    op.create_table(
        'transactions',
        sa.Column('transaction_id', sa.String(), primary_key=True, nullable=False, unique=True),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False)
    )


def downgrade():
    """
    Drop the 'transactions' table
    """
    op.drop_table('transactions')
