import re
from typing import List


class GenUtils:

    @staticmethod
    def slugify(text: str) -> str:
        slug = text.strip().lower()
        slug = slug[1:] if slug[0] == "'" or slug[0] == "-" else slug
        slug = re.sub(r"a\$ap", "a-ap", slug)
        slug = re.sub(r"\$", "s", slug)
        slug = re.sub(r"^[\-']]", "", slug)
        slug = re.sub(r"\s", "-", slug)
        slug = re.sub(r"\.", "", slug)
        slug = re.sub(r"!", "", slug)
        slug = re.sub(r"[:/]", "", slug)
        slug = re.sub(r"\*", "", slug)
        slug = re.sub(r"#", " ", slug)
        slug = re.sub(r"%", "percent", slug)
        slug = re.sub(r"&amp;", "and", slug)
        slug = re.sub(r"&", "and", slug)
        slug = re.sub(r"\+", "and", slug)
        slug = re.sub(r"é", "e", slug)
        slug = re.sub(r"–", "-", slug)
        slug = re.sub(r"ó", "o", slug)
        slug = re.sub(r"á", "a", slug)
        slug = re.sub(r"@", "at", slug)
        slug = re.sub(r"½", "half", slug)
        slug = re.sub(r"ō", "o", slug)
        slug = re.sub(r"'", "", slug)
        slug = re.sub(r"’", "", slug)
        slug = re.sub(r"“", "", slug)
        slug = re.sub(r"”", "", slug)
        slug = re.sub(r",", "", slug)
        slug = re.sub(r"-$", "", slug)
        slug = re.sub(r"\?", "", slug)
        slug = re.sub(r"[()]", "", slug)
        slug = re.sub(r"\s-", "-", slug)
        return slug

    @staticmethod
    def prune(song_title: str) -> str:
        st = re.sub(r" \(with.*?\)", "", song_title, re.IGNORECASE)
        st = re.sub(r" \(feat.*?\)", "", st, re.IGNORECASE)
        st = re.sub(r" - feat.*?$", "", st, re.IGNORECASE)
        st = re.sub(r" feat\. .*?$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Version$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Chopped$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Screwed$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Chopped & Screwed$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Screwed & Chopped$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Remastered.*?$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Slabed$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?S\.L\.A\.B.*?$", "", st, re.IGNORECASE)
        st = re.sub(r" - Bonus .*?$", "", st, re.IGNORECASE)
        st = re.sub(r"^Slabed - (.*)", r"\g<1>", st, re.IGNORECASE)
        return st

    @staticmethod
    def link(artists: List[str], song_title: str, album_title: str = "") -> str:
        h = "https"
        g = "genius"
        c = "com"
        if len(artists) == 2:
            _a1, _a2 = artists
            artist = f"{GenUtils.adjust_artist_name(_a1)} and {GenUtils.adjust_artist_name(_a2)}"
        else:
            _artist = artists[0]
            artist = GenUtils.adjust_artist_name(_artist)
        song_title = GenUtils.adjust_song_title(song_title, album_title)
        _slug = GenUtils.slugify(artist + " " + song_title + "-lyrics")
        slug = re.sub(r"[-]+", "-", _slug)
        return f"{h}://{g}.{c}/{slug.capitalize()}"

    @staticmethod
    def adjust_artist_name(name: str) -> str:
        _name = "Yasiin Bey" if name.lower() == "mos def" else name
        _name = "2Pac" if name.lower() == "makaveli" else name
        _name = _name[:-4] if _name.endswith(", The") else _name
        # _name = _name[4:] if _name.startswith("The ") else _name
        return _name

    @staticmethod
    def adjust_song_title(song_title: str, album_title: str) -> str:
        title = GenUtils.prune(song_title) if song_title.lower() != "intro" else GenUtils.prune(f"{song_title} ({album_title}) ")
        title = title.replace("F**k", "Fuck")
        title = title.replace("Sh*t", "Shit")
        title = title.replace("S***", "Shit")
        title = title.replace("Muthaf*cka", "Muthafucka")
        return title
