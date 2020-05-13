from collections import namedtuple
from typing import NamedTuple, Optional


_section_fields = [
    ("type", Optional[str]),
    ("number", Optional[int]),
    ("artists", Optional[str]),
    ("offset", Optional[int]),
    ("text", Optional[str])
]
SectionTuple = NamedTuple("SectionTuple", _section_fields)

_track_fields = ['title', 'url', 'album', 'primary_artists', 'featured_artists']
TrackTuple = namedtuple("TrackTuple", _track_fields, defaults=[None, None, None, list(), list()])

_album_fields = ['name', 'release_date_string', 'release_date', 'header_image_url', 'url', 'artist']
AlbumTuple = namedtuple("AlbumTuple", _album_fields, defaults=(None,) * len(_album_fields))

_artist_fields = ['name', 'header_image_url', 'url']
ArtistTuple = namedtuple("ArtistTuple", _artist_fields, defaults=(None,) * len(_artist_fields))
