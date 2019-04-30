from app.spot import playlists


class Consumer:

    @staticmethod
    def playlist_tracks(playlist_uri: str):
        sp = playlists.SpotPlaylist()
        return sp.extract_tracks(playlist_uri)
