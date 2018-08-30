import random
from pprint import pprint
from src.spot.playlists import PlaylistGrabber
from src.geni.utils import GenUtils
from src.geni.parser import GenParser


def main():
    test_uri = "spotify:user:matt.kohl-gb:playlist:2d1Q2cY735lRoXC8cC6DDJ"
    pg = PlaylistGrabber()
    tracks = pg.extract_tracks(test_uri)
    track = random.choice(tracks)
    artist, song_title = track["artists"][0]["name"], track["title"]
    test_url = GenUtils.link(artist, song_title)
    pprint(track)
    print(test_url)
    gp = GenParser()
    lyrics = gp.download(test_url)
    print(lyrics)


if __name__ == "__main__":
    main()
