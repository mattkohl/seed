from typing import NamedTuple, Optional


_section_fields = [
    ("type", Optional[str]),
    ("number", Optional[int]),
    ("artists", Optional[str]),
    ("offset", Optional[int]),
    ("text", Optional[str])
]
SectionTuple = NamedTuple("SectionTuple", _section_fields)
