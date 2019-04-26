from app.spot import playlists


class PlaylistConsumer:

    @staticmethod
    def run(uri: str):
        sp = playlists.SpotPlaylist()
        return sp.extract_tracks(uri)
