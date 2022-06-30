"""added one to many relationship

Revision ID: d7ff17a7cc73
Revises: ec0bc091fa62
Create Date: 2022-06-30 08:05:59.289495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7ff17a7cc73'
down_revision = 'ec0bc091fa62'
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