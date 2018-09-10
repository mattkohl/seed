import os
import logging
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

import sys
import click

from flask import Flask
from kafka.errors import KafkaError

from geni import GenConsumer
from spot import SpotConsumer
from bus import Producer

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

handler = RotatingFileHandler('flask.log', maxBytes=10000, backupCount=1)
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
