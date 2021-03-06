import traceback
from typing import Dict, List


from src.spot.oauth2 import SpotifyClientCredentials
from src.spot.client import Spotify


class SpotPlaylist:

    client_credentials_manager = SpotifyClientCredentials()
    sp = Spotify(client_credentials_manager=client_credentials_manager)

    def download_playlist_tracks(self, uri: str) -> List[Dict]:
        playlist_id = uri.split(':')[-1]

        def _download_tracks(_playlist_id, offset):
            try:
                pl = self.sp.playlist_tracks(_playlist_id, offset=offset)
            except Exception as e:
                print(f"Unable to download playlist {_playlist_id}:")
                traceback.print_tb(e.__traceback__)
                raise
            else:
                print(f"Downloaded playlist {_playlist_id}")
                if pl["next"] is not None:
                    _next = pl['offset'] + pl['limit']
                    print(f"Downloading next page playlist {pl['next']}")
                    return pl["items"] + _download_tracks(_playlist_id, offset=_next)
                else:
                    return pl["items"]
        return _download_tracks(playlist_id, 0)
