from flask import render_template, request, url_for, g
from werkzeug.utils import redirect

from src.forms import SearchForm
from src.ui import ui

from src.models import Track, Album


@ui.route("/")
def test():
    return render_template('_base.html')


@ui.route("/index")
def index():
    offset = request.args.get('offset') or 0
    offset = int(offset)
    songs = Track.query.limit(10).offset(offset)
    start_page = int(offset/10)
    end_page = start_page + 10
    song_count = Track.query.count()
    return render_template('ui/index.html', songs=songs, offset=offset, song_count=song_count, start_page=start_page, end_page=end_page)


@ui.route("/<song_id>")
def get_song(song_id: int):
    q = request.args.get('q') if request.args.get('q') else ""
    song = Track.query.filter_by(id=song_id).first()
    if song:
        return render_template('ui/song.html', song_id=song_id, result=song, q=q)
    return redirect(url_for('.index'))


@ui.route("/edit_song")
def edit_song():
    return "bar"


@ui.route('/search', methods=['GET', 'POST'])
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('.index'))
    return redirect(url_for('.search_results', query=g.search_form.search.data))


@ui.route('/search-results/<query>')
def search_results(query, in_xml=True):
    q = query
    if query.endswith('.*'):
        q = q.replace('.*', '')

    result = Track.query.filter(Track.lyrics.like('%'+q+'%')).join(Album).order_by(Album.release_date)

    if in_xml:
        return render_template('ui/xml_search_results.html', query=query, results=result.all(), number=result.count())
    else:
        return render_template('ui/search_results.html', query=query, results=result.all(), number=result.count())


@ui.before_request
def before_request():
    g.search_form = SearchForm()
