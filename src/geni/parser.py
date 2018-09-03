from bs4 import BeautifulSoup
import requests


class GenParser:

    @staticmethod
    def download(url) -> str:
        try:
            page = requests.get(url)
            html = BeautifulSoup(page.text, "html.parser")
            lyrics = html.find("div", class_="lyrics").get_text()
        except Exception as e:
            print(e)
        else:
            return lyrics

