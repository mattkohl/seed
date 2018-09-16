import ast
import time
from . import utils
from . import parser
from app.bus import Producer, Consumer


class GenConsumer(Consumer):

    def __init__(self, topic: str, kp: Producer):
        Consumer.__init__(self, topic)
        self.producer = kp

    def run(self) -> None:
        for msg in self.queue:
            track = ast.literal_eval(msg.value.decode('utf-8'))
            artist, song_title = track["artists"][0]["name"], track["title"]
            url = utils.GenUtils.link(artist, song_title)
            lyrics = parser.GenParser.download(url)
            if lyrics:
                track.update({"genUrl": url, "lyrics": lyrics})
                self.producer.publish_message(self.producer.connect(), "lyrics", "hh", str(track))
            else:
                self.producer.publish_message(self.producer.connect(), "failedLyrics", "hh", url)
            time.sleep(2)