from collections import namedtuple

_track_fields = ['album', 'disc_number', 'duration_ms', 'episode', 'explicit',
                 'external_ids', 'external_urls', 'href', 'id', 'is_local', 'label', 'name', 'popularity', 'preview_url',
                 'track', 'track_number', 'type', 'uri', 'primary_artists', 'featured_artists']
TrackTuple = namedtuple("TrackTuple", _track_fields, defaults=(None,) * len(_track_fields))

_album_fields = ['album_type', 'album_group', 'artists', 'copyrights', 'external_ids', 'external_urls', 'genres',
                 'href', 'id', 'images', 'label', 'name', 'popularity', 'release_date', 'release_date_string',
                 'release_date_precision', 'tracks', 'total_tracks', 'type', 'uri']
AlbumTuple = namedtuple("AlbumTuple", _album_fields, defaults=(None,) * len(_album_fields))

_artist_fields = ['external_urls', 'followers', 'genres', 'href', 'id', 'images', 'name', 'popularity', 'type', 'uri']
ArtistTuple = namedtuple("ArtistTuple", _artist_fields, defaults=(None,) * len(_artist_fields))

_genre_fields = ['id', 'name']
GenreTuple = namedtuple("GenreTuple", _genre_fields, defaults=(None,) * len(_genre_fields))
