from collections import namedtuple

_artist_fields = ['alias_list', 'area', 'begin_area', 'end_area', 'country', 'disambiguation', 'ext_score', 'gender',
                  'genres', 'id', 'ipi_list', 'isni_list', 'life_span', 'name', 'sort_name', 'tag_list', 'type']

MbArtistTuple = namedtuple("ArtistTuple", _artist_fields, defaults=(None,) * len(_artist_fields))

_album_fields = ["first_release_date", "genres", "id", "primary_type", "secondary_type_list", "title", "type"]

MbAlbumTuple = namedtuple("AlbumTuple", _album_fields, defaults=(None,) * len(_album_fields))
