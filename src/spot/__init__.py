import random
from src.bus import Producer, Consumer
from src.geni.parser import GenParser
from src.spot.playlists import SpotPlaylist


if __name__ == "__main__":

    sp = SpotPlaylist()
    kc = Consumer("playlist")
    gp = GenParser()
    kp = Producer()
    producer = kp.connect()

    for msg in kc.queue:
        uri = msg.value.value.decode('utf-8')
        tracks = sp.extract_tracks(uri)
        track = random.choice(tracks)
        kp.publish_message(producer, "track", "hh", str(track))
