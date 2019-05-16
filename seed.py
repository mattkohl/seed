import os

from flask import jsonify, Response, request
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.tasks.persist import Persistence
from app.tasks.pipeline import Tasks
from app.tasks.fetch import Fetch

application = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(application, db)


@application.cli.command()
def deploy() -> None:
    upgrade()


@application.route("/")
def index():
    return jsonify({"service": "Seed API", "version": 0.1})


@application.route("/albums")
def albums():
    return jsonify(Fetch.albums())


@application.route("/albums/<uri>")
def album(uri):
    return jsonify(Fetch.album(uri))


@application.route("/albums/<uri>/run")
def album_run(uri):
    return jsonify(Tasks.run_album(uri))


@application.route("/artists")
def artists():
    return jsonify(Fetch.artists())


@application.route("/artists/<uri>")
def artist(uri):
    return jsonify(Fetch.artist(uri))


@application.route("/artists/<uri>/run")
def artist_run(uri):
    return jsonify(Tasks.run_artist(uri))


@application.route("/clear")
def clear() -> str:
    return jsonify(Persistence.clear())


@application.route("/playlists/<playlist_uri>")
def get_playlist(playlist_uri: str):
    return jsonify(Tasks.run_playlist(playlist_uri))


@application.route("/tracks")
def tracks():
    return jsonify(Fetch.tracks())


@application.route("/tracks/<uri>")
def track(uri):
    return jsonify(Fetch.track(uri))


@application.route("/tracks/<uri>/run")
def track_run(uri):
    return jsonify(Tasks.run_track(uri))


@application.route("/tracks/<track_uri>/lyrics")
def track_lyrics(track_uri):
    update = request.args.get('update', default=False)
    return jsonify(Fetch.track_lyrics(track_uri, update))


@application.route("/tracks/<uri>/lyrics/annotations")
def track_lyrics_annotations(uri):
    return Response(Fetch.lyrics_annotations(uri))


@application.route("/tracks/<uri>/links")
def track_lyrics_links(uri):
    return jsonify(Fetch.lyric_links(uri))
