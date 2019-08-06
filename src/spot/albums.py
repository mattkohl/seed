import traceback
from typing import Dict, List

from src.models import Album
from src.spot.utils import SpotUtils
from src.spot.oauth2 import SpotifyClientCredentials
from src.spot.client import Spotify


class SpotAlbum:

    client_credentials_manager = SpotifyClientCredentials()
    sp = Spotify(client_credentials_manager=client_credentials_manager)

    def download_album(self, uri: str):
        album_id = uri.split(':')[-1]
        try:
            _album = self.sp.album(album_id)

        except Exception as e:
            print(f"Unable to download album {album_id}")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            print(f"Downloaded album {album_id}")
            return _album

    def download_album_tracks(self, uri: str) -> List[Dict]:
        album_id = uri.split(':')[-1]
        try:
            track_dicts = self.sp.album_tracks(album_id)["items"]
        except Exception as e:
            print(f"Unable to download tracks for {album_id}")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            print(f"Downloaded album tracks {album_id}")
            return track_dicts

    @staticmethod
    def package_tracks(_tracks: List[Dict], _album: Album):

        def add_albums():
            for _track in _tracks:
                _track.update({"album": _album.as_tuple_dict(_album.artists)})
                yield _track

        def _track_tuples():
            for _t in SpotUtils.tuplify_tracks(list(add_albums())):
                if _t is not None:
                    yield _t

        track_tuples = list(_track_tuples())
        return track_tuples
