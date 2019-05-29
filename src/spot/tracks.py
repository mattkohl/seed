import traceback
from typing import Dict

from src.spot.oauth2 import SpotifyClientCredentials
from src.spot.client import Spotify


class SpotTrack:

    client_credentials_manager = SpotifyClientCredentials()
    sp = Spotify(client_credentials_manager=client_credentials_manager)

    def download_track(self, uri: str) -> Dict:
        track_id = uri.split(':')[-1]
        try:
            track_dict = self.sp.track(track_id)
        except Exception as e:
            print(f"Unable to download track {track_id}")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            print(f"Downloaded track {track_id}")
            return track_dict