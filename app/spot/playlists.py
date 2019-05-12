from typing import Dict, List


from app.spot.oauth2 import SpotifyClientCredentials
from app.spot.client import Spotify


class SpotPlaylist:

    client_credentials_manager = SpotifyClientCredentials()
    sp = Spotify(client_credentials_manager=client_credentials_manager)

    def download_tracks(self, uri: str) -> List[Dict]:
        username = uri.split(':')[2]
        playlist_id = uri.split(':')[4]
        try:
            pl = self.sp.user_playlist(username, playlist_id)["tracks"]
        except Exception as e:
            print(f"Unable to download playlist {playlist_id}:", e)
            raise
        else:
            print(f"Downloaded playlist {playlist_id}")
            if pl["next"] is not None:
                print(f"Downloading next page playlist {playlist_id} at {pl['next']}")
                return pl["items"] + self.download_tracks(pl["next"])
            else:
                return pl
