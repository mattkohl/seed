import traceback
from typing import Dict, List

import musicbrainzngs as mb


class MB:

    mb.set_useragent("seed-trr", 0.1)

    @staticmethod
    def search_artists(name: str) -> List[Dict]:
        """
        available keys: 'id', 'type', 'ext:score', 'name', 'sort-name', 'gender', 'life-span'
        """
        try:
            _metadata = mb.search_artists(artist=name)["artist-list"]
            _ = _metadata[0]["ext:score"] == "100"
        except Exception as e:
            print(f"Unable to retrieve MB metadata for {name}")
            traceback.print_tb(e.__traceback__)
            return list()
        else:
            return _metadata[0].items()

    @staticmethod
    def get_albums_with_artist_id(mb_id: str) -> List[Dict]:
        try:
            _metadata = mb.browse_release_groups(artist=mb_id)["release-group-list"]
        except Exception as e:
            print(f"Unable to retrieve MB metadata for {mb_id}")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            return _metadata

    @staticmethod
    def get_tracks_with_album_id(mb_id: str) -> List[Dict]:
        try:
            _metadata = mb.browse_releases(release_group=mb_id)["release-list"]
        except Exception as e:
            print(f"Unable to retrieve MB metadata for {mb_id}")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            return _metadata

