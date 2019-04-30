from app.spot import playlists, artists


class Consumer:

    @staticmethod
    def playlist_tracks(playlist_uri: str):
        sp = playlists.SpotPlaylist()
        return sp.extract_tracks(playlist_uri)

    @staticmethod
    def artist_albums(artist_uri: str):
        sp = artists.SpotArtist()
        return sp.extract_albums(artist_uri)
