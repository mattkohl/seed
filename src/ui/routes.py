import traceback

from flask import render_template, request, url_for, g
from werkzeug.utils import redirect
from sqlalchemy import or_

from src.spot.utils import SpotUtils
from src import db
from src.tasks.fetch import Fetch
from src.forms import SearchForm, UriForm, TrackForm, AlbumForm, ArtistForm
from src.ui import ui
from src.models import Track, Album, Artist, Location, Genre


@ui.route("/")
def index():
    queries = ["wack", "dope"]
    counts = [build_lyric_query_stat(q) for q in queries]
    stats = Fetch.stats()
    return render_template('ui/index.html', stats=stats, counts=counts)


@ui.route("/tracks")
def tracks():
    return render_class(Track, 'ui/tracks.html', 'ui.tracks')


@ui.route("/albums")
def albums():
    return render_class(Album, 'ui/albums.html', 'ui.albums')


@ui.route("/artists")
def artists():
    return render_class(Artist, 'ui/artists.html', 'ui.artists')


@ui.route("/locations")
def locations():
    return render_class(Location, 'ui/locations.html', 'ui.locations')


@ui.route("/tracks/<track_id>")
def get_track(track_id: int):
    return render_instance(Track, track_id, 'ui/track.html')


@ui.route("/albums/<album_id>")
def get_album(album_id: int):
    return render_instance(Album, album_id, 'ui/album.html')


@ui.route("/artists/<artist_id>")
def get_artist(artist_id: int):
    # id, name, spot_uri, thumb, img, birthplace, hometown, wikipedia_uri, dbp_uri, lyrics_percentage,
    # lyrics_missed_percentage, albums, primary_tracks, featured_tracks, genres

    q = request.args.get('q') if request.args.get('q') else ""
    instance = Artist.query.get(artist_id)
    if instance:
        albums_count = len(instance.albums)
        primary_tracks_count = len(instance.primary_tracks)
        featured_tracks_count = len(instance.featured_tracks)
        return render_template('ui/artist.html',
                               result=instance,
                               q=q,
                               albums_count=albums_count,
                               primary_tracks_count=primary_tracks_count,
                               featured_tracks_count=featured_tracks_count)
    return redirect(url_for('.index'))


@ui.route("/genres/<genre_id>")
def get_genre(genre_id: int):
    return render_instance(Genre, genre_id, 'ui/genre.html')


@ui.route("/locations/<location_id>")
def get_location(location_id: int):
    return render_instance(Location, location_id, 'ui/location.html')


@ui.route("/tracks/<track_id>/update", methods=["POST"])
def update_track(track_id: int):
    form = TrackForm(request.form)
    if form.validate_on_submit():
        _track = Track.query.filter_by(id=track_id).first()
        _track.lyrics = form.lyrics.data
        _track.lyrics_annotated = form.lyrics_annotated.data
        db.session.add(_track)
        db.session.commit()
        if not _track.lyrics_annotated:
            try:
                _ = Fetch.track_lyrics_annotate(_track.spot_uri)
            except Exception as e:
                print(f"Unable to annotate {_track.name}")
                traceback.print_tb(e.__traceback__)
    else:
        print(f"INVALID: {form.errors}")
    return redirect(url_for('ui.get_track', track_id=track_id))


@ui.route("/tracks/<track_id>/edit")
def edit_track(track_id: int):
    result = Track.query.filter_by(id=track_id).first()
    form = TrackForm(obj=result)
    return render_template('ui/track_edit.html', result=result, form=form)


@ui.route("/albums/<album_id>/update", methods=["POST"])
def update_album(album_id: int):
    form = AlbumForm(request.form)
    if form.validate_on_submit():
        _album = Album.query.filter_by(id=album_id).first()
        _album.name = form.name.data
        _album.release_date_string = form.release_date_string.data
        _album.release_date = SpotUtils.clean_up_date(_album.release_date_string)
        _album.dbp_uri = form.dbp_uri.data
        _album.wikipedia_uri = form.wikipedia_uri.data
        db.session.add(_album)
        db.session.commit()
    else:
        print(f"INVALID: {form.errors}")
    return redirect(url_for('ui.get_album', album_id=album_id))


@ui.route("/albums/<album_id>/edit")
def edit_album(album_id: int):
    result = Album.query.filter_by(id=album_id).first()
    form = AlbumForm(obj=result)
    return render_template('ui/album_edit.html', result=result, form=form)


@ui.route("/artists/<artist_id>/update", methods=["POST"])
def update_artist(artist_id: int):
    form = ArtistForm(request.form)
    if form.validate_on_submit():
        _artist = Artist.query.filter_by(id=artist_id).first()
        _artist.name = form.name.data
        _artist.dbp_uri = form.dbp_uri.data
        _artist.wikipedia_uri = form.wikipedia_uri.data
        db.session.add(_artist)
        db.session.commit()
    else:
        print(f"INVALID: {form.errors}")
    return redirect(url_for('ui.get_artist', artist_id=artist_id))


@ui.route("/artists/<artist_id>/edit")
def edit_artist(artist_id: int):
    result = Artist.query.filter_by(id=artist_id).first()
    form = ArtistForm(obj=result)
    return render_template('ui/artist_edit.html', result=result, form=form)


@ui.route('/search', methods=['GET', 'POST'])
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('.index'))
    return redirect(url_for('.search_results', query=g.search_form.search.data))


@ui.route('/search-results/<query>')
def search_results(query, in_xml=True):
    result = Track.query.filter(or_(
        Track.lyrics.ilike(f"% {query}%"),
        Track.lyrics.ilike(f"{query}%"),
        Track.lyrics.ilike(f"%\n{query}%")
    )).join(Album).order_by(Album.release_date)
    template = 'ui/xml_search_results.html' if in_xml else 'ui/search_results.html'
    return render_template(template, query=query, results=result.all(), number=result.count())


@ui.before_request
def before_request():
    g.search_form = SearchForm()
    g.uri_form = UriForm()


def pagination(_request) -> (int, int, int):
    offset = _request.args.get('offset') or 0
    offset = int(offset)
    start_page = int(offset/100)
    end_page = start_page + 100
    return offset, start_page, end_page


def render_class(model: db.Model, template: str, endpoint: str):
    q = request.args.get('q') or ""
    date = request.args.get('date') or ""
    offset, start_page, end_page = pagination(request)
    instances = model.query.filter(model.name.ilike(f"%{q}%")).order_by(model.id).limit(100).offset(offset)
    count = model.query.count()
    return render_template(template, endpoint=endpoint, instances=instances, offset=offset, count=count, start_page=start_page, end_page=end_page, q=q)


def render_instance(model: db.Model, _id: int, template: str):
    q = request.args.get('q') if request.args.get('q') else ""
    instance = model.query.get(_id)
    if instance:
        return render_template(template, result=instance, q=q)
    return redirect(url_for('.index'))


def build_lyric_query_stat(query: str):
    return {"query": query, "count": Track.query.filter(Track.lyrics.contains(query)).count()}
