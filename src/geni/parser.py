from typing import Optional, List, Tuple, Dict
import re
import json
from bs4 import BeautifulSoup
import requests

from src.geni import utils
from src.geni.models import SectionTuple, TrackTuple


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
            raw = GenParser.extract_lyrics_text(page)
            lyrics = GenParser.clean(raw)
        except Exception as e:
            print(f"Lyric extraction error: {e}")
            if len(urls) >= 1:
                return GenParser.download(urls)
            else:
                return None, url
        return lyrics, url

    @staticmethod
    def clean(lyrics: str) -> str:
        lyrics = lyrics.replace("‘", "'")
        return lyrics

    @staticmethod
    def extract_lyrics_text(page: requests.Response) -> str:
        html = BeautifulSoup(page.text, "html.parser")
        try:
            lyrics = html.find("div", class_="lyrics").get_text()
            if lyrics is None:
                lyrics = html.select_one('div[class*="Lyrics__Container-"]').get_text()
        except Exception as e:
            print(f"No lyrics found at {page.url}")
            print(html)
            raise e
        else:
            return lyrics

    @staticmethod
    def extract_album_tracks(page: requests.Response) -> List[TrackTuple]:
        html = BeautifulSoup(page.text, 'html.parser')
        content = html.find(content=re.compile("quot"))["content"]
        _dict = json.loads(content)
        return utils.GenUtils.extract_album_tracks(_dict)

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

        def adjust(_urls: List[str]) -> List[str]:
            adjusted = []
            for url in _urls:
                if "joey-badass" in url.lower():
                    adjusted.append(url.replace("badass", "bada"))
                adjusted.append(url)
            return adjusted

        def remove_various_artists(xs):
            return list(filter(lambda x: x.name.lower() != "various artists", xs))

        _artists = remove_various_artists(_track.album.artists)

        for a in _track.primary_artists:
            if a.name.lower() != "various artists"and a not in _artists:
                _artists.append(a)
        if len(_artists) == 0:
            _artists = remove_various_artists(_track.featured_artists)

        if len(_artists) == 2:
            url1 = utils.GenUtils.link([_artist.name for _artist in _artists], _track.name, _track.album.name)
            url2 = utils.GenUtils.link([_artist.name for _artist in _artists[::-1]], _track.name, _track.album.name)
            url3 = utils.GenUtils.link([_artist.name for _artist in _artists[:1]], _track.name, _track.album.name)
            url4 = utils.GenUtils.link([_artist.name for _artist in _artists[1:2]], _track.name, _track.album.name)
            urls = adjust([url2, url1, url4, url3])
        else:
            urls = adjust([utils.GenUtils.link([_artist.name for _artist in _artists], _track.name, _track.album.name)])
        return urls
