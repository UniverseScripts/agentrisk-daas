"""add_subscription_id

Revision ID: b70298e752a9
Revises: 8a31c7e4b60b
Create Date: 2026-07-26 18:48:02.845952

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b70298e752a9'
down_revision: Union[str, Sequence[str], None] = '8a31c7e4b60b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('api_key', sa.Column('subscription_id', sa.String(), nullable=True))
    op.create_index(op.f('ix_api_key_subscription_id'), 'api_key', ['subscription_id'], unique=True)
    op.drop_column('api_key', 'token_balance')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('api_key', sa.Column('token_balance', sa.Integer(), server_default='0', nullable=False))
    op.drop_index(op.f('ix_api_key_subscription_id'), table_name='api_key')
    op.drop_column('api_key', 'subscription_id')
