from typing import Dict, List, Optional
from datetime import datetime
from flask import json
from requests import Response

from app.dbp.annotation import Spotlight
from app.dbp.models import CandidatesTuple
from app.geni import utils, parser
from app.models import Track, Artist
from app.persist.persist import Persist
from app.spot.models import TrackTuple
from app.spot.playlists import SpotPlaylist
from app.spot.utils import SpotUtils
from app.mb import metadata
from app.mb.models import ArtistTuple
from app.utils import Utils


class Tasks:

    @staticmethod
    def get_playlist_tracks(uri: str) -> Dict:
        sp = SpotPlaylist()
        return sp.download(uri)

    @staticmethod
    def extract_tracks_from_playlist(playlist: Dict) -> List[Dict]:
        return SpotUtils.extract_tracks(playlist)

    @staticmethod
    def tuplify_tracks(track_dicts: List[Dict]) -> List[TrackTuple]:
        return [Tasks.tuplify_track(track_dict) for track_dict in track_dicts]

    @staticmethod
    def tuplify_track(d: Dict) -> TrackTuple:
        _track = SpotUtils.extract_track(d)
        _album = _track.album._asdict()
        _artists = [_artist._asdict() for _artist in _track.artists]
        _updated = _track._replace(artists=_artists, album=_album)
        return _track

    @staticmethod
    def dump_track_tuple_to_json(track_tuple: TrackTuple):
        yield json.dumps(track_tuple._asdict(), indent=2, separators=(', ', ': '))

    @staticmethod
    def persist_track(track_tuple: TrackTuple) -> None:
        Persist.persist_track(track_tuple)

    @staticmethod
    def generate_lyrics_url(artists: List[str], title: str) -> str:
        return utils.GenUtils.link(artists, title)

    @staticmethod
    def get_lyrics(url) -> Optional[str]:
        return parser.GenParser.download(url)

    @staticmethod
    def persist_lyrics(track_id: int, lyrics: Optional[str], url: str, fetched) -> None:
        _track = Track.query.filter_by(id=track_id).first()
        if lyrics:
            _updates = {Track.lyrics: lyrics, Track.lyrics_url: url, Track.lyrics_fetched_timestamp: fetched}
            Persist.update_track(_track.id, _updates)

    @staticmethod
    def persist_dbp_uri(artist_id: int, dbp_uri: Optional[str]) -> None:
        _artist = Track.query.filter_by(id=artist_id).first()
        if dbp_uri:
            _updates = {Artist.dbp_uri: dbp_uri}
            Persist.update(Artist, _artist.id, _updates)

    @staticmethod
    def persist_mb_metadata(artist_id: int, artist_tuple: ArtistTuple) -> None:
        _artist = Track.query.filter_by(id=artist_id).first()
        _updates = {Artist.mb_id: artist_tuple.id, Artist.mb_obj: artist_tuple._asdict()}
        Persist.update(Artist, _artist.id, _updates)

    @staticmethod
    def run_playlist(playlist_uri) -> List[Dict]:
        playlist = Tasks.get_playlist_tracks(playlist_uri)
        track_dicts = Tasks.extract_tracks_from_playlist(playlist)
        track_tuples = Tasks.tuplify_tracks(track_dicts)
        [Tasks.persist_track(t) for t in track_tuples]
        track_dicts = [t._asdict() for t in track_tuples]
        return track_dicts

    @staticmethod
    def scrape_all_lyrics() -> List[Dict]:
        return [Tasks.scrape_track_lyrics(_track.spot_uri) for _track in Track.query.filter_by(lyrics=None).all()]

    @staticmethod
    def scrape_track_lyrics(uri: str) -> Dict:
        result = Track.query.filter_by(spot_uri=uri).first()
        _track = result.as_dict()
        _artists = [_artist.as_dict() for _artist in result.artists]
        _album = result.album.as_dict()
        _track.update({"album": _album, "artists": _artists})
        url = Tasks.generate_lyrics_url([_artist.name for _artist in result.artists], result.name)
        try:
            lyrics = Tasks.get_lyrics(url)
        except Exception as e:
            print(f"Could not connect to {url}: {e}")
            return {"error": f"Could not connect to {url}: {e}"}
        else:
            fetched = datetime.now()
            Tasks.persist_lyrics(result.id, lyrics, url, fetched)
            _track.update({"lyrics": lyrics, "lyrics_url": url, "lyrics_fetched_timestamp": fetched})
            return _track

    @staticmethod
    def extract_candidate_links_from_track(uri) -> Optional[CandidatesTuple]:
        _track = Track.query.filter_by(spot_uri=uri).first()
        return Spotlight.candidates(_track.lyrics)

    @staticmethod
    def annotate_track(uri) -> Response:
        _track = Track.query.filter_by(spot_uri=uri).first()
        return Spotlight.annotate(_track.lyrics)

    @staticmethod
    def annotate_artist_and_track_names(artist_uri: str) -> Optional[CandidatesTuple]:
        _artist = Artist.query.filter_by(spot_uri=artist_uri).first()
        _statements = [f"""On {_track.album.release_date.strftime('%d %b, %Y')} {_artist.name} released the hip-hop song, "{_track.name}" """ for _track in _artist.tracks]
        message = "\n".join(_statements)
        return Spotlight.candidates(message)

    @staticmethod
    def get_artist_dbp_uri(uri: str) -> Dict:
        result = Artist.query.filter_by(spot_uri=uri).first()
        _artist = result.as_dict()
        if result.dbp_uri is None:
            try:
                candidates = Tasks.annotate_artist_and_track_names(uri)
                dbp_uri = candidates.Resources[0]["@URI"]
                Tasks.persist_dbp_uri(result.id,  dbp_uri)
            except Exception as e:
                print(f"Could not get DBP URI for {result.name}")
            else:
                _artist.update({"dbp_uri": dbp_uri})
        return _artist

    @staticmethod
    def get_artist_mb_metadata(uri: str) -> Optional[ArtistTuple]:
        result = Artist.query.filter_by(spot_uri=uri).first()
        _artist = result.as_dict()
        if result.mb_id is None:
            try:
                mb_results = metadata.MBArtist().search(result.name)
                assert mb_results[0]["ext:score"] == "100"
            except Exception as e:
                print(f"Could not get MB metadata for {result.name}: {e}")
            else:
                cleaned = {Utils.clean_key(k): v for k, v in mb_results[0].items()}
                at = ArtistTuple(**cleaned)
                Tasks.persist_mb_metadata(result.id, at)
                _artist.update({"mb_id": at.id, "mb_obj": at._asdict()})
        return _artist

