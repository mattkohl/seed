import re


class DbpUtils:

    @staticmethod
    def strip_html(annotated: str):
        formatted = annotated.replace("DBpedia Spotlight annotation", "").replace("<br/>", "\n")
        return re.sub("<(?!\/?a(?=>|\s.*>))\/?.*?>", "", formatted).strip()
