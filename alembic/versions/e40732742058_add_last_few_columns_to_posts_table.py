"""Add last few columns to posts table

Revision ID: e40732742058
Revises: 5ae9803f5687
Create Date: 2023-03-23 23:03:55.767451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e40732742058'
down_revision = '5ae9803f5687'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE')),
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published'),
    op.drop_column('posts', 'created_at'),
    pass
