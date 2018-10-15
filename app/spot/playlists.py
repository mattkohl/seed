from typing import Dict, List
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from app.spot.utils import SpotUtils


logger = logging.getLogger()
console = logging.StreamHandler()
logger.addHandler(console)


class SpotPlaylist:

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def download(self, uri: str) -> Dict:
        logger.info(uri)
        username = uri.split(':')[2]
        playlist_id = uri.split(':')[4]
        pl = self.sp.user_playlist(username, playlist_id)
        return pl

    def extract_tracks(self, uri: str) -> List[Dict]:
        playlist = self.download(uri)
        return [SpotUtils.extract_track(item["track"]) for item in playlist["tracks"]["items"]]
