from typing import Optional

from bs4 import BeautifulSoup
import requests


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

