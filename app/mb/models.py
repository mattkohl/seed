from collections import namedtuple

_fields = ['alias_list', 'area', 'begin_area', 'end_area', 'country', 'disambiguation', 'ext_score', 'gender', 'id',
                          'ipi_list', 'life_span', 'name', 'sort_name', 'tag_list', 'type']

ArtistTuple = namedtuple("ArtistTuple", _fields, defaults=(None,) * len(_fields))
