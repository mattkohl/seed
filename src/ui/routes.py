from flask import render_template, request, url_for, Response
from werkzeug.utils import redirect

from src.ui import ui


@ui.route("/")
def index():
    return render_template("ui/index.html")


@ui.route("/get_song")
def get_song():
    return "bar"


@ui.route("/edit_song")
def edit_song():
    return "bar"


@ui.route("/search")
def search():
    return "bar"
