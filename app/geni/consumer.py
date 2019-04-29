from typing import Dict

from app.geni import utils, parser


class GenConsumer:

    @staticmethod
    def run(track: Dict) -> Dict:
        artist, song_title = track["artists"][0]["name"], track["title"]
        url = utils.GenUtils.link(artist, song_title)
        lyrics = parser.GenParser.download(url)
        if lyrics:
            track.update({"genUrl": url, "lyrics": lyrics})
        print(track)
        return track
