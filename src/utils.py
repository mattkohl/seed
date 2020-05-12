from typing import Dict
from fuzzywuzzy import fuzz
import datetime


class Utils:

    @staticmethod
    def clean_key(k: str) -> str:
        return k.replace("@", "").replace("-", "_").replace(":", "_")

    @staticmethod
    def fuzzy_match(a: str, b: str) -> float:
        return fuzz.token_sort_ratio(a, b)

    @staticmethod
    def format_dates(d: Dict) -> Dict:
        for k, v in d.items():
            if isinstance(v, datetime.datetime):
                d.update({k: v.strftime('%Y-%m-%d')})
        return d

    @staticmethod
    def move_definite_article_to_end(name: str) -> str:
        return name[4:] + ', The' if name.lower().startswith('the ') and len(name) > 4 else name
