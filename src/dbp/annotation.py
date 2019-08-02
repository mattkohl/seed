import traceback
import requests

from src.dbp.models import AnnotationTuple, CandidatesTuple
from src.dbp.utils import DbpUtils
from src.utils import Utils

TYPE_WHITELIST = ", ".join(
    [
        "DBpedia:Band",
        "DBpedia:Place",
        "DBpedia:Artist",
        "DBpedia:Person",
        "DBpedia:Company"
    ]
)


class Spotlight:

    @staticmethod
    def annotate(text) -> AnnotationTuple:
        url = "https://api.dbpedia-spotlight.org/en/annotate"
        try:
            params = {"text": text, "types": TYPE_WHITELIST}
            response = requests.get(url=url, params=params)
            assert response.status_code == 200
            cleaned = DbpUtils.strip_html(response.text)
            done = AnnotationTuple(cleaned)
        except Exception as e:
            print(f"Unable to resolve DBP Spotlight {url}")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            return done

    @staticmethod
    def candidates(text) -> CandidatesTuple:
        url = "https://api.dbpedia-spotlight.org/en/annotate"
        try:
            params = {"text": text}
            response = requests.get(url=url, params=params, headers={"accept": "application/json"})
            assert response.status_code == 200
            done = CandidatesTuple(**{Utils.clean_key(k): v for k, v in response.json().items()})
        except Exception as e:
            print(f"Unable to resolve DBP Spotlight {url}")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            return done


