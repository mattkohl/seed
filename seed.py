import json
import os

from flask import Response
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import Artist, Album, Song
from app.persist.utils import AlchemyEncoder
from app.pipeline.tasks import Tasks

application = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(application, db)


@application.cli.command()
def deploy():
    upgrade()


@application.route("/")
def index() -> str:
    return "Index"


@application.route("/artists")
def artists():
    results = Artist.query.all()
    return Response(response=json.dumps(results, cls=AlchemyEncoder), content_type='application/json')


@application.route("/albums")
def albums():
    results = Album.query.all()
    return Response(response=json.dumps(results, cls=AlchemyEncoder), content_type='application/json')


@application.route("/songs")
def songs():
    results = Song.query.all()
    return Response(response=json.dumps(results, cls=AlchemyEncoder), content_type='application/json')


@application.route("/clear")
def clear() -> str:
    song_count = Song.query.count()
    artist_count = Artist.query.count()
    album_count = Album.query.count()
    message = f"Deleted {song_count} Songs, {artist_count} Artists, & {album_count} Albums"
    Song.query.delete()
    Artist.query.delete()
    Album.query.delete()
    db.session.commit()
    return message


@application.route("/clear/artists")
def clear_artists() -> str:
    artist_count = Artist.query.count()
    message = f"Deleted {artist_count} Artists"
    Artist.query.delete()
    db.session.commit()
    return message


@application.route("/go/<playlist_uri>")
def go(playlist_uri: str):
    return Response(Tasks.playlist(playlist_uri), content_type='application/json')