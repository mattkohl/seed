from datetime import datetime
from typing import Dict, Optional, List

from app.dbp.annotation import Spotlight
from app.dbp.models import CandidatesTuple
from app.geni import parser, utils
from app.mb import metadata
from app.mb.models import ArtistTuple as MBArtistTuple
from app.models import Artist, Track, Album
from app.spot.albums import SpotAlbum
from app.spot.artists import SpotArtist
from app.spot.playlists import SpotPlaylist
from app.tasks.persist import TasksPersist
from app.utils import Utils


class Fetch:

    @staticmethod
    def playlist_tracks(uri: str) -> Dict:
        sp = SpotPlaylist()
        return sp.download_tracks(uri)

    @staticmethod
    def artist_albums(uri: str) -> List[Dict]:
        sp = SpotArtist()
        return sp.download_albums(uri)

    @staticmethod
    def album_tracks(uri: str) -> List[Dict]:
        sp = SpotAlbum()
        return sp.download_tracks(uri)

    # FIXME!!
    @staticmethod
    def artist_dbp_uri(uri: str) -> Dict:
        result = Artist.query.filter_by(spot_uri=uri).first()
        _artist = result.as_dict()
        try:
            candidates = Fetch.artist_and_track_name_annotations(uri)
            potentials = [resource for resource in candidates.Resources if "DBpedia:MusicalArtist" in resource['@types'].split(",")]
            dbp_uri = potentials[0]["@URI"] if potentials and Utils.fuzzy_match(result.name, potentials[0]["@URI"].split("/")[-1]) else None
            TasksPersist.persist_dbp_uri(result.id,  dbp_uri)
        except Exception as e:
            print(f"Could not get DBP URI for {result.name}", e)
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
    def artist_and_track_name_annotations(artist_uri: str) -> CandidatesTuple:
        _artist = Artist.query.filter_by(spot_uri=artist_uri).first()
        _albums = [_album for _album in _artist.albums if len(_album.artists) == 1]
        _statements = set([f""" {_album.name} in {_album.release_date_string[:4]}""" for _album in _albums])
        message = f"{_artist.name}, the hip-hop artist, released the albums" + ", \n".join(_statements)
        print(message)
        return Spotlight.candidates(message)
