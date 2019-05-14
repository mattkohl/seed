import traceback
from typing import Dict, List

import musicbrainzngs as mb


class MBArtist:

    mb.set_useragent("seed-trr", 0.1)

    @staticmethod
    def search(name: str) -> List[Dict]:
        """
        available keys: 'id', 'type', 'ext:score', 'name', 'sort-name', 'gender', 'life-span'
        """
        try:
            _metadata = mb.search_artists(artist=name)["artist-list"]
            assert _metadata[0]["ext:score"] == "100"
        except Exception as e:
            print(f"Unable to retrieve MB metadata for {name}")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            return _metadata
