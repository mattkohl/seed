import os

from flask import jsonify, Response
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import Artist, Album, Track
from app.tasks.pipeline import Tasks
from app.tasks.fetch import Fetch

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
    results = [_artist.as_dict() for _artist in Artist.query.all()]
    return jsonify(results)


@application.route("/artists/<uri>")
def artist(uri):
    try:
        result = Artist.query.filter_by(spot_uri=uri).first()
        _artist = result.as_dict()
        _albums = [_album.as_dict() for _album in result.albums]
        _artist.update({"albums": _albums})
        return jsonify(_artist)
    except Exception as e:
        print(e)
        return jsonify(dict())


@application.route("/artists/<uri>/albums")
def get_artist_albums(uri):
    try:
        _albums = Tasks.run_artist_albums(uri)
    except Exception:
        raise
    else:
        return jsonify(_albums)


@application.route("/albums")
def albums():
    results = [_album.as_dict() for _album in Album.query.all()]
    return jsonify(results)


@application.route("/albums/<uri>")
def album(uri):
    result = Album.query.filter_by(spot_uri=uri).first()
    _album = result.as_dict()
    _artists = [_artist.as_dict() for _artist in result.artists]
    _tracks = [_track.as_dict() for _track in result.tracks]
    _album.update({"tracks": _tracks, "artists": _artists})
    return jsonify(_album)


@application.route("/albums/<uri>/tracks")
def album_tracks(uri):
    return jsonify(Tasks.run_album_tracks(uri))


@application.route("/tracks")
def tracks():
    results = [_track.as_dict() for _track in Track.query.all()]
    return jsonify(results)


@application.route("/tracks/<uri>")
def track(uri):
    result = Track.query.filter_by(spot_uri=uri).first()
    _track = result.as_dict()
    _artists = [_artist.as_dict() for _artist in result.artists]
    _album = result.album.as_dict()
    _track.update({"album": _album, "artists": _artists})
    return jsonify(_track)


@application.route("/clear")
def clear() -> str:
    message = f"Deleted {Track.query.count()} Tracks, {Artist.query.count()} Artists, & {Album.query.count()} Albums"
    Track.query.delete()
    Artist.query.delete()
    Album.query.delete()
    db.session.commit()
    return message


@application.route("/playlists/<playlist_uri>")
def get_playlist(playlist_uri: str):
    return jsonify(Tasks.run_playlist(playlist_uri))


@application.route("/scrape")
def scrape_lyrics():
    return jsonify(Tasks.scrape_all_lyrics())


@application.route("/tracks/<track_uri>/lyrics")
def scrape_lyric(track_uri):
    return jsonify(Fetch.track_lyrics(track_uri))


@application.route("/tracks/<uri>/annotate")
def annotate(uri):
    return jsonify(Fetch.lyric_annotations(uri))


@application.route("/tracks/<uri>/annotations")
def annotations(uri):
    _track = Track.query.filter_by(spot_uri=uri).first()
    return Response(_track.lyrics_annotated)


@application.route("/tracks/<uri>/links")
def get_lyric_links(uri):
    return jsonify(Fetch.lyric_links(uri))


@application.route("/dbp_annotate/<uri>")
def dbp_annotate(uri):
    candidates = Fetch.artist_and_track_name_annotations(uri)
    if candidates is not None:
        return jsonify(candidates._asdict())
    else:
        return jsonify({"Error": "no candidates found"})


@application.route("/artists/<spot_uri>/dbp")
def get_artist_dbp_uri(spot_uri):
    return jsonify(Fetch.artist_dbp_uri(spot_uri))


@application.route("/artists/<uri>/mb")
def get_mb_metadata(uri):
    return jsonify(Fetch.artist_mb_metadata(uri))
