from datetime import datetime
from typing import Dict, Optional, List
import traceback

from app.dbp.annotation import Spotlight
from app.dbp.models import CandidatesTuple
from app.geni import parser, utils
from app.mb import metadata
from app.mb.models import ArtistTuple as MBArtistTuple
from app.models import Artist, Track, Album
from app.spot.albums import SpotAlbum
from app.spot.artists import SpotArtist
from app.spot.models import TrackTuple, AlbumTuple
from app.spot.playlists import SpotPlaylist
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
    def album_tracks(uri: str) -> List[TrackTuple]:
        sp = SpotAlbum()
        try:
            result = Album.query.filter_by(spot_uri=uri).first()
            track_dicts = sp.download_tracks(uri)
            track_tuples = SpotUtils.tuplify_tracks(track_dicts, result.as_album_tuple())
        except Exception as e:
            print(f"Unable to retrieve album {uri} tracks:")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            return track_tuples

    @staticmethod
    def albums() -> List[Dict]:
        return [_album.as_dict() for _album in Album.query.all()]

    @staticmethod
    def artist(uri: str) -> Dict:
        try:
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
    def artists() -> List[Dict]:
        return [_artist.as_dict() for _artist in Artist.query.all()]

    @staticmethod
    def artist_albums(uri: str) -> List[AlbumTuple]:
        sp = SpotArtist()
        try:
            album_dicts = sp.download_albums(uri)
            album_tuples = sp.extract_albums(album_dicts)
        except Exception as e:
            print(f"Unable to retrieve artist {uri} albums:")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            return album_tuples

    @staticmethod
    def artist_and_track_name_annotations(artist_uri: str) -> CandidatesTuple:
        _artist = Artist.query.filter_by(spot_uri=artist_uri).first()
        _albums = [_album for _album in _artist.albums if len(_album.artists) == 1]
        _statements = set([f""" {_album.name} in {_album.release_date_string[:4]}""" for _album in _albums])
        message = f"{_artist.name}, the hip-hop artist, released the albums" + ", \n".join(_statements)
        print(message)
        return Spotlight.candidates(message)

    @staticmethod
    def artist_dbp_uri(uri: str, force_update: bool = False) -> Dict:
        result = Artist.query.filter_by(spot_uri=uri).first()
        _artist = result.as_dict()
        if result.dbp_uri is None or force_update:
            try:
                candidates = Fetch.artist_and_track_name_annotations(uri)
                potentials = [resource for resource in candidates.Resources if "DBpedia:MusicalArtist" in resource['@types'].split(",")]
                dbp_uri = potentials[0]["@URI"] if potentials and Utils.fuzzy_match(result.name, potentials[0]["@URI"].split("/")[-1]) else None
                Persistence.persist_dbp_uri(result.id, dbp_uri)
            except Exception as e:
                print(f"Could not get DBP URI for {result.name}", e)
            else:
                _artist.update({"dbp_uri": dbp_uri})
        return _artist

    @staticmethod
    def artist_mb_metadata(uri: str, force_update: bool = False) -> Optional[MBArtistTuple]:
        result = Artist.query.filter_by(spot_uri=uri).first()
        _artist = result.as_dict()
        if result.mb_id is None or force_update:
            mb_results = metadata.MBArtist().search(result.name)
            cleaned = {Utils.clean_key(k): v for k, v in mb_results[0].items()}
            at = MBArtistTuple(**cleaned)
            Persistence.persist_mb_metadata(result.id, at)
            _artist.update({"mb_id": at.id, "mb_obj": at._asdict()})
        return _artist

    @staticmethod
    def lyric_links(uri) -> Dict:
        result = Track.query.filter_by(spot_uri=uri).first()
        _track = result.as_dict()
        if result.lyrics is not None:
            candidates = Spotlight.candidates(result.lyrics)
            Persistence.persist_lyrics_links(result.id, candidates)
            _track.update({"lyrics_annotations_json": candidates._asdict()})
        return _track

    @staticmethod
    def lyrics_annotate(uri) -> Dict:
        result = Track.query.filter_by(spot_uri=uri).first()
        _track = result.as_dict()
        if result.lyrics is not None:
            annotated = Spotlight.annotate(result.lyrics)
            Persistence.persist_lyrics_annotated(result.id, annotated)
            _track.update({"lyrics_annotated": annotated})
        return _track

    @staticmethod
    def lyrics_annotations(uri):
        _track = Track.query.filter_by(spot_uri=uri).first()
        return _track.lyrics_annotated

    @staticmethod
    def playlist_tracks(uri: str) -> List[TrackTuple]:
        sp = SpotPlaylist()
        try:
            playlist = sp.download_tracks(uri)
            track_dicts = SpotUtils.extract_tracks_from_playlist(playlist)
            track_tuples = SpotUtils.tuplify_tracks(track_dicts, None)
        except Exception as e:
            print(f"Unable to retrieve playlist {uri} tracks")
            traceback.print_tb(e.__traceback__)
        else:
            return track_tuples

    @staticmethod
    def track(uri: str) -> Dict:
        result = Track.query.filter_by(spot_uri=uri).first()
        _track = result.as_dict()
        _artists = [_artist.as_dict() for _artist in result.artists]
        _album = result.album.as_dict()
        _track.update({"album": _album, "artists": _artists})
        return _track

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
    def tracks() -> List[Dict]:
        return [_track.as_dict() for _track in Track.query.all()]

    @staticmethod
    def text_annotate(text):
        try:
            annotated = Spotlight.annotate(text)
        except Exception as e:
            print(f"Unable to annotate text")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            return annotated

