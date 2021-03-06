"""empty message

Revision ID: 0ab3831208d2
Revises: 7b199ba57d25
Create Date: 2019-09-19 10:50:10.765657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ab3831208d2'
down_revision = '7b199ba57d25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Songs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('artist', sa.String(), nullable=True),
    sa.Column('album', sa.String(), nullable=True),
    sa.Column('releaseDate', sa.String(), nullable=True),
    sa.Column('songTitle', sa.String(), nullable=True),
    sa.Column('feat', sa.String(), nullable=True),
    sa.Column('lyrics', sa.Text(), nullable=True),
    sa.Column('discogsDate', sa.String(), nullable=True),
    sa.Column('relDateVerified', sa.String(), nullable=True),
    sa.Column('lyricsVerified', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Songs')
    # ### end Alembic commands ###
