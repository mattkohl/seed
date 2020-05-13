import traceback
import requests


class GeniAlbum:

    @staticmethod
    def download_album(uri: str) -> requests.Response:
        try:
            page = requests.get(uri)

        except Exception as e:
            print(f"Unable to download album {uri}")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            print(f"Downloaded album {uri}")
            return page
