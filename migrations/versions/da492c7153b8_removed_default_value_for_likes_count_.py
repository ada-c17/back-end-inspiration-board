"""removed default value for likes_count in Card model

Revision ID: da492c7153b8
Revises: 4ba675b5d851
Create Date: 2022-06-27 20:58:43.073379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da492c7153b8'
down_revision = '4ba675b5d851'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('card', 'likes_count',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('card', 'likes_count',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
