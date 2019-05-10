from fuzzywuzzy import fuzz


class Utils:

    @staticmethod
    def clean_key(k):
        return k.replace("@", "").replace("-", "_").replace(":", "_")

    @staticmethod
    def fuzzy_match(a: str, b: str) -> bool:
        return fuzz.token_sort_ratio(a, b) > 90
