import ast
from app.bus import Producer, Consumer
from app.models import Artist, db
from app.persist.utils import PersistUtils
from app import create_app


class PersistArtistConsumer(Consumer):

    def __init__(self, topic: str, kp: Producer):
        Consumer.__init__(self, topic)
        self.producer = kp

    def run(self):
        for msg in self.queue:
            artist_json = ast.literal_eval(msg.value.decode('utf-8'))
            name, uri = artist_json["name"], artist_json["uri"]
            try:
                current = create_app('docker')
                with current.app_context():
                    a = PersistUtils.get_or_create(db.session, Artist, name=name, spot_uri=uri)
                    self.producer.publish_message(self.producer.connect(), "persisted", "hh", str(a))
            except Exception as e:
                print(str(e))
