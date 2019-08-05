from typing import Dict
from fuzzywuzzy import fuzz
import datetime


class Utils:

    @staticmethod
    def clean_key(k):
        return k.replace("@", "").replace("-", "_").replace(":", "_")

    @staticmethod
    def fuzzy_match(a: str, b: str):
        return fuzz.token_sort_ratio(a, b)

    @staticmethod
    def format_dates(d: Dict):
        for k, v in d.items():
            if isinstance(v, datetime.datetime):
                d.update({k: v.strftime('%Y-%m-%d')})
        return d
