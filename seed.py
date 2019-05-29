import os

from flask import jsonify, Response, request, redirect, url_for
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
    name_filter = request.args.get('filter', default=None)
    fetched = Fetch.albums(name_filter)
    if len(fetched) == 1:
        return redirect(url_for("album", uri=fetched[0]["spot_uri"]))
    return jsonify(fetched)


@application.route("/albums/<uri>")
def album(uri):
    return jsonify(Fetch.album(uri))


@application.route("/albums/<uri>/run")
def album_run(uri):
    return jsonify(Tasks.run_album(uri))


@application.route("/artists")
def artists():
    name_filter = request.args.get('filter', default=None)
    fetched = Fetch.artists(name_filter)
    if len(fetched) == 1:
        return redirect(url_for("artist", uri=fetched[0]["spot_uri"]))
    return jsonify(fetched)


@application.route("/artists/<uri>")
def artist(uri):
    return jsonify(Fetch.artist(uri))


@application.route("/artists/<uri>/hometown")
def artist_hometown(uri):
    return jsonify(Fetch.artist_hometown(uri))


@application.route("/artists/<uri>/hometown/delete")
def artist_hometown_delete(uri):
    return jsonify(Persistence.delete_artist_hometown(uri))


@application.route("/artists/<uri>/birthplace")
def artist_birthplace(uri):
    return jsonify(Fetch.artist_birthplace(uri))


@application.route("/artists/<uri>/birthplace/delete")
def artist_birthplace_delete(uri):
    return jsonify(Persistence.delete_artist_birthplace(uri))


@application.route("/artists/<uri>/run")
def artist_run(uri):
    return jsonify(Tasks.run_artist(uri))


@application.route("/clear")
def clear() -> str:
    return jsonify(Persistence.clear())


@application.route("/genres")
def genres():
    name_filter = request.args.get('filter', default=None)
    fetched = Fetch.genres(name_filter)
    if len(fetched) == 1:
        return redirect(url_for("genre", _id=fetched[0]["id"]))
    return jsonify(fetched)


@application.route("/genres/<_id>")
def genre(_id):
    return jsonify(Fetch.genre(_id))


@application.route("/locations")
def locations():
    name_filter = request.args.get('filter', default=None)
    fetched = Fetch.locations(name_filter)
    if len(fetched) == 1:
        return redirect(url_for("location", _id=fetched[0]["id"]))
    return jsonify(fetched)


@application.route("/locations/<_id>")
def location(_id):
    return jsonify(Fetch.location(_id))


@application.route("/playlists/<playlist_uri>")
def get_playlist(playlist_uri: str):
    return jsonify(Tasks.run_playlist(playlist_uri))


@application.route("/stats")
def stats():
    return jsonify(Fetch.stats())


@application.route("/tracks")
def tracks():
    name_filter = request.args.get('filter', default=None)
    fetched = Fetch.tracks(name_filter)
    if len(fetched) == 1:
        return redirect(url_for("track", uri=fetched[0]["spot_uri"]))
    return jsonify(fetched)


@application.route("/tracks/run/random")
def track_run_random():
    return jsonify(Tasks.run_random_track())


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
    return Response(Fetch.track_lyrics_annotations(uri))


@application.route("/tracks/<uri>/links")
def track_lyrics_links(uri):
    return jsonify(Fetch.track_lyric_links(uri))


@application.route("/tracks/<uri>/lyrics/test")
def track_lyrics_test(uri):
    return jsonify(Fetch.track_lyrics_test(uri))


@application.route("/tracks/<uri>/mb")
def track_mb(uri):
    return jsonify(Fetch.track_mb_metadata(uri))
