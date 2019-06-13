from typing import Optional, List
import re
from bs4 import BeautifulSoup
import requests

from src.geni.models import SectionTuple


class GenParser:

    heading_regex = re.compile(
        r"\[(?P<block_type>[\w-]+)\s?(?P<block_num>\d?\d?):?\s?(?P<artists>.*?)\]\n\n?(?P<text>(.+\n)+)",
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
