import traceback
from typing import Optional, List, Tuple
import re
from bs4 import BeautifulSoup
import requests


from src.geni import utils
from src.geni.models import SectionTuple


class GenParser:

    heading_regex = re.compile(
        r"\[(?P<block_type>[\w-]+)\s?(?P<block_num>\d?\d?):?\s?(?P<artists>.*?)\]\n+(?P<text>(?:[^\n\[\]]+\n\n?\n??)+)",
        flags=re.MULTILINE
    )

    @staticmethod
    def download(urls: List[str]) -> Tuple[Optional[str], str]:
        assert len(urls) > 0
        url = urls.pop()
        lyrics = None
        try:
            page = requests.get(url)
            lyrics = GenParser.extract_lyrics_text(page)
        except Exception as e:
            print(f"Lyric extraction error: {e}")
            if len(urls) >= 1:
                GenParser.download(urls)
            else:
                traceback.print_tb(e.__traceback__)
                return None, url
        return GenParser.clean(lyrics), url

    @staticmethod
    def clean(lyrics: str) -> str:
        lyrics = lyrics.replace("‘", "'")
        return lyrics

    @staticmethod
    def extract_lyrics_text(page: requests.Response) -> str:
        try:
            html = BeautifulSoup(page.text, "html.parser")
            lyrics = html.find("div", class_="lyrics").get_text()
        except Exception as e:
            print(f"No lyrics found at {page.url}")
            raise
        else:
            return lyrics

    @staticmethod
    def extract_sections(text: str) -> List[SectionTuple]:
        return [GenParser.extract_section(match) for match in GenParser.heading_regex.finditer(text)]

    @staticmethod
    def extract_section(match) -> SectionTuple:
        return SectionTuple(
            type=match.group("block_type") if match.group("block_type") else None,
            number=int(match.group("block_num")) if match.group("block_num") else None,
            artists=match.group("artists") if match.group("artists") else None,
            offset=match.start(),
            text=match.group("text").strip() if match.group("text").strip() else None
        )

    @staticmethod
    def build_urls(_track):
        _artists = _track.primary_artists if len(_track.primary_artists) > 0 else _track.featured_artists
        if len(_artists) == 2:
            url1 = utils.GenUtils.link([_artist.name for _artist in _artists], _track.name, _track.album.name)
            url2 = utils.GenUtils.link([_artist.name for _artist in _artists[:1]], _track.name, _track.album.name)
            return [url1, url2]
        else:
            return [utils.GenUtils.link([_artist.name for _artist in _artists], _track.name, _track.album.name)]
