from typing import Dict


import requests
from requests import Response

from app.dbp.models import AnnotationTuple, CandidatesTuple
from app.utils import Utils

TYPE_WHITELIST = ", ".join(
    [
        "DBpedia:Band",
        "DBpedia:Place",
        "DBpedia:Artist",
        "DBpedia:Company"
    ]
)


class Spotlight:

    @staticmethod
    def annotate(text) -> Response:
        url = "https://api.dbpedia-spotlight.org/en/annotate"
        try:
            params = {"text": text, "types": TYPE_WHITELIST}
            response = requests.get(url=url, params=params)
        except Exception as e:
            print(f"Unable to resolve {url}: {e}")
        else:
            return AnnotationTuple(**{Utils.clean_key(k): v for k, v in response})

    @staticmethod
    def candidates(text) -> Dict:
        url = "https://api.dbpedia-spotlight.org/en/annotate"
        try:
            params = {"text": text, "types": TYPE_WHITELIST}
            response = requests.get(url=url, params=params, headers={"accept": "application/json"})
        except Exception as e:
            print(f"Unable to resolve {url}: {e}")
        else:
            return CandidatesTuple(**{Utils.clean_key(k): v for k, v in response.json()})
