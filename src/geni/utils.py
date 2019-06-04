import re
from typing import List


class GenUtils:

    heading_regex = re.compile(r"\[(.*):\s(.*)\]\n(.*)")

    @staticmethod
    def slugify(text: str) -> str:
        slug = text.strip().lower()
        slug = slug[1:] if slug[0] == "'" or slug[0] == "-" else slug
        slug = re.sub("^[\-']]", "", slug)
        slug = re.sub("\s", "-", slug)
        slug = re.sub("\.", "", slug)
        slug = re.sub("!", "", slug)
        slug = re.sub("[:/]", "", slug)
        slug = re.sub("\$", "-", slug)
        slug = re.sub("\*", "", slug)
        slug = re.sub("#", "number", slug)
        slug = re.sub("%", "percent", slug)
        slug = re.sub("&amp;", "and", slug)
        slug = re.sub("&", "and", slug)
        slug = re.sub("\+", "and", slug)
        slug = re.sub("é", "e", slug)
        slug = re.sub("ó", "o", slug)
        slug = re.sub("á", "a", slug)
        slug = re.sub("@", "at", slug)
        slug = re.sub("½", "half", slug)
        slug = re.sub("ō", "o", slug)
        slug = re.sub("'", "", slug)
        slug = re.sub(",", "", slug)
        slug = re.sub("-$", "", slug)
        slug = re.sub("\?", "", slug)
        slug = re.sub("[()]", "", slug)
        slug = re.sub("\s-", "-", slug)
        return slug

    @staticmethod
    def prune(song_title: str) -> str:
        st = re.sub("\s\(with.*?\)", "", song_title, re.I)
        st = re.sub("\s\(feat.*?\)", "", st, re.I)
        st = re.sub(" - feat.*?$", "", st, re.I)
        st = re.sub(" feat\. .*?$", "", st, re.I)
        st = re.sub(" - .*?version$", "", st, re.I)
        st = re.sub(" - bonus .*?$", "", st, re.I)
        return st

    @staticmethod
    def link(artists: List[str], song_title: str) -> str:
        h = "https"
        g = "genius"
        c = "com"
        _artist = artists[0]
        artist = "The " + _artist[:-4] if _artist.endswith(", The") else _artist
        song_title = GenUtils.prune(song_title)
        _slug = GenUtils.slugify(artist + " " + song_title + "-lyrics")
        slug = re.sub("[-]+", "-", _slug)
        return f"{h}://{g}.{c}/{slug}"
