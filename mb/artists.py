from typing import Dict, List

import musicbrainzngs as mb


class MBArtist:

    mb.set_useragent("seed-trr", 0.1)

    @staticmethod
    def search(name: str) -> List[Dict]:
        """
        available keys: 'id', 'type', 'ext:score', 'name', 'sort-name', 'gender', 'life-span'
        """
        return mb.search_artists(artist=name)["artist-list"]


if __name__ == "__main__":
    from pprint import pprint
    test_name = "pete rock cl smooth"
    mba = MBArtist()
    result = mba.search(test_name)
    pprint(result)
