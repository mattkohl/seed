import os

from dotenv import load_dotenv
from flask import Flask
from kafka.errors import KafkaError
from geni import GenConsumer
from spot import SpotConsumer
from bus import Producer

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

application = Flask(__name__)


kp = Producer()
producer = kp.connect()

tasks = [
    GenConsumer("track", kp),
    SpotConsumer("playlist", kp)
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
