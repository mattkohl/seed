from typing import List

from src import db


class TaskUtils:

    @staticmethod
    def just_names_and_uris(results: List[db.Model]):
        return [{"name": result.name, "uri": result.spot_uri} for result in results]
