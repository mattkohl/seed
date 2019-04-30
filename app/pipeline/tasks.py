from flask import json

from app.spot.consumer import PlaylistConsumer
from app.persist.persist import Persist


class Tasks:

    @staticmethod
    def extract_tracks_from_playlist(uri: str):
        for result in PlaylistConsumer.run(uri):
            Persist.persist_song(result)
            _album = result.album._asdict()
            _artists = [_artist._asdict() for _artist in result.artists]
            _updated = result._replace(artists=_artists, album=_album)
            yield json.dumps(_updated._asdict(), indent=2, separators=(', ', ': '))
