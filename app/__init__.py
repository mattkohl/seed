from flask import Flask

from app.geni import GenConsumer
from app.spot import SpotConsumer
from app.bus import Producer


application = Flask(__name__)
kp = Producer()
producer = kp.connect()

tasks = [
    GenConsumer("track", kp),
    SpotConsumer("playlist", kp)
]

for t in tasks:
    t.start()


@application.route("/", methods=["GET"])
def index():
    return "Index"


@application.route("/go/<playlist_uri>", methods=["GET"])
def go(playlist_uri) -> None:
    # test_uri = "spotify:user:matt.kohl-gb:playlist:2d1Q2cY735lRoXC8cC6DDJ"
    kp.publish_message(producer, "playlist", "hh", playlist_uri)
    return playlist_uri


if __name__ == "__main__":
    application.run(host="0.0.0.0", port="5001")
