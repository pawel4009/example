"""Add content column to posts tabnle

Revision ID: f7918a102f96
Revises: d236c7f93ca5
Create Date: 2023-03-23 00:53:10.881541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7918a102f96'
down_revision = 'd236c7f93ca5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
