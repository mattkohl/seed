from flask import render_template, request, url_for, g
from werkzeug.utils import redirect

from src import db
from src.forms import SearchForm
from src.ui import ui

from src.models import Track, Album, Artist


@ui.route("/")
def index():
    return render_template('ui/index.html')


@ui.route("/tracks")
def tracks():
    return render_class(Track, 'ui/tracks.html')


@ui.route("/albums")
def albums():
    return render_class(Album, 'ui/albums.html')


@ui.route("/artists")
def artists():
    return render_class(Artist, 'ui/artists.html')


@ui.route("/tracks/<track_id>")
def get_track(track_id: int):
    q = request.args.get('q') if request.args.get('q') else ""
    track = Track.query.filter_by(id=track_id).first()
    if track:
        return render_template('ui/track.html', result=track, q=q)
    return redirect(url_for('.index'))


@ui.route("/albums/<album_id>")
def get_album(album_id: int):
    album = Album.query.filter_by(id=album_id).first()
    if album:
        return render_template('ui/album.html', result=album)
    return redirect(url_for('.index'))


@ui.route("/artists/<artist_id>")
def get_artist(artist_id: int):
    artist = Album.query.filter_by(id=artist_id).first()
    if artist:
        return render_template('ui/artist.html', artist=artist)
    return redirect(url_for('.index'))


@ui.route("/edit_track")
def edit_track():
    return "bar"


@ui.route('/search', methods=['GET', 'POST'])
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('.index'))
    return redirect(url_for('.search_results', query=g.search_form.search.data))


@ui.route('/search-results/<query>')
def search_results(query, in_xml=True):
    result = Track.query.filter(Track.lyrics.contains(query)).join(Album).order_by(Album.release_date)
    template = 'ui/xml_search_results.html' if in_xml else 'ui/search_results.html'
    return render_template(template, query=query, results=result.all(), number=result.count())


@ui.before_request
def before_request():
    g.search_form = SearchForm()


def pagination(_request) -> (int, int, int):
    offset = _request.args.get('offset') or 0
    offset = int(offset)
    start_page = int(offset/10)
    end_page = start_page + 10
    return offset, start_page, end_page


def render_class(model: db.Model, template: str):
    offset, start_page, end_page = pagination(request)
    instances = model.query.order_by(model.id).limit(10).offset(offset)
    count = model.query.count()
    return render_template(template, instances=instances, offset=offset, count=count, start_page=start_page, end_page=end_page)
