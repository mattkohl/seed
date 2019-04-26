from typing import Dict

from app.models import Artist, db, Song
from app.persist.utils import PersistUtils
from app import create_app


class Persist:

    @staticmethod
    def persist_artist(artist: Dict) -> Artist:
        try:
            name, uri = artist["name"], artist["uri"]
            current = create_app('docker')
            with current.app_context():
                return PersistUtils.get_or_create(db.session, Artist, name=name, spot_uri=uri)

        except Exception as e:
            print(str(e))

    @staticmethod
    def persist_song(track: Dict) -> Song:
        try:
            name, uri = track["name"], track["uri"]
            current = create_app('docker')
            with current.app_context():
                artists = [PersistUtils.get_or_create(db.session, Artist, name=artist.name, spot_uri=artist.uri) for artist in track["artists"]]
                song = PersistUtils.get_or_create(db.session, Song, name=name, spot_uri=uri)
                for artist in artists:
                    song.artists.append(artist)
                db.session.add(song)
                db.session.commit()
                return song

        except Exception as e:
            print(str(e))
