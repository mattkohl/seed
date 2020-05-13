import re
import traceback
from copy import deepcopy
from typing import List, Dict, Optional

from src.geni.models import TrackTuple, AlbumTuple, ArtistTuple
from src.spot.utils import SpotUtils


class GenUtils:

    @staticmethod
    def tuplify_tracks(track_dicts: List[Dict], album: AlbumTuple) -> List[TrackTuple]:
        return [GenUtils.tuplify_track(track_dict["song"], album) for track_dict in track_dicts]

    @staticmethod
    def tuplify_track(d: Dict, album: AlbumTuple) -> Optional[TrackTuple]:
        try:
            _track = GenUtils.extract_track(d, album)
        except Exception as e:
            print(f"Unable to tuplify track")
            print(d)
            traceback.print_tb(e.__traceback__)
            return None
        else:
            return _track

    @staticmethod
    def extract_track(track_dict: Dict, album: AlbumTuple):
        return TrackTuple(
            title=track_dict["title"],
            url=track_dict["url"],
            album=album,
            primary_artists=[GenUtils.extract_artist(track_dict["primary_artist"])],
            featured_artists=[GenUtils.extract_artist(feat) for feat in track_dict["featured_artists"]]
        )

    @staticmethod
    def extract_artist(artist_dict: Dict) -> ArtistTuple:
        return ArtistTuple(
            name=artist_dict["name"],
            header_image_url=artist_dict["header_image_url"],
            url=["url"]
        )

    @staticmethod
    def extract_album_tracks(raw: Dict) -> List[TrackTuple]:
        _dict = deepcopy(raw)
        _album_dict = _dict["album"]
        _track_dicts = _dict["album_appearances"]
        _release_date_string = _album_dict["release_date"]
        _release_date = SpotUtils.clean_up_date(_release_date_string)
        _artist_dict = _album_dict["artist"]
        try:
            _album_tuple = AlbumTuple(
                name=_album_dict["name"],
                release_date_string=_release_date_string,
                release_date=_release_date,
                header_image_url=_album_dict["header_image_url"],
                url=_album_dict["url"],
                artist=GenUtils.extract_artist(_artist_dict)
            )
        except Exception as e:
            print(f"Exception when trying to extract album")
            print(raw)
            traceback.print_tb(e.__traceback__)
            raise
        else:
            return GenUtils.tuplify_tracks(_track_dicts, _album_tuple)

    @staticmethod
    def slugify(text: str) -> str:
        slug = text.strip().lower()
        slug = slug[1:] if slug[0] == "'" or slug[0] == "-" else slug
        slug = re.sub(r"ma\$e", "ma-e", slug)
        slug = re.sub(r"a\$ap", "a-ap", slug)
        slug = re.sub(r"curren\$y", "curren-y", slug)
        slug = re.sub(r"à", "a", slug)
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
        st = re.sub(r" \(screwed\)", "", st, re.IGNORECASE)
        st = re.sub(r" \(Screwed Version\)", "", st, re.IGNORECASE)
        st = re.sub(r" \(with.*?\)", "", st, re.IGNORECASE)
        st = re.sub(r" \(feat.*?\)", "", st, re.IGNORECASE)
        st = re.sub(r" \(Sky High\)", "", st, re.IGNORECASE)
        st = re.sub(r" \[feat.*?\]", "", st, re.IGNORECASE)
        st = re.sub(r" \[Prod\.? By.*?\]", "", st, re.IGNORECASE)
        st = re.sub(r" \[Bonus Track\]", "", st, re.IGNORECASE)
        st = re.sub(r" - feat.*?$", "", st, re.IGNORECASE)
        st = re.sub(r" - Vocal$", "", st, re.IGNORECASE)
        st = re.sub(r" feat\. .*?$", "", st, re.IGNORECASE)
        st = re.sub(r" - Dirty$", "", st, re.IGNORECASE)
        st = re.sub(r" - Edited$", "", st, re.IGNORECASE)
        st = re.sub(r" - Edit$", "", st, re.IGNORECASE)
        st = re.sub(r" - Radio$", "", st, re.IGNORECASE)
        st = re.sub(r" - LP Mix$", "", st, re.IGNORECASE)
        st = re.sub(r" - Explici?t$", "", st, re.IGNORECASE)
        st = re.sub(r"; Explicit version$", "", st, re.IGNORECASE)
        st = re.sub(r"; Explicit$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Version$", "", st, re.IGNORECASE)
        st = re.sub(r" - UNRATED$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Chopped$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Slowed$", "", st, re.IGNORECASE)
        st = re.sub(r" - .*?Screwed$", "", st, re.IGNORECASE)
        st = re.sub(r" \(Chopped&Screwed\).*?$", "", st, re.IGNORECASE)
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
        pruned = GenUtils.prune(song_title) if song_title.lower() != "intro" else GenUtils.prune(f"{song_title} ({album_title}) ")
        song_title = GenUtils.adjust_song_title(pruned)
        _slug = GenUtils.slugify(artist + " " + song_title + "-lyrics")
        slug = re.sub(r"[-]+", "-", _slug)
        return f"{h}://{g}.{c}/{slug.capitalize()}"

    @staticmethod
    def adjust_artist_name(name: str) -> str:
        _name = "Yasiin Bey" if name.lower() == "mos def" else name
        _name = "Rob Base and DJ E-Z Rock" if name == "Rob Base & DJ EZ Rock" else _name
        _name = "Just-Ice Rap" if name == "Just-Ice" else _name
        _name = "Treacherous Three" if name == "The Treacherous Three" else _name
        _name = "Dayton Family" if name == "The Dayton Family" else _name
        _name = "Sugarhill Gang" if name == "The Sugarhill Gang" else _name
        _name = "Masta Ace" if name.lower() == "masta ace incorporated" else _name
        _name = "2Pac" if name.lower() == "makaveli" else _name
        _name = _name[:-4] if _name.endswith(", The") else _name
        _name = _name[4:] if _name.startswith("The Egyptian") else _name
        return _name

    @staticmethod
    def adjust_song_title(song_title: str) -> str:
        title = song_title.replace("H-E", "Hoe")
        title = title.replace("H*es", "Hoes")
        title = title.replace("Mother ******", "Mother Fucker")
        title = title.replace("N____", "Nigga")
        title = title.replace("N****", "Nigga")
        title = title.replace("N***a", "Nigga")
        title = title.replace("N!@@a", "Nigga")
        title = title.replace("N!$$@", "Nigga")
        title = title.replace("N*gga", "Nigga")
        title = title.replace("N**ga", "Nigga")
        title = title.replace("N**gas", "Niggas")
        title = title.replace("N*ggas", "Niggas")
        title = title.replace("Ni---z", "Niggaz")
        title = title.replace("Ni**azz", "Niggaz")
        title = title.replace("N**gaz", "Niggaz")
        title = title.replace("N***az", "Niggaz")
        title = title.replace("N*****", "Niggas")
        title = title.replace("F*ck", "Fuck")
        title = title.replace("F#ck", "Fuck")
        title = title.replace("F**k", "Fuck")
        title = title.replace("F***", "Fuck")
        title = title.replace("F------", "Fucking")
        title = title.replace("F--k", "Fuck")
        title = title.replace("F---", "Fuck")
        title = title.replace("D**n", "Damn")
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
        title = title.replace("B*tch", "Bitch")
        title = title.replace("B-t-h", "Bitch")
        title = title.replace("B*tches", "Bitches")
        title = title.replace("B****es", "Bitches")
        title = title.replace("Bullsh--", "Bullshit")
        title = title.replace("P*ssy", "Pussy")
        title = title.replace("P****", "Pussy")
        title = title.replace("P***y", "Pussy")
        title = title.replace("Bulls**t", "Bullshit")
        title = title.replace("Sh*t", "Shit")
        title = title.replace("S**t", "Shit")
        title = title.replace("Sh!t", "Shit")
        title = title.replace("Sh--", "Shit")
        title = title.replace("S...", "Shit")
        title = title.replace("S***", "Shit")
        title = title.replace("Sh**", "Shit")
        title = title.replace("Muthaf*cka", "Muthafucka")
        title = title.replace("Mutherf-----", "Mutherfucker")
        title = title.replace("#!*@", "Fuck")
        title = title.replace("****", "Fuck")

        return title
