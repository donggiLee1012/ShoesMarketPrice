"""empty message

Revision ID: dbea50bcb0ae
Revises: 93726435b950
Create Date: 2020-11-05 00:52:33.425267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbea50bcb0ae'
down_revision = '93726435b950'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shoes', sa.Column('keyword', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shoes', 'keyword')
    # ### end Alembic commands ###
