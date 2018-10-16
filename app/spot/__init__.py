from app.bus import Producer, Consumer
from . import playlists


class PlaylistConsumer(Consumer):

    sp = playlists.SpotPlaylist()

    def __init__(self, topic: str, kp: Producer):
        Consumer.__init__(self, topic)
        self.producer = kp

    def run(self):
        for msg in self.queue:
            uri = msg.value.decode('utf-8')
            tracks = self.sp.extract_tracks(uri)
            for track in tracks:
                for artist in track["artists"]:
                    self.producer.publish_message(self.producer.connect(), "artist", "hh", str(artist))
                self.producer.publish_message(self.producer.connect(), "track", "hh", str(track))
