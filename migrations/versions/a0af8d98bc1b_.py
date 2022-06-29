"""empty message

Revision ID: a0af8d98bc1b
Revises: 
Create Date: 2022-06-28 14:06:25.443870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0af8d98bc1b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('board',
    sa.Column('board_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('owner', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('board_id')
    )
    op.create_table('card',
    sa.Column('card_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('likes_count', sa.Integer(), nullable=False),
    sa.Column('board_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['board_id'], ['board.board_id'], ),
    sa.PrimaryKeyConstraint('card_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('card')
    op.drop_table('board')
    # ### end Alembic commands ###