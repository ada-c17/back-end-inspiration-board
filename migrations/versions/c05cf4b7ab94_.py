"""empty message

Revision ID: c05cf4b7ab94
Revises: 279c48b6df9e
Create Date: 2022-07-18 11:24:24.048464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c05cf4b7ab94'
down_revision = '279c48b6df9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('board', sa.Column('creator', sa.String()))
    op.drop_column('board', 'owner')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('board', sa.Column('owner', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('board', 'creator')
    # ### end Alembic commands ###
