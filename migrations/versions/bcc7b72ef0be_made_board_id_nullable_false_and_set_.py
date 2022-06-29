"""Made board_id nullable=False and set cascade in board.cards

Revision ID: bcc7b72ef0be
Revises: 762b62826263
Create Date: 2022-06-29 14:47:51.272150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcc7b72ef0be'
down_revision = '762b62826263'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('card', 'board_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('card', 'board_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
