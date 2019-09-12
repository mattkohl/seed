import re
from typing import List


class GenUtils:

    @staticmethod
    def slugify(text: str) -> str:
        slug = text.strip().lower()
        slug = slug[1:] if slug[0] == "'" or slug[0] == "-" else slug
        slug = re.sub(r"ma\$e", "ma-e", slug)
        slug = re.sub(r"a\$ap", "a-ap", slug)
        slug = re.sub(r"curren\$y", "curren-y", slug)
        slug = re.sub(r"\$", "s", slug)
        slug = re.sub(r"^[\-']]", "", slug)
        slug = re.sub(r"/", "-", slug)
        slug = re.sub(r"\s", "-", slug)
        slug = re.sub(r"\.\.\.\.", "-", slug)
        slug = re.sub(r"\.", "", slug)
        slug = re.sub(r"!", "", slug)
        slug = re.sub(r":", "-", slug)
        slug = re.sub(r"\*", "", slug)
        slug = re.sub(r"#", "-", slug)
        slug = re.sub(r"%", "", slug)
        slug = re.sub(r"&amp;", "and", slug)
        slug = re.sub(r"&", "and", slug)
        slug = re.sub(r"\+", "-", slug)
        slug = re.sub(r"é", "e", slug)
        slug = re.sub(r"–", "-", slug)
        slug = re.sub(r"ó", "o", slug)
        slug = re.sub(r"á", "a", slug)
        slug = re.sub(r"@", "at", slug)
        slug = re.sub(r"½", "half", slug)
        slug = re.sub(r"ō", "o", slug)
        slug = re.sub(r"'", "", slug)
        slug = re.sub(r"’", "", slug)
        slug = re.sub(r'"', "", slug)
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
        st = re.sub(r" \(Vocal\)", "", song_title, re.IGNORECASE)
        st = re.sub(r" \(screwed\)", "", song_title, re.IGNORECASE)
        st = re.sub(r" \(with.*?\)", "", st, re.IGNORECASE)
        st = re.sub(r" \(feat.*?\)", "", st, re.IGNORECASE)
        st = re.sub(r" \(Sky High\)", "", st, re.IGNORECASE)
        st = re.sub(r" - feat.*?$", "", st, re.IGNORECASE)
        st = re.sub(r" feat\. .*?$", "", st, re.IGNORECASE)
        st = re.sub(r" - Dirty$", "", st, re.IGNORECASE)
        st = re.sub(r" - Edit$", "", st, re.IGNORECASE)
        st = re.sub(r" - LP Mix$", "", st, re.IGNORECASE)
        st = re.sub(r" - Explici?t$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Version$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Chopped$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Slowed$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Screwed$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Chopped & Screwed$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Album Version\s?\(Edited\)$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Screwed & Chopped$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Remastered.*?$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Slabed$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?S\.L\.A\.B.*?$", "", st, re.IGNORECASE)
        st = re.sub(r" - Bonus .*?$", "", st, re.IGNORECASE)
        st = re.sub(r" - From \"House Party\" Soundtrack", "", st, re.IGNORECASE)
        st = re.sub(r" - radio edit.*?$", "", st, re.IGNORECASE)
        st = re.sub(r" - Acapella.*?$", "", st, re.IGNORECASE)
        st = re.sub(r" - \d\d\d\d Remaster$", "", st, re.IGNORECASE)
        st = re.sub(r" - \d\d\d\d Mix\/Master$", "", st, re.IGNORECASE)
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
        _name = "Rob Base and DJ E-Z Rock" if name == "Rob Base & DJ EZ Rock" else _name
        _name = "Treacherous Three" if name == "The Treacherous Three" else _name
        _name = "Sugarhill Gang" if name == "The Sugarhill Gang" else _name
        _name = "Masta Ace" if name.lower() == "masta ace incorporated" else _name
        _name = "2Pac" if name.lower() == "makaveli" else _name
        _name = _name[:-4] if _name.endswith(", The") else _name
        _name = _name[4:] if _name.startswith("The Egyptian") else _name
        return _name

    @staticmethod
    def adjust_song_title(song_title: str, album_title: str) -> str:
        title = GenUtils.prune(song_title) if song_title.lower() != "intro" else GenUtils.prune(f"{song_title} ({album_title}) ")
        title = title.replace("H-E", "Hoe")
        title = title.replace("H*es", "Hoes")
        title = title.replace("N____", "Nigga")
        title = title.replace("N****", "Nigga")
        title = title.replace("N***a", "Nigga")
        title = title.replace("N!@@a", "Nigga")
        title = title.replace("N*gga", "Nigga")
        title = title.replace("N**ga", "Nigga")
        title = title.replace("N**gas", "Niggas")
        title = title.replace("N**gaz", "Niggaz")
        title = title.replace("N***az", "Niggaz")
        title = title.replace("F*", "Fuck")
        title = title.replace("F*ck", "Fuck")
        title = title.replace("F**k", "Fuck")
        title = title.replace("F***", "Fuck")
        title = title.replace("F--k", "Fuck")
        title = title.replace("D**k", "Dick")
        title = title.replace("A*s", "Ass")
        title = title.replace("A**", "Ass")
        title = title.replace("A--", "Ass")
        title = title.replace("B____", "Bitch")
        title = title.replace("B@#$H", "Bitch")
        title = title.replace("B@!Ch", "Bitch")
        title = title.replace("B---H", "Bitch")
        title = title.replace("B**ch", "Bitch")
        title = title.replace("B***h", "Bitch")
        title = title.replace("B-t-h", "Bitch")
        title = title.replace("B*tches", "Bitches")
        title = title.replace("B****es", "Bitches")
        title = title.replace("Sh*t", "Shit")
        title = title.replace("Sh!t", "Shit")
        title = title.replace("Sh--", "Shit")
        title = title.replace("S...", "Shit")
        title = title.replace("Bullsh--", "Bullshit")
        title = title.replace("S***", "Shit")
        title = title.replace("Sh**", "Shit")
        title = title.replace("Muthaf*cka", "Muthafucka")
        title = title.replace("#!*@", "Fuck")
        title = title.replace("****", "Fuck")

        return title
