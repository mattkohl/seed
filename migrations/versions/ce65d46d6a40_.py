"""empty message

Revision ID: ce65d46d6a40
Revises: 92016ded09fe
Create Date: 2020-05-13 16:12:02.680394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce65d46d6a40'
down_revision = '92016ded09fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('albums', sa.Column('geni_uri', sa.Text(), nullable=True))
    op.add_column('artists', sa.Column('geni_uri', sa.Text(), nullable=True))
    op.add_column('tracks', sa.Column('geni_uri', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tracks', 'geni_uri')
    op.drop_column('artists', 'geni_uri')
    op.drop_column('albums', 'geni_uri')
    # ### end Alembic commands ###
