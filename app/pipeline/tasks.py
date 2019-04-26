import json

from app.spot.consumer import PlaylistConsumer
from app.persist.persist import Persist


class Tasks:

    @staticmethod
    def playlist(uri: str):
        for result in PlaylistConsumer.run(uri):
            Persist.persist_song(result)
            yield json.dumps(result)
