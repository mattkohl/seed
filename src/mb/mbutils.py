from typing import Dict

from src.mb.genres import GENRES
from src.utils import Utils


class MbUtils:

    @staticmethod
    def add_genres(d: Dict) -> Dict:
        if 'tag_list' in d:
            _genres = [i["name"].replace(" ", "-").lower() for i in d['tag_list'] if i["name"] in GENRES]
            d.update({"genres": _genres})
        return d

    @staticmethod
    def cleaned(d) -> Dict:
        return {Utils.clean_key(k): v for k, v in d.items()}
