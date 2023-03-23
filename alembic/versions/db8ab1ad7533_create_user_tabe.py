"""Create user tabe

Revision ID: db8ab1ad7533
Revises: f7918a102f96
Create Date: 2023-03-23 01:00:00.604445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db8ab1ad7533'
down_revision = 'f7918a102f96'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column(('id'), sa.Integer(), nullable=False),
                    sa.Column(('email'), sa.String(), nullable=False),
                    sa.Column(('password'), sa.String(), nullable=False),
                    sa.Column(('created_at'), sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
