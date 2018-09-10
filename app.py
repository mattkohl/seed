import os
import logging
from logging import StreamHandler

from dotenv import load_dotenv
from flask import Flask
from kafka.errors import KafkaError
from geni import GenConsumer
from spot import SpotConsumer
from bus import Producer

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
log_formatter = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
handler = StreamHandler()
handler.formatter(logging.Formatter(log_formatter, '%m-%d %H:%M:%S'))
handler.setLevel(logging.INFO)

application = Flask(__name__)
application.logger.addHandler(handler)

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
