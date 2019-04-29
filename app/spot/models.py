from collections import namedtuple

Track = namedtuple("Track",
                   ['album', 'artists', 'disc_number', 'duration_ms', 'episode', 'explicit',
                    'external_ids', 'external_urls', 'href', 'id', 'is_local', 'name', 'popularity', 'preview_url',
                    'track', 'track_number', 'type', 'uri'])

Album = namedtuple("Album",
                   ['album_type', 'artists', 'external_urls', 'href', 'id', 'images', 'name',
                    'release_date', 'release_date_precision', 'total_tracks', 'type', 'uri'])

Artist = namedtuple("Artist",
                    ['external_urls', 'href', 'id', 'name', 'type', 'uri'])
