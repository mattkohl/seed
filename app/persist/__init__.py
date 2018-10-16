import ast
from app.bus import Producer, Consumer
from app.models import Artist, db


class PersistArtistConsumer(Consumer):

    def __init__(self, topic: str, kp: Producer):
        Consumer.__init__(self, topic)
        self.producer = kp

    def run(self):
        for msg in self.queue:
            artist_json = ast.literal_eval(msg.value.decode('utf-8'))
            name, uri = artist_json["name"], artist_json["uri"]
            artist = Artist(name=name, spot_uri=uri)
            try:
                db.session.add(artist)
                db.session.commit()
            except Exception as e:
                print(str(e))
            else:
                self.producer.publish_message(self.producer.connect(), "persisted", "hh", str(artist))
