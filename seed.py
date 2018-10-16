import os
from kafka.errors import KafkaError
from flask_migrate import Migrate
import app.geni
import app.spot
import app.bus
import app.persist
from app.models import Artist
from app import create_app, db


application = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(application, db)


kp = app.bus.Producer()
producer = kp.connect()

tasks = [
    app.geni.GenConsumer("track", kp),
    app.spot.PlaylistConsumer("playlist", kp),
    # app.persist.PersistArtistConsumer("artist", kp)
]

for t in tasks:
    t.start()


@application.route("/")
def index() -> str:
    return "Index"


@application.route("/test/<name>")
def test(name: str) -> str:
    return name


@application.route("/artists")
def artists() -> str:
    results = Artist.query.all()
    return "\n".join(a for a in results)


@application.route("/go/<playlist_uri>")
def go(playlist_uri: str) -> str:
    try:
        kp.publish_message(producer, "playlist", "hh", playlist_uri)
    except KafkaError as e:
        application.logger.error(str(e))
        return str(e)
    return playlist_uri
