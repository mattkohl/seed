from typing import List

import spotlight


SERVER = "https://api.dbpedia-spotlight.org/en"


class SpotlightAnnotation:

    @staticmethod
    def annotate(text):
        return spotlight.annotate(SERVER, text)

    @staticmethod
    def annotate_artists(names: List[str]):
        template = f"""The hip-hop artists {", ".join(names)} recorded rap songs."""
        print(template)
        return spotlight.annotate(SERVER, template)

