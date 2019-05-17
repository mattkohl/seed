from datetime import datetime
from typing import Dict, Optional, List, Callable
import traceback

from app import db
from app.dbp.annotation import Spotlight
from app.dbp.models import CandidatesTuple, AnnotationTuple
from app.geni import parser, utils
from app.mb import metadata
from app.mb.models import MbArtistTuple, MbAlbumTuple
from app.models import Artist, Track, Album
from app.spot.albums import SpotAlbum
from app.spot.artists import SpotArtist
from app.spot.models import TrackTuple, AlbumTuple
from app.spot.playlists import SpotPlaylist
from app.spot.tracks import SpotTrack
from app.spot.utils import SpotUtils
from app.tasks.persist import Persistence
from app.utils import Utils


class Fetch:

    @staticmethod
    def album(uri: str) -> Dict:
        try:
            result = Album.query.filter_by(spot_uri=uri).first()
            _album = result.as_dict()
            _artists = [_artist.as_dict() for _artist in result.artists]
            _tracks = [_track.as_dict() for _track in result.tracks]
            _album.update({"tracks": _tracks, "artists": _artists})
        except Exception as e:
            print(f"Unable to retrieve album {uri}")
            traceback.print_tb(e.__traceback__)
        else:
            return _album

    @staticmethod
    def album_dbp_uri(uri: str, force_update: bool = False) -> Dict:
        result = Album.query.filter_by(spot_uri=uri).first()
        _album = result.as_dict()
        if result.dbp_uri is None or force_update:
            dbp_uri = Fetch.dbp_uri(instance_id=result.id, instance_name=result.name, model=Album, uri=uri,
                                    fetch_candidates=Fetch.album_and_artist_annotations)
            _album.update({"dbp_uri": dbp_uri})
        return _album

    @staticmethod
    def album_and_artist_annotations(album_uri: str) -> CandidatesTuple:
        _album = Album.query.filter_by(spot_uri=album_uri).first()
        _artists = [_artist for _artist in _album.artists]
        message = f"{_album.name}, a hip-hop album, was released in {_album.release_date_string[:4]} by " + ", ".join([_artist.name for _artist in _artists])
        print(message)
        return Spotlight.candidates(message)

    @staticmethod
    def album_tracks(uri: str) -> List[TrackTuple]:
        sp = SpotAlbum()
        try:
            result = Album.query.filter_by(spot_uri=uri).first()
            track_dicts = sp.download_album_tracks(uri)
            track_tuples = [t for t in SpotUtils.tuplify_tracks(track_dicts, result.as_album_tuple()) if t is not None]
        except Exception as e:
            print(f"Unable to retrieve album {uri} tracks:")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            return track_tuples

    @staticmethod
    def albums(name_filter: Optional[str]) -> List[Dict]:
        results = Album.query.filter(Album.name.ilike(f"%{name_filter}%")) if name_filter else Album.query.all()
        return [_album.as_dict() for _album in results]

    @staticmethod
    def artist(uri: str) -> Dict:
        try:
            result = Artist.query.filter_by(spot_uri=uri).first()
            if result is None:
                print(f"{uri} not found. Querying API.")
                album_tuples = Fetch.artist_albums(uri)
                [Persistence.persist_album(a) for a in album_tuples]
                result = Artist.query.filter_by(spot_uri=uri).first()
            _artist = result.as_dict()
            _albums = [_album.as_dict() for _album in result.albums]
            _artist.update({"albums": _albums})
        except Exception as e:
            print(f"Unable to retrieve artist {uri}:")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            return _artist

    @staticmethod
    def artists(name_filter: Optional[str]) -> List[Dict]:
        results = Artist.query.filter(Artist.name.ilike(f"%{name_filter}%")) if name_filter else Artist.query.all()
        return [_artist.as_dict() for _artist in results]

    @staticmethod
    def artist_albums(uri: str) -> List[AlbumTuple]:
        sp = SpotArtist()
        try:
            album_dicts = sp.download_artist_albums(uri)
            album_tuples = [a for a in SpotUtils.extract_albums(album_dicts) if a is not None]
        except Exception as e:
            print(f"Unable to retrieve artist {uri} albums:")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            return album_tuples

    @staticmethod
    def artist_and_track_name_annotations(artist_uri: str) -> CandidatesTuple:
        _artist = Artist.query.filter_by(spot_uri=artist_uri).first()
        _disambiguation = _artist.mb_obj['disambiguation'] if _artist.mb_obj is not None else None
        _clause = f"({_disambiguation})" if _disambiguation is not None else "the hip-hop artist"
        _albums = [_album for _album in _artist.albums if len(_album.artists) == 1]
        _statements = set([f"""{_album.name} in {_album.release_date_string[:4]}""" for _album in _albums])
        message = f"{_artist.name}, {_clause}, released the albums " + ", ".join(_statements)
        print(message)
        return Spotlight.candidates(message)

    @staticmethod
    def artist_dbp_uri(uri: str, force_update: bool = False) -> Dict:
        result = Artist.query.filter_by(spot_uri=uri).first()
        _artist = result.as_dict()
        if result.dbp_uri is None or force_update:
            dbp_uri = Fetch.dbp_uri(instance_id=result.id, instance_name=result.name, model=Artist, uri=uri,
                                    fetch_candidates=Fetch.artist_and_track_name_annotations)
            _artist.update({"dbp_uri": dbp_uri})
        return _artist

    @staticmethod
    def artist_mb_metadata(uri: str, force_update: bool = False) -> Dict:
        result = Artist.query.filter_by(spot_uri=uri).first()
        _artist = result.as_dict()
        if result.mb_id is None or force_update:
            mb_results = metadata.MB().search_artists(result.name)
            cleaned = {Utils.clean_key(k): v for k, v in mb_results[0].items()}
            at = MbArtistTuple(**cleaned)
            Persistence.persist_mb_metadata(result.id, at)
            _artist.update({"mb_id": at.id, "mb_obj": at._asdict()})
        return _artist

    @staticmethod
    def dbp_uri(instance_id: int, instance_name: str, model: db.Model, uri: str, fetch_candidates: Callable) -> Optional[str]:
        try:
            candidates = fetch_candidates(uri)
            first = candidates.Resources[0]
            offset_is_zero = int(first["@offset"]) == 0
            local_name = first["@URI"].split("/")[-1].replace("_", " ")
            fuzzy_match_score = Utils.fuzzy_match(instance_name, local_name)
            dbp_uri = first["@URI"] if (offset_is_zero and fuzzy_match_score > 75) else None
            Persistence.persist_dbp_uri(model, instance_id, dbp_uri)
        except Exception as e:
            print(f"Could not get DBP URI for {instance_name}")
            traceback.print_tb(e.__traceback__)
        else:
            if dbp_uri is None:
                print(f"DBP resolution rejected for this candidate {instance_name}: {first}; Fuzzy match score was {fuzzy_match_score} using {local_name}")
            return dbp_uri

    @staticmethod
    def playlist_tracks(uri: str) -> List[TrackTuple]:
        sp = SpotPlaylist()
        try:
            playlist = sp.download_playlist_tracks(uri)
            track_dicts = SpotUtils.extract_tracks_from_playlist(playlist)
            track_tuples = [t for t in SpotUtils.tuplify_tracks(track_dicts, None) if t is not None]
        except Exception as e:
            print(f"Unable to retrieve playlist {uri} tracks")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            return track_tuples

    @staticmethod
    def stats():
        return {
            "counts": {
                "artists": Artist.query.count(),
                "albums": Album.query.count(),
                "tracks": Track.query.count(),
                "lyrics": Track.query.filter(Track.lyrics != None).count()
            }
        }

    @staticmethod
    def text_annotate(text) -> AnnotationTuple:
        try:
            annotated = Spotlight.annotate(text)
        except Exception as e:
            print(f"Unable to annotate text")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            return annotated

    @staticmethod
    def track(uri: str) -> Dict:
        result = Track.query.filter_by(spot_uri=uri).first()
        if result is None:
            sp = SpotTrack()
            track_dict = sp.download_track(uri)
            track_tuple = SpotUtils.tuplify_track(track_dict, None)
            Persistence.persist_track(track_tuple)
            result = Track.query.filter_by(spot_uri=uri).first()
        _track = result.as_dict()
        _artists = [_artist.as_dict() for _artist in result.artists]
        _album = result.album.as_dict()
        _track.update({"album": _album, "artists": _artists})
        return _track

    @staticmethod
    def track_album_and_artist_annotations(track_uri: str) -> CandidatesTuple:
        _track = Track.query.filter_by(spot_uri=track_uri).first()
        _artists = [_artist for _artist in _track.album.artists]
        message = f"{_track.name}, a track on the a hip-hop album {_track.album.name}, released in {_track.album.release_date_string[:4]} by " + ", ".join([_artist.name for _artist in _artists])
        print(message)
        return Spotlight.candidates(message)

    @staticmethod
    def track_dbp_uri(uri: str, force_update: bool = False) -> Dict:
        result = Track.query.filter_by(spot_uri=uri).first()
        _track = result.as_dict()
        if result.dbp_uri is None or force_update:
            dbp_uri = Fetch.dbp_uri(instance_id=result.id, instance_name=result.name, model=Track, uri=uri,
                                    fetch_candidates=Fetch.track_album_and_artist_annotations)
            _track.update({"dbp_uri": dbp_uri})
        return _track

    @staticmethod
    def track_mb_metadata(uri: str, force_update: bool = False):
        result = Track.query.filter_by(spot_uri=uri).first()

        def cleaned(d) -> Dict:
            return {Utils.clean_key(k): v for k, v in d.items()}

        _albums = [cleaned(item)
                   for _artist in result.album.artists
                   for item in metadata.MB().get_albums_with_artist_id(_artist.mb_id)]

        return _albums

    @staticmethod
    def track_lyrics(uri: str, force_update: bool = False) -> Dict:
        result = Track.query.filter_by(spot_uri=uri).first()
        _track = result.as_dict()
        _artists = [_artist.as_dict() for _artist in result.artists]
        _album = result.album.as_dict()
        _track.update({"album": _album, "artists": _artists})
        if result.lyrics is None or force_update:
            url = utils.GenUtils.link([_artist.name for _artist in result.artists], result.name)
            try:
                lyrics = parser.GenParser.download(url)
            except Exception as e:
                print(f"Could not connect to {url}:", e)
                raise
            else:
                fetched = datetime.now()
                Persistence.persist_lyrics(result.id, lyrics, url, fetched)
                _track.update({"lyrics": lyrics, "lyrics_url": url, "lyrics_fetched_timestamp": fetched})
        return _track

    @staticmethod
    def track_lyrics_test(uri: str):
        result = Track.query.filter_by(spot_uri=uri).first()
        return utils.GenUtils.link([_artist.name for _artist in result.artists], result.name)

    @staticmethod
    def track_lyric_links(uri) -> Dict:
        result = Track.query.filter_by(spot_uri=uri).first()
        _track = result.as_dict()
        if result.lyrics is not None:
            candidates = Spotlight.candidates(result.lyrics)
            Persistence.persist_lyrics_links(result.id, candidates)
            _track.update({"lyrics_annotations_json": candidates._asdict()})
        return _track

    @staticmethod
    def track_lyrics_annotate(uri) -> Dict:
        result = Track.query.filter_by(spot_uri=uri).first()
        _track = result.as_dict()
        if result.lyrics is not None:
            annotated = Spotlight.annotate(result.lyrics)
            Persistence.persist_lyrics_annotated(result.id, annotated)
            _track.update({"lyrics_annotated": annotated})
        return _track

    @staticmethod
    def track_lyrics_annotations(uri) -> str:
        _track = Track.query.filter_by(spot_uri=uri).first()
        return _track.lyrics_annotated

    @staticmethod
    def tracks(name_filter: Optional[str]) -> List[Dict]:
        results = Track.query.filter(Track.name.ilike(f"%{name_filter}%")) if name_filter else Track.query.all()
        return [_track.as_dict() for _track in results]
