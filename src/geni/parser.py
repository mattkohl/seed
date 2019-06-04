from typing import Optional, List

from bs4 import BeautifulSoup
import requests

from src.geni.models import VerseTuple
from src.geni.utils import GenUtils


class GenParser:

    @staticmethod
    def download(url) -> Optional[str]:
        try:
            page = requests.get(url)
            html = BeautifulSoup(page.text, "html.parser")
            lyrics = html.find("div", class_="lyrics").get_text()
        except Exception as e:
            print(f"Nothing found at {url}: {e}")
            return None
        else:
            return lyrics

    @staticmethod
    def extract_verses(text: str) -> List[VerseTuple]:
        return GenUtils.heading_regex.findall(text)

