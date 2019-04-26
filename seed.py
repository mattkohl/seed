from flask import Response, jsonify
import os
from flask_migrate import Migrate, upgrade
from app.models import Artist, Song
from app import create_app, db
from app.pipeline.tasks import Tasks


application = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(application, db)


@application.route("/")
def index() -> str:
    return "Index"


@application.route("/artists/clear")
def clear_artists() -> str:
    count = Artist.query.count()
    for r in Artist.query.all():
        db.session.delete(r)
    db.session.commit()
    return f"Deleted {count} Artist records"


@application.route("/artists")
def artists() -> str:
    results = Artist.query.all()
    return "\n".join([str(a) for a in results])


@application.route("/songs")
def songs() -> str:
    results = Song.query.all()
    print(results)
    return jsonify("foo")


@application.route("/songs/clear")
def clear_songs() -> str:
    count = Song.query.count()
    for r in Song.query.all():
        db.session.delete(r)
    db.session.commit()
    return f"Deleted {count} Song records"


@application.route("/go/<playlist_uri>")
def go(playlist_uri: str):
    return Response(Tasks.playlist(playlist_uri), content_type='application/json')


@application.cli.command()
def deploy():
    upgrade()
