from datetime import datetime
from typing import Dict, Optional, List, Callable
import traceback

from src import db
from src.dbp.annotation import Spotlight
from src.dbp.models import CandidatesTuple, AnnotationTuple
from src.dbp.sparql import Sparql
from src.geni import parser, utils
from src.mb import metadata
from src.mb.models import MbArtistTuple, MbAlbumTuple
from src.mb.mbutils import MbUtils
from src.models import Artist, Track, Album, Location, Genre
from src.spot.albums import SpotAlbum
from src.spot.artists import SpotArtist
from src.spot.models import TrackTuple, AlbumTuple
from src.spot.playlists import SpotPlaylist
from src.spot.tracks import SpotTrack
from src.spot.utils import SpotUtils
from src.tasks.persist import Persistence
from src.utils import Utils


class Fetch:

    @staticmethod
    def album(uri: str) -> Dict:
        try:
            result = Album.query.filter_by(spot_uri=uri).first()
            if result is None:
                sp = SpotAlbum()
                _album = sp.download_album(uri)
                _album_tuple = SpotUtils.extract_album(_album)
                Persistence.persist_album(_album_tuple)
                result = Album.query.filter_by(spot_uri=uri).first()
            _album = result.as_dict()
            _artists = [_artist.as_dict() for _artist in result.artists]
            _tracks = [_track.as_dict() for _track in result.tracks]
            _genres = [genre.name for genre in result.genres] if result.genres else None
            _album.update({"tracks": _tracks, "artists": _artists, "genres": _genres})
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
    def album_mb_metadata(uri: str, force_update: bool = False):
        result = Album.query.filter_by(spot_uri=uri).first()
        _album = result.as_dict()

        if result.mb_id is None or force_update:
            _artist_mb_ids = [a.mb_id for a in result.artists]
            if _artist_mb_ids:
                _mb_album_candidates = [MbUtils.cleaned(item)
                                        for _id in _artist_mb_ids
                                        for item in metadata.MB().get_albums_with_artist_id(_id)]

                _mb_albums = [a for a in _mb_album_candidates if Utils.fuzzy_match(a['title'], result.name) > 90]

                if _mb_albums:
                    mb_obj = _mb_albums[0]
                    _album_tuple = MbAlbumTuple(**mb_obj)
                    Persistence.persist_mb_metadata(Album, result.id, _album_tuple)
                    _album.update({"mb_id": _album_tuple.id, "mb_obj": _album_tuple._asdict()})
                else:
                    _candidate_string = '\n'.join([str(a) for a in _mb_album_candidates])
                    print(f"Found no matches for {result} in list:\n {_candidate_string}")
            else:
                print(f"Cannot resolve MB id for {result}: missing mb_id for {[result.artists]}")
        return _album

    @staticmethod
    def album_tracks(uri: str):
        sp = SpotAlbum()
        try:
            _album = Album.query.filter_by(spot_uri=uri).first()
            _tracks = sp.download_album_tracks(uri)
            track_tuples = [t for t in SpotUtils.tuplify_tracks(_tracks, _album.as_album_tuple(_album.artists)) if t is not None]
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
            _albums = [_album.as_dict() for _album in sorted(result.albums, key=lambda x: x.release_date)]
            _birthplace = result.birthplace.as_dict() if result.birthplace else None
            _hometown = result.hometown.as_dict() if result.hometown else None
            _genres = [genre.name for genre in result.genres] if result.genres else None
            _artist.update({"albums": _albums, "hometown": _hometown, "birthplace": _birthplace, "genres": _genres})
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
            _cleaned = {Utils.clean_key(k): v for k, v in mb_results}
            _cleaned_with_genres = MbUtils.add_genres(_cleaned)
            _artist_tuple = MbArtistTuple(**_cleaned_with_genres)
            Persistence.persist_mb_metadata(Artist, result.id, _artist_tuple)
            _artist.update({"mb_id": _artist_tuple.id, "mb_obj": _artist_tuple._asdict()})
        return _artist

    @staticmethod
    def artist_spot_metadata(uri: str, force_update: bool = False) -> Dict:
        result = Artist.query.filter_by(spot_uri=uri).first()
        _artist = result.as_dict()
        if result.img is None or force_update:
            sp = SpotArtist()
            try:
                artist_dict = sp.download_artist(uri)
                artist_tuple = SpotUtils.extract_artist(artist_dict)
                Persistence.persist_artist(artist_tuple)
            except Exception as e:
                print(f"Unable to retrieve artist {uri} metadata:")
                traceback.print_tb(e.__traceback__)
                raise
            else:
                _artist.update({"genres": artist_tuple.genres})
        return _artist

    @staticmethod
    def artist_hometown(uri: str) -> Dict:
        result = Artist.query.filter_by(spot_uri=uri).first()
        _artist = result.as_dict()
        if result.dbp_uri is not None:
            _location_tuple = Sparql.hometown(result.dbp_uri)
            if _location_tuple:
                Persistence.persist_artist_hometown(result.id, _location_tuple)
                _location = Location.query.filter_by(dbp_uri=_location_tuple.uri).first()
                _artist.update({"hometown": _location.as_dict()})
        return _artist

    @staticmethod
    def artist_birthplace(uri: str) -> Dict:
        result = Artist.query.filter_by(spot_uri=uri).first()
        _artist = result.as_dict()
        if result.dbp_uri is not None:
            _location_tuple = Sparql.birthplace(result.dbp_uri)
            if _location_tuple:
                Persistence.persist_artist_birthplace(result.id, _location_tuple)
                _location = Location.query.filter_by(dbp_uri=_location_tuple.uri).first()
                _artist.update({"birthplace": _location.as_dict()})
        return _artist

    @staticmethod
    def dbp_uri(instance_id: int, instance_name: str, model: db.Model, uri: str, fetch_candidates: Callable) -> Optional[str]:
        try:
            candidates = fetch_candidates(uri)
            first = candidates.Resources[0]
            offset_is_zero = int(first["@offset"]) == 0
            local_name = first["@URI"].split("/")[-1].replace("_", " ")
            fuzzy_match_score = Utils.fuzzy_match(instance_name, local_name)
            dbp_uri = first["@URI"] if ((offset_is_zero and fuzzy_match_score > 85) or fuzzy_match_score == 100) else None
            Persistence.persist_dbp_uri(model, instance_id, dbp_uri)
        except Exception as e:
            print(f"Could not get DBP URI for {instance_name}")
            traceback.print_tb(e.__traceback__)
        else:
            if dbp_uri is None:
                print(f"DBP resolution rejected for this candidate {instance_name}: {first}; Fuzzy match score was {fuzzy_match_score} using {local_name}")
            return dbp_uri

    @staticmethod
    def genre(_id: int) -> Dict:
        try:
            result = Genre.query.filter_by(id=_id).first()
            _genre = result.as_dict()
            _artists = [_artist.name for _artist in result.artists]
            _albums = [_album.name for _album in result.albums]
            _genre.update({"artists": _artists, "albums": _albums})
        except Exception as e:
            print(f"Unable to retrieve genre {_id}")
            traceback.print_tb(e.__traceback__)
        else:
            return _genre

    @staticmethod
    def genres(name_filter: Optional[str]) -> List[Dict]:
        results = Genre.query.filter(Genre.name.ilike(f"%{name_filter}%")) if name_filter else Genre.query.all()

        def _genres():
            for result in results:
                _genre = result.as_dict()
                _artists = [_artist.name for _artist in result.artists]
                _albums = [_album.name for _album in result.albums]
                _genre.update({"artists": _artists, "albums": _albums})
                yield _genre
        return list(_genres())

    @staticmethod
    def locations(name_filter: Optional[str]) -> List[Dict]:
        results = Location.query.filter(Location.name.ilike(f"%{name_filter}%")) if name_filter else Location.query.all()

        def _locations():
            for result in results:
                _location = result.as_dict()
                _hometown_of = [a.name for a in result.hometown_of]
                _birthplace_of = [a.name for a in result.birthplace_of]
                _location.update({"hometown_of": _hometown_of, "birthplace_of": _birthplace_of})
                yield _location
        return list(_locations())

    @staticmethod
    def location(_id: int) -> Dict:
        try:
            result = Location.query.filter_by(id=_id).first()
            _location = result.as_dict()
            _hometown_of = [_artist.name for _artist in result.hometown_of]
            _birthplace_of = [_artist.name for _artist in result.birthplace_of]
            _location.update({"hometown_of": _hometown_of, "birthplace_of": _birthplace_of})
        except Exception as e:
            print(f"Unable to retrieve location {_id}")
            traceback.print_tb(e.__traceback__)
        else:
            return _location

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
                "genres": Genre.query.count(),
                "locations": Location.query.count(),
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
        _primary_artists = [_artist.as_dict() for _artist in result.primary_artists]
        _featured_artists = [_artist.as_dict() for _artist in result.featured_artists]
        _album = result.album.as_dict()
        _track.update({"album": _album, "primary_artists": _primary_artists, "featured_artists": _featured_artists})
        return _track

    @staticmethod
    def track_album_and_artist_annotations(track_uri: str) -> CandidatesTuple:
        _track = Track.query.filter_by(spot_uri=track_uri).first()
        _artists = [_artist for _artist in _track.primary_artists]
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
    def track_lyrics(uri: str, force_update: bool = False) -> Dict:
        result = Track.query.filter_by(spot_uri=uri).first()
        _track = result.as_dict()
        _artists = [_artist.as_dict() for _artist in result.primary_artists]
        _album = result.album.as_dict()
        _track.update({"album": _album, "artists": _artists})
        if result.lyrics is None or force_update:
            url = utils.GenUtils.link([_artist.name for _artist in result.primary_artists], result.name)
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
    def track_mb_metadata(uri: str, force_update: bool = False):
        result = Track.query.filter_by(spot_uri=uri).first()
        _track = result.as_dict()
        if result.mb_id is None or force_update:
            if result.album.mb_id:
                _mb_track_candidates = [MbUtils.cleaned(item) for item in metadata.MB().get_tracks_with_album_id(result.album.mb_id)]

                _mb_tracks = [a for a in _mb_track_candidates if Utils.fuzzy_match(a['title'], result.name) > 90]
                if _mb_tracks:
                    mb_obj = _mb_tracks[0]
                    from pprint import pprint
                    pprint(_mb_tracks)
                else:
                    _candidate_string = '\n'.join([str(a) for a in _mb_track_candidates])
                    print(f"Found no matches for {result} in list:\n {_candidate_string}")
            else:
                print(f"Cannot resolve MB id for {result}: missing mb_id for {[result.artists]}")
        return _track

    @staticmethod
    def tracks(name_filter: Optional[str]) -> List[Dict]:
        results = Track.query.filter(Track.name.ilike(f"%{name_filter}%")) if name_filter else Track.query.all()
        return [_track.as_dict() for _track in results]

    @staticmethod
    def tracks_missing_lyrics():
        return [t.as_dict() for t in Track.query.filter_by(lyrics=None).filter_by(lyrics_url=None).limit(5)]
