import json

from app.spot.consumer import PlaylistConsumer
from app.persist.persist import Persist


class Tasks:

    @staticmethod
    def playlist(uri: str):
        for result in PlaylistConsumer.run(uri):
            persisted = Persist.persist_song(result)
            f"PERSISTED: {persisted}"
            yield json.dumps(result)
