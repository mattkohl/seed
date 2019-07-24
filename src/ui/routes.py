from flask import render_template, request, url_for, g
from werkzeug.utils import redirect

from src.forms import SearchForm
from src.ui import ui

from src.models import Track, Album


@ui.route("/")
def index():
    offset = request.args.get('offset') or 0
    offset = int(offset)
    tracks = Track.query.order_by(Track.id).limit(10).offset(offset)
    start_page = int(offset/10)
    end_page = start_page + 10
    track_count = Track.query.count()
    return render_template('ui/index.html', tracks=tracks, offset=offset, track_count=track_count, start_page=start_page, end_page=end_page)


@ui.route("/<track_id>")
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
