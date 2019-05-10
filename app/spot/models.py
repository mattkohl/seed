from collections import namedtuple

_track_fields = ['album', 'artists', 'disc_number', 'duration_ms', 'episode', 'explicit',
                 'external_ids', 'external_urls', 'href', 'id', 'is_local', 'name', 'popularity', 'preview_url',
                 'track', 'track_number', 'type', 'uri']
TrackTuple = namedtuple("TrackTuple", _track_fields, defaults=(None,) * len(_track_fields))

_album_fields = ['album_type', 'album_group', 'artists', 'external_urls', 'href', 'id', 'images', 'name',
                 'release_date', 'release_date_string', 'release_date_precision', 'total_tracks', 'type',
                 'uri']
AlbumTuple = namedtuple("AlbumTuple", _album_fields, defaults=(None,) * len(_album_fields))

_artist_fields = ['external_urls', 'href', 'id', 'name', 'type', 'uri']
ArtistTuple = namedtuple("ArtistTuple", _artist_fields, defaults=(None,) * len(_artist_fields))
