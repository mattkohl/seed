import re


class DbpUtils:

    dbp_uri = re.compile(r"""<a about="(?P<uri>http://dbpedia\.org/resource/.*?)" typeof="http://dbpedia\.org/ontology/Agent" href="http://dbpedia\.org/resource/.*?" title="http://dbpedia\.org/resource/.*?">(?P<label>.*?)</a>""")

    @staticmethod
    def strip_html(annotated: str):
        formatted = annotated.replace("DBpedia Spotlight annotation", "").replace("<br/>", "\n")
        return re.sub("<(?!\/?a(?=>|\s.*>))\/?.*?>", "", formatted).strip()
