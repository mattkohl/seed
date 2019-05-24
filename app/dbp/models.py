from collections import namedtuple

_candidates_fields = ["text", "confidence", "support", "types", "sparql", "policy", "Resources"]
CandidatesTuple = namedtuple("CandidatesTuple", _candidates_fields, defaults=((None,) * (len(_candidates_fields) - 1)) + (list(),))

AnnotationTuple = namedtuple("AnnotationTuple", ["text"], defaults=(None,))

_location_fields = ["uri", "label", "latitude", "longitude", "hometown_of", "birthplace_of"]
LocationTuple = namedtuple("LocationTuple", _location_fields, defaults=((None,) * (len(_location_fields))))

