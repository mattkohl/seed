import ast
from . import artists
from app.bus import Producer, Consumer


class MBConsumer(Consumer):

    mba = artists.MBArtist()

    def __init__(self, topic: str, kp: Producer):
        Consumer.__init__(self, topic)
        self.producer = kp

    def run(self):
        for msg in self.queue:
            track = ast.literal_eval(msg.value.decode('utf-8'))
            artist = track["artists"][0]["name"]
            results = self.mba.search(artist)
            if results and results[0]["ext:score"] == "100":
                mb_id = results[0]["id"]
                track.update({"mbId": mb_id})
                self.producer.publish_message(self.producer.connect(), "mb", "hh", str(track))
