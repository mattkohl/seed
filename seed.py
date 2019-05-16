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


@application.route("/artists")
def artists():
    return jsonify(Fetch.artists())


@application.route("/artists/<uri>")
def artist(uri):
    return jsonify(Fetch.artist(uri))


@application.route("/artists/<uri>/albums")
def get_artist_albums(uri):
    return jsonify(Tasks.run_artist_albums(uri))


@application.route("/albums")
def albums():
    return jsonify(Fetch.albums())


@application.route("/albums/<uri>")
def album(uri):
    return jsonify(Fetch.album(uri))


@application.route("/albums/<uri>/tracks")
def album_tracks(uri):
    return jsonify(Tasks.run_album_tracks(uri))


@application.route("/tracks")
def tracks():
    return jsonify(Fetch.tracks())


@application.route("/tracks/<uri>")
def track(uri):
    return jsonify(Fetch.track(uri))


@application.route("/clear")
def clear() -> str:
    return jsonify(Persistence.clear())


@application.route("/playlists/<playlist_uri>")
def get_playlist(playlist_uri: str):
    return jsonify(Tasks.run_playlist(playlist_uri))


@application.route("/tracks/<track_uri>/lyrics")
def get_lyrics(track_uri):
    update = request.args.get('update', default=False)
    return jsonify(Fetch.track_lyrics(track_uri, update))


@application.route("/tracks/<uri>/lyrics/annotate")
def annotate(uri):
    return jsonify(Fetch.lyrics_annotate(uri))


@application.route("/tracks/<uri>/lyrics/annotations")
def annotations(uri):
    return Response(Fetch.lyrics_annotations(uri))


@application.route("/tracks/<uri>/links")
def get_lyric_links(uri):
    return jsonify(Fetch.lyric_links(uri))


@application.route("/dbp_annotate/<uri>")
def dbp_annotate(uri):
    return jsonify(Fetch.artist_and_track_name_annotations(uri))


@application.route("/artists/<spot_uri>/dbp")
def get_artist_dbp_uri(spot_uri):
    update = request.args.get('update', default=False)
    return jsonify(Fetch.artist_dbp_uri(spot_uri, update))


@application.route("/albums/<spot_uri>/dbp")
def get_album_dbp_uri(spot_uri):
    update = request.args.get('update', default=False)
    return jsonify(Fetch.album_dbp_uri(spot_uri, update))


@application.route("/tracks/<spot_uri>/dbp")
def get_track_dbp_uri(spot_uri):
    update = request.args.get('update', default=False)
    return jsonify(Fetch.track_dbp_uri(spot_uri, update))


@application.route("/artists/<uri>/mb")
def get_mb_metadata(uri):
    return jsonify(Fetch.artist_mb_metadata(uri))
