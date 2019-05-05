from typing import Dict

from app.mb import artists


class MbConsumer:

    @staticmethod
    def run(track: Dict) -> Dict:
        _artists = track["artists"]
        for _artist in _artists:
            results = artists.MBArtist().search(_artist["name"])
            if results and results[0]["ext:score"] == "100":
                _artist.update(results[0])
        return track
