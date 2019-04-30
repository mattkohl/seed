from typing import Dict

from app import create_app, db
from app.models import Artist, Song, Album
from app.persist.utils import PersistUtils
from app.spot.models import Track


class Persist:

    @staticmethod
    def persist_artist(artist: Artist):
        current = create_app('docker')
        with current.app_context():
            return PersistUtils.get_or_create(db.session, Artist, name=artist.name, spot_uri=artist.uri)
            
    @staticmethod
    def persist_song(track: Track):

        current = create_app('docker')
        with current.app_context():
            _album = PersistUtils.get_or_create(db.session, Album, name=track.album.name, spot_uri=track.album.uri,
                                                release_date=track.album.release_date)
            song = PersistUtils.get_or_create(db.session, Song, name=track.name, spot_uri=track.uri,
                                              popularity=track.popularity, preview_url=track.preview_url,
                                              album_id=_album.id)
            artists = [PersistUtils.get_or_create(db.session, Artist, name=artist.name, spot_uri=artist.uri) for artist
                       in track.artists]
            db.session.add(song)
            for artist in artists:
                song.artists.append(artist)
                artist.extract_albums.append(_album)
            db.session.commit()

    @staticmethod
    def persist_album(album: Album):

        current = create_app('docker')
        with current.app_context():
            return PersistUtils.get_or_create(db.session, Album, name=album.name, spot_uri=album.uri,
                                              release_date=album.release_date)
