from typing import Dict

from . import artists


class MBConsumer:

    @staticmethod
    def run(track: Dict) -> Dict:
        artist = track["artists"][0]["name"]
        results = artists.MBArtist().search(artist)
        if results and results[0]["ext:score"] == "100":
            mb_id = results[0]["id"]
            track.update({"mbId": mb_id})
        return track
