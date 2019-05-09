from datetime import datetime
from typing import Dict, Optional

from app.dbp.annotation import Spotlight
from app.dbp.models import CandidatesTuple
from app.geni import parser, utils
from app.mb import metadata
from app.mb.models import ArtistTuple as MBArtistTuple
from app.models import Artist, Track
from app.spot.albums import SpotAlbum
from app.spot.playlists import SpotPlaylist
from app.tasks.persist import TasksPersist
from app.utils import Utils


class Fetch:

    @staticmethod
    def playlist_tracks(uri: str) -> Dict:
        sp = SpotPlaylist()
        return sp.download(uri)

    @staticmethod
    def album_tracks(uri: str) -> Dict:
        sp = SpotAlbum()
        return sp.download_tracks(uri)

    @staticmethod
    def artist_dbp_uri(uri: str) -> Dict:
        result = Artist.query.filter_by(spot_uri=uri).first()
        _artist = result.as_dict()
        if result.dbp_uri is None:
            try:
                candidates = Fetch.artist_and_track_name_annotations(uri)
                dbp_uri = candidates.Resources[0]["@URI"]
                TasksPersist.persist_dbp_uri(result.id,  dbp_uri)
            except Exception:
                print(f"Could not get DBP URI for {result.name}")
                raise
            else:
                _artist.update({"dbp_uri": dbp_uri})
        return _artist

    @staticmethod
    def artist_mb_metadata(uri: str) -> Optional[MBArtistTuple]:
        result = Artist.query.filter_by(spot_uri=uri).first()
        _artist = result.as_dict()
        if result.mb_id is None:
            try:
                mb_results = metadata.MBArtist().search(result.name)
                assert mb_results[0]["ext:score"] == "100"
            except Exception as e:
                print(f"Could not get MB metadata for {result.name}:", e)
            else:
                cleaned = {Utils.clean_key(k): v for k, v in mb_results[0].items()}
                at = MBArtistTuple(**cleaned)
                TasksPersist.persist_mb_metadata(result.id, at)
                _artist.update({"mb_id": at.id, "mb_obj": at._asdict()})
        return _artist

    @staticmethod
    def track_lyrics(uri: str) -> Dict:
        result = Track.query.filter_by(spot_uri=uri).first()
        _track = result.as_dict()
        _artists = [_artist.as_dict() for _artist in result.artists]
        _album = result.album.as_dict()
        _track.update({"album": _album, "artists": _artists})
        url = utils.GenUtils.link([_artist.name for _artist in result.artists], result.name)
        try:
            lyrics = parser.GenParser.download(url)
        except Exception as e:
            print(f"Could not connect to {url}:", e)
            raise
        else:
            fetched = datetime.now()
            TasksPersist.persist_lyrics(result.id, lyrics, url, fetched)
            _track.update({"lyrics": lyrics, "lyrics_url": url, "lyrics_fetched_timestamp": fetched})
            return _track

    @staticmethod
    def lyric_links(uri) -> Dict:
        result = Track.query.filter_by(spot_uri=uri).first()
        _track = result.as_dict()
        if result.lyrics is not None:
            try:
                candidates = Spotlight.candidates(result.lyrics)
                TasksPersist.persist_lyrics_links(result.id, candidates)
                _track.update({"lyrics_annotations_json": candidates._asdict()})
            except Exception as e:
                print(f"Could not extract links for {uri}:", e)
                raise
        return _track

    @staticmethod
    def lyric_annotations(uri) -> Dict:
        result = Track.query.filter_by(spot_uri=uri).first()
        _track = result.as_dict()
        if result.lyrics is not None:
            try:
                annotated = Spotlight.annotate(result.lyrics)
                TasksPersist.persist_lyrics_annotated(result.id, annotated)
                _track.update({"lyrics_annotated": annotated})
            except Exception as e:
                print(f"Could not annotate to {uri}:", e)
                raise
        return _track

    @staticmethod
    def artist_and_track_name_annotations(artist_uri: str) -> Optional[CandidatesTuple]:
        _artist = Artist.query.filter_by(spot_uri=artist_uri).first()
        _statements = [f"""{_track.name} is a song by the hip-hop group {_artist.name}, released in {_track.album.release_date.strftime('%b, %Y')} on the album {_track.album.name}""" for _track in _artist.tracks]
        message = "\n".join(_statements)
        return Spotlight.candidates(message)