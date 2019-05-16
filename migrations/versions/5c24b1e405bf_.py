"""empty message

Revision ID: 5c24b1e405bf
Revises: 8174011b38d0
Create Date: 2019-05-15 08:15:36.087762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c24b1e405bf'
down_revision = '8174011b38d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('albums', sa.Column('dbp_uri', sa.Text(), nullable=True))
    op.add_column('tracks', sa.Column('dbp_uri', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tracks', 'dbp_uri')
    op.drop_column('albums', 'dbp_uri')
    # ### end Alembic commands ###