from typing import NamedTuple, Optional


_verse_fields = [
    ("type", Optional[str]),
    ("number", Optional[int]),
    ("artists", Optional[str]),
    ("offset", Optional[int]),
    ("text", Optional[str])
]
VerseTuple = NamedTuple("VerseTuple", _verse_fields)
