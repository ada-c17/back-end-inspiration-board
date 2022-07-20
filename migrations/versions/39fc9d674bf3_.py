"""empty message

Revision ID: 39fc9d674bf3
Revises: f38f3b858867
Create Date: 2022-06-29 11:09:38.116839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39fc9d674bf3'
down_revision = 'f38f3b858867'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('card', sa.Column('board_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'card', 'board', ['board_id'], ['board_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'card', type_='foreignkey')
    op.drop_column('card', 'board_id')
    # ### end Alembic commands ###
