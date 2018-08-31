import ast
from kafka import KafkaConsumer
from pprint import pprint
from src.geni.utils import GenUtils
from src.geni.parser import GenParser
from src.bus import Producer


class Consumer:

    queue = KafkaConsumer("track",
                          auto_offset_reset='earliest',
                          bootstrap_servers=['localhost:9092'],
                          api_version=(0, 10),
                          consumer_timeout_ms=1000)


if __name__ == "__main__":

    kc = Consumer()
    gp = GenParser()
    kp = Producer()
    producer = kp.connect()

    for msg in kc.queue:
        track = ast.literal_eval(msg.value.decode('utf-8'))
        artist, song_title = track["artists"][0]["name"], track["title"]
        test_url = GenUtils.link(artist, song_title)
        lyrics = gp.download(test_url)
        if lyrics is not None:
            track.update({"genUrl": test_url, "lyrics": lyrics})
            pprint(track)
            kp.publish_message(producer, "lyrics", "hh", str(track))
