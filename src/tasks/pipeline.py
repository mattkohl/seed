from typing import Dict, List

from src.models import Track, Artist, Album
from src.tasks.fetch import Fetch
from src.tasks.persist import Persistence
from src.repository.persist import Persist
from sqlalchemy.sql.expression import func


class Tasks:

    @staticmethod
    def run_playlist(playlist_uri) -> List[Dict]:
        track_tuples = Fetch.playlist_tracks(playlist_uri)
        [Persistence.persist_track(t) for t in track_tuples]
        return [Fetch.track(t.uri) for t in track_tuples]

    @staticmethod
    def run_random_track() -> Dict:
        _track = Track.query.filter(Track.lyrics == None).order_by(func.random()).first()
        return Tasks.run_track(_track.spot_uri) if _track and _track.spot_uri is not None else {"error": "No tracks found"}

    @staticmethod
    def run_random_album() -> Dict:
        _album = Album.query.filter(Album.last_updated == None).order_by(func.random()).first()
        return Tasks.run_album(_album.spot_uri) if _album and _album.spot_uri is not None else {"error": "No albums found"}

    @staticmethod
    def run_random_artist() -> Dict:
        _artist = Artist.query.filter(Artist.last_updated == None).order_by(func.random()).first()
        return Tasks.run_artist(_artist.spot_uri) if _artist and _artist.spot_uri is not None else {"error": "No albums found"}

    @staticmethod
    def run_track(track_uri) -> Dict:
        _track = Fetch.track(track_uri)
        _ = Fetch.track_dbp_uri(track_uri)
        _ = Fetch.track_lyrics(track_uri, force_update=True)
        _ = Fetch.track_lyrics_annotate(track_uri)
        _ = Fetch.track_sections(track_uri)
        Persist.update(Track, _track['id'], {})
        return Fetch.track(track_uri)

    @staticmethod
    def run_track_sections(track_uri) -> Dict:
        _track = Fetch.track(track_uri)
        _ = Fetch.track_sections(track_uri)
        Persist.update(Track, _track['id'], {})
        return Fetch.track(track_uri)

    @staticmethod
    def run_artist(artist_uri) -> Dict:
        album_tuples = Fetch.artist_albums(artist_uri)
        print(f"Downloaded {len(album_tuples)} albums for {artist_uri}")
        [Persistence.persist_album(a) for a in album_tuples]
        _artist = Fetch.artist_mb_metadata(artist_uri)
        _ = Fetch.artist_dbp_uri(artist_uri, True)
        _ = Fetch.artist_hometown(artist_uri)
        _ = Fetch.artist_birthplace(artist_uri)
        _ = Fetch.artist_spot_metadata(artist_uri)
        Persist.update(Artist, _artist['id'], {})
        return Fetch.artist(artist_uri)

    @staticmethod
    def run_album(album_uri) -> Dict:
        track_tuples = Fetch.album_tracks(album_uri)
        [Persistence.persist_track(t) for t in track_tuples]
        _album = Fetch.album_dbp_uri(album_uri)
        _ = Fetch.album_mb_metadata(album_uri)
        Persist.update(Album, _album['id'], {})
        return Fetch.album(album_uri)
