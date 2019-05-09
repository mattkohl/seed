"""empty message

Revision ID: 8174011b38d0
Revises: 
Create Date: 2019-05-09 08:55:21.467883

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8174011b38d0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('albums',
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('release_date_string', sa.Text(), nullable=True),
    sa.Column('release_date', sa.DateTime(), nullable=True),
    sa.Column('spot_uri', sa.Text(), nullable=True),
    sa.Column('images_json', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_albums_timestamp'), 'albums', ['timestamp'], unique=False)
    op.create_table('artists',
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('spot_uri', sa.Text(), nullable=True),
    sa.Column('dbp_uri', sa.Text(), nullable=True),
    sa.Column('mb_id', sa.Text(), nullable=True),
    sa.Column('mb_obj', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_artists_timestamp'), 'artists', ['timestamp'], unique=False)
    op.create_table('album_artist',
    sa.Column('album_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['album_id'], ['albums.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('album_id', 'artist_id')
    )
    op.create_table('tracks',
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('spot_uri', sa.Text(), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('album_id', sa.Integer(), nullable=True),
    sa.Column('preview_url', sa.Text(), nullable=True),
    sa.Column('lyrics', sa.Text(), nullable=True),
    sa.Column('lyrics_url', sa.Text(), nullable=True),
    sa.Column('lyrics_annotated', sa.Text(), nullable=True),
    sa.Column('lyrics_annotations_json', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('lyrics_fetched_timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['album_id'], ['albums.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tracks_timestamp'), 'tracks', ['timestamp'], unique=False)
    op.create_table('track_artist',
    sa.Column('track_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['track_id'], ['tracks.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('track_id', 'artist_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('track_artist')
    op.drop_index(op.f('ix_tracks_timestamp'), table_name='tracks')
    op.drop_table('tracks')
    op.drop_table('album_artist')
    op.drop_index(op.f('ix_artists_timestamp'), table_name='artists')
    op.drop_table('artists')
    op.drop_index(op.f('ix_albums_timestamp'), table_name='albums')
    op.drop_table('albums')
    # ### end Alembic commands ###
