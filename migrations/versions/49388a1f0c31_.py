"""empty message

Revision ID: 49388a1f0c31
Revises: 94d3731683f2
Create Date: 2023-07-18 08:58:44.236543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49388a1f0c31'
down_revision = '94d3731683f2'
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
