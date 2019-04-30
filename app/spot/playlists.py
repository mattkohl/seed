from typing import Dict, List
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from app.spot.models import TrackTuple
from app.spot.utils import SpotUtils


class SpotPlaylist:

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def download(self, uri: str) -> Dict:
        username = uri.split(':')[2]
        playlist_id = uri.split(':')[4]
        try:
            pl = self.sp.user_playlist(username, playlist_id)
        except Exception as e:
            logging.error(f"Unable to download playlist {playlist_id}: {e}")
            return dict()
        else:
            logging.info(f"Downloaded playlist {playlist_id}")
            return pl

    def extract_tracks(self, uri: str) -> List[TrackTuple]:
        playlist = self.download(uri)
        for item in playlist["tracks"]["items"]:
            yield SpotUtils.extract_track(item["track"])
