from typing import Dict, List
import os
import ast
import time

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from app.spot.utils import SpotUtils


class SpotPlaylist:

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    cache = "spot/resources"

    def cached(self, filename: str) -> bool:
        already_there = os.listdir(self.cache)
        if filename in already_there:
            file_mod_time = os.stat(f"{self.cache}/{filename}").st_mtime
            last_mod = (time.time() - file_mod_time) / 60 / 60
            if last_mod < 24:
                return True
        return False

    def open_cached(self, fn: str) -> Dict:
        with open(f"{self.cache}/{fn}") as f:
            lines = f.readlines()
            return ast.literal_eval("\n".join(lines))

    def cache_response(self, fn: str, txt: str) -> None:
        with open(f"{self.cache}/{fn}", "w") as f:
            f.write(str(txt))

    def download(self, uri: str) -> Dict:
        username = uri.split(':')[2]
        playlist_id = uri.split(':')[4]
        pl = self.sp.user_playlist(username, playlist_id)
        return pl

    def extract_tracks(self, uri: str) -> List[Dict]:
        playlist = self.download(uri)
        return [SpotUtils.extract_track(item["track"]) for item in playlist["tracks"]["items"]]


if __name__ == "__main__":
    from pprint import pprint
    test_uri = "spotify:user:matt.kohl-gb:playlist:2d1Q2cY735lRoXC8cC6DDJ"
    sp = SpotPlaylist()
    pprint(sp.extract_tracks(test_uri))
