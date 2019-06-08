from typing import Optional, List
import re
from bs4 import BeautifulSoup
import requests

from src.geni.models import VerseTuple


class GenParser:

    dbp_uri = re.compile(r"""<a about="(?P<uri>http://dbpedia\.org/resource/.*?)" typeof="http://dbpedia\.org/ontology/Agent" href="http://dbpedia\.org/resource/.*?" title="http://dbpedia\.org/resource/.*?">(?P<label>.*?)</a>""")

    heading_regex = re.compile(
        r"\[(?P<block_type>[\w-]+)\s?(?P<block_num>\d?\d?):?\s?(?P<artists>.*?)\]\n(?P<text>(.+\n)+)",
        flags=re.MULTILINE
    )

    @staticmethod
    def download(url) -> Optional[str]:
        try:
            page = requests.get(url)
            html = BeautifulSoup(page.text, "html.parser")
            lyrics = html.find("div", class_="lyrics").get_text()
        except Exception as e:
            print(f"Nothing found at {url}: {e}")
            raise
        else:
            return lyrics

    @staticmethod
    def extract_verses(text: str) -> List[VerseTuple]:
        return [GenParser.extract_verse(match) for match in GenParser.heading_regex.finditer(text)]

    @staticmethod
    def extract_verse(match) -> VerseTuple:
        return VerseTuple(
            match.group("block_type") if match.group("block_type") else None,
            int(match.group("block_num")) if match.group("block_num") else None,
            match.group("artists") if match.group("artists") else None,
            match.start(),
            match.group("text").strip() if match.group("text").strip() else None
        )
