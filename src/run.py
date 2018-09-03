import random
from pprint import pprint
from src.spot.playlists import SpotPlaylist
from src.geni.utils import GenUtils
from src.geni.parser import GenParser
from src.bus import Producer


def main() -> None:
    sp = SpotPlaylist()
    gp = GenParser()
    kp = Producer()
    producer = kp.connect()

    test_uri = "spotify:user:matt.kohl-gb:playlist:2d1Q2cY735lRoXC8cC6DDJ"
    kp.publish_message(producer, "playlist", "hh", test_uri)

    tracks = sp.extract_tracks(test_uri)
    track = random.choice(tracks)
    artist, song_title = track["artists"][0]["name"], track["title"]
    test_url = GenUtils.link(artist, song_title)
    lyrics = gp.download(test_url)
    if lyrics is not None:
        track.update({"genUrl": test_url, "lyrics": lyrics})
        pprint(track)
        kp.publish_message(producer, "lyrics", "hh", str(track))


if __name__ == "__main__":
    main()
