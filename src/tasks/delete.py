from typing import Dict
import traceback

from src.models import Track, Artist, Album, Location, Genre
from src.repository.delete import Delete


class Deletion:

    @staticmethod
    def clear():
        message = f"Deleted " \
            f"{Track.query.count()} Tracks, " \
            f"{Artist.query.count()} Artists, " \
            f"{Album.query.count()} Albums, " \
            f"{Genre.query.count()} Genres, & " \
            f"{Location.query.count()} Locations"
        try:
            Delete.clear()
        except Exception as e:
            print(f"Unable to delete everything")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            return {"status": message}

    @staticmethod
    def delete_artist(_id: int) -> None:
        try:
            Delete.delete_artist(_id)
        except Exception as e:
            print(f"Unable to delete artist {_id}")
            traceback.print_tb(e.__traceback__)
            raise

    @staticmethod
    def delete_artist_birthplace(artist_uri: str) -> None:
        try:
            Delete.delete_birthplace(artist_uri)
        except Exception as e:
            print(f"Unable to delete artist {artist_uri} birthplace")
            traceback.print_tb(e.__traceback__)
            raise

    @staticmethod
    def delete_artist_hometown(artist_uri: str) -> None:
        try:
            Delete.delete_hometown(artist_uri)
        except Exception as e:
            print(f"Unable to delete artist {artist_uri} hometown")
            traceback.print_tb(e.__traceback__)
            raise

    @staticmethod
    def delete_track(_id: int) -> Dict:
        try:
            Delete.delete_track(_id)
        except Exception as e:
            print(f"Unable to delete track {_id}")
            traceback.print_tb(e.__traceback__)
            raise
        finally:
            return dict(message=f"Deleted track: {_id}")

    @staticmethod
    def delete_album(_id: int) -> Dict:
        try:
            Delete.delete_album(_id)
        except Exception as e:
            print(f"Unable to delete album {_id}")
            traceback.print_tb(e.__traceback__)
            raise
        finally:
            return dict(message=f"Deleted album: {_id}")

