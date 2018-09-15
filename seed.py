import os
from kafka.errors import KafkaError
import app.geni
import app.spot
import app.bus
from app import create_app


application = create_app(os.getenv('FLASK_CONFIG') or 'default')


kp = app.bus.Producer()
producer = kp.connect()

tasks = [
    app.geni.GenConsumer("track", kp),
    app.spot.SpotConsumer("playlist", kp)
]

for t in tasks:
    t.start()


@application.route("/")
def index() -> str:
    return "Index"


@application.route("/go/<playlist_uri>")
def go(playlist_uri) -> str:
    try:
        kp.publish_message(producer, "playlist", "hh", playlist_uri)
    except KafkaError as e:
        application.logger.error(str(e))
        return str(e)
    return playlist_uri
