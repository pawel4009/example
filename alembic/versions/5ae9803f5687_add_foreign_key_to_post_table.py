"""Add foreign key to post table

Revision ID: 5ae9803f5687
Revises: db8ab1ad7533
Create Date: 2023-03-23 22:58:07.716369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ae9803f5687'
down_revision = 'db8ab1ad7533'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
