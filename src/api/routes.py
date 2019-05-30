from flask import jsonify, request, url_for, Response
from werkzeug.utils import redirect

from src.api import api
from src.tasks.fetch import Fetch
from src.tasks.persist import Persistence
from src.tasks.pipeline import Tasks


@api.route("/")
def index():
    return jsonify({"service": "Seed API", "version": 0.1})


@api.route("/albums")
def albums():
    name_filter = request.args.get('filter', default=None)
    fetched = Fetch.albums(name_filter)
    if len(fetched) == 1:
        return redirect(url_for("api.album", uri=fetched[0]["spot_uri"]))
    return jsonify(fetched)


@api.route("/albums/<uri>")
def album(uri):
    return jsonify(Fetch.album(uri))


@api.route("/albums/<uri>/run")
def album_run(uri):
    return jsonify(Tasks.run_album(uri))


@api.route("/artists")
def artists():
    name_filter = request.args.get('filter', default=None)
    fetched = Fetch.artists(name_filter)
    if len(fetched) == 1:
        return redirect(url_for("api.artist", uri=fetched[0]["spot_uri"]))
    return jsonify(fetched)


@api.route("/artists/<uri>")
def artist(uri):
    return jsonify(Fetch.artist(uri))


@api.route("/artists/<uri>/hometown")
def artist_hometown(uri):
    return jsonify(Fetch.artist_hometown(uri))


@api.route("/artists/<uri>/hometown/delete")
def artist_hometown_delete(uri):
    return jsonify(Persistence.delete_artist_hometown(uri))


@api.route("/artists/<uri>/birthplace")
def artist_birthplace(uri):
    return jsonify(Fetch.artist_birthplace(uri))


@api.route("/artists/<uri>/birthplace/delete")
def artist_birthplace_delete(uri):
    return jsonify(Persistence.delete_artist_birthplace(uri))


@api.route("/artists/<uri>/run")
def artist_run(uri):
    return jsonify(Tasks.run_artist(uri))


@api.route("/clear")
def clear() -> str:
    return jsonify(Persistence.clear())


@api.route("/genres")
def genres():
    name_filter = request.args.get('filter', default=None)
    fetched = Fetch.genres(name_filter)
    if len(fetched) == 1:
        return redirect(url_for("api.genre", _id=fetched[0]["id"]))
    return jsonify(fetched)


@api.route("/genres/<_id>")
def genre(_id):
    return jsonify(Fetch.genre(_id))


@api.route("/locations")
def locations():
    name_filter = request.args.get('filter', default=None)
    fetched = Fetch.locations(name_filter)
    if len(fetched) == 1:
        return redirect(url_for("api.location", _id=fetched[0]["id"]))
    return jsonify(fetched)


@api.route("/locations/<_id>")
def location(_id):
    return jsonify(Fetch.location(_id))


@api.route("/playlists/<playlist_uri>/run")
def get_playlist(playlist_uri: str):
    return jsonify(Tasks.run_playlist(playlist_uri))


@api.route("/stats")
def stats():
    return jsonify(Fetch.stats())


@api.route("/tracks")
def tracks():
    name_filter = request.args.get('filter', default=None)
    fetched = Fetch.tracks(name_filter)
    if len(fetched) == 1:
        return redirect(url_for("api.track", uri=fetched[0]["spot_uri"]))
    return jsonify(fetched)


@api.route("/tracks/missing-lyrics")
def tracks_missing_lyrics():
    return jsonify(Fetch.tracks_missing_lyrics())


@api.route("/tracks/run/random")
def tracks_run_random():
    return jsonify(Tasks.run_random_track())


@api.route("/tracks/<uri>")
def track(uri):
    return jsonify(Fetch.track(uri))


@api.route("/tracks/<uri>/run")
def track_run(uri):
    return jsonify(Tasks.run_track(uri))


@api.route("/tracks/<track_uri>/lyrics")
def track_lyrics(track_uri):
    update = request.args.get('update', default=False)
    return jsonify(Fetch.track_lyrics(track_uri, update))


@api.route("/tracks/<uri>/lyrics/annotations")
def track_lyrics_annotations(uri):
    return Response(Fetch.track_lyrics_annotations(uri))


@api.route("/tracks/<uri>/links")
def track_lyrics_links(uri):
    return jsonify(Fetch.track_lyric_links(uri))


@api.route("/tracks/<uri>/mb")
def track_mb(uri):
    return jsonify(Fetch.track_mb_metadata(uri))