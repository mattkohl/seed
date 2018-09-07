import re


class GenUtils:

    @staticmethod
    def slugify(text: str) -> str:
        slug = text.strip().lower()
        slug = slug[1:] if slug[0] == "'" or slug[0] == "-" else slug
        slug = re.sub("^[\-']]", "", slug)
        slug = re.sub("\s", "-", slug)
        slug = re.sub("\.", "", slug)
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
        st = re.sub("\s\(with.*?\)$", "", song_title, re.I)
        st = re.sub("\s\(feat.*?\)$", "", song_title, re.I)
        st = re.sub(" - Feat.*?$", "", song_title, re.I)
        st = re.sub(" feat\. .*?$", "", song_title, re.I)
        st = re.sub(" - .*?Version$", "", song_title, re.I)
        st = re.sub(" - Bonus .*?$", "", song_title, re.I)
        return st

    @staticmethod
    def link(artist: str, song_title: str) -> str:
        h = "https"
        g = "genius"
        c = "com"
        artist = "The " + artist[:-4] if artist.endswith(", The") else artist
        song_title = GenUtils.prune(song_title)
        slug = GenUtils.slugify(artist + " " + song_title + "-lyrics")
        return f"{h}://{g}.{c}/{slug}"
