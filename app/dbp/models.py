from collections import namedtuple

CandidatesTuple = namedtuple("CandidatesTuple",
                             ["text", "confidence", "support", "types", "sparql", "policy", "Resources"])

AnnotationTuple = namedtuple("AnnotationTuple", ["text"])
