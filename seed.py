import os

from flask import jsonify
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import Artist, Album, Track
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
        return jsonify(dict())


@application.route("/artists/<uri>/mb_metadata")
def get_mb_metadata(uri):
    try:
        result = Artist.query.filter_by(spot_uri=uri).first()
        metadata = Tasks.get_artist_metadata_from_mb(result.name)
    except Exception as e:
        print(f"Could not source metadata for {uri}: {e}")
    else:
        return jsonify(metadata._asdict()) if metadata is not None else jsonify({"error": "job failed"})


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


@application.route("/get_playlist/<playlist_uri>")
def get_playlist(playlist_uri: str):
    return jsonify(Tasks.run_playlist(playlist_uri))


@application.route("/scrape")
def scrape_lyrics():
    return jsonify(Tasks.scrape_all_lyrics())


@application.route("/go/lyrics/<track_uri>")
def scrape_lyric(track_uri):
    return jsonify(Tasks.scrape_track_lyrics(track_uri))


@application.route("/tracks/<uri>/annotate")
def annotate(uri):
    response = Tasks.annotate_track(uri)
    return response.text


@application.route("/tracks/<uri>/extract_links")
def extract_links(uri):
    return jsonify(Tasks.extract_candidate_links_from_track(uri))


