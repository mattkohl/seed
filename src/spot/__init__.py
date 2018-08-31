import random
from kafka import KafkaConsumer
from src.bus import Producer
from src.geni.parser import GenParser
from src.spot.playlists import SpotPlaylist


class Consumer:

    queue = KafkaConsumer("playlist",
                          auto_offset_reset='earliest',
                          bootstrap_servers=['localhost:9092'],
                          api_version=(0, 10),
                          consumer_timeout_ms=1000)


if __name__ == "__main__":

    sp = SpotPlaylist()
    kc = Consumer()
    gp = GenParser()
    kp = Producer()
    producer = kp.connect()

    for msg in kc.queue:
        uri = msg.value.value.decode('utf-8')
        tracks = sp.extract_tracks(uri)
        track = random.choice(tracks)
        kp.publish_message(producer, "track", "hh", str(track))
