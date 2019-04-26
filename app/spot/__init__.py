from . import playlists


class PlaylistConsumer:

    sp = playlists.SpotPlaylist()

    def run(self, uri: str):
        tracks = self.sp.extract_tracks(uri)
        for track in tracks:
            for artist in track["artists"]:
                yield artist
            yield track
