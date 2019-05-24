from typing import Optional

from SPARQLWrapper import SPARQLWrapper2

from app.dbp.models import LocationTuple


class Sparql:

    @staticmethod
    def hometown(dbp_uri: str) -> Optional[LocationTuple]:
        query = Sparql.location_query("http://dbpedia.org/ontology/hometown").replace("?subject", f"<{dbp_uri}>")
        return Sparql.execute(query)

    @staticmethod
    def birthplace(dbp_uri: str) -> Optional[LocationTuple]:
        query = Sparql.location_query("http://dbpedia.org/ontology/birthPlace").replace("?subject", f"<{dbp_uri}>")
        return Sparql.execute(query)

    @staticmethod
    def location_query(predicate: str) -> str:
        return """
        SELECT DISTINCT ?uri ?label ?latitude ?longitude
        WHERE { 
            { ?subject ?predicate ?uri . }
            UNION
            { ?subject ?predicate ?_uri . ?_uri dbo:wikiPageRedirects ?uri . }
            ?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/Settlement> .
            ?uri <http://www.georss.org/georss/point> ?point .
            BIND(STRBEFORE(?point, " " ) as ?latitude)
            BIND(STRAFTER(?point, " " ) as ?longitude)            
            ?uri <http://www.w3.org/2000/01/rdf-schema#label> ?label .
            FILTER(LANG(?label) = "en")
        }
        """.replace("?predicate", f"<{predicate}>")

    @staticmethod
    def execute(query: str) -> Optional[LocationTuple]:
        endpoint = SPARQLWrapper2("http://dbpedia.org/sparql")
        endpoint.setQuery(query)
        results = endpoint.query()
        if results.bindings:
            return LocationTuple(**{v: b[v].value for v in results.variables for b in results.bindings if v in b})
        else:
            return None
