from typing import Dict, List
import re


class SpotUtils:

    @staticmethod
    def extract_album(raw: Dict) -> Dict:
        """
        available keys: 'album_type', 'artists', 'available_markets', 'external_urls', 'href', 'id', 'images', 'name', 'release_date', 'release_date_precision', 'total_tracks', 'type', 'uri'
        """
        return {"title": raw["name"], "release_date": raw["release_date"], "uri": raw["uri"]}

    @staticmethod
    def extract_artist(raw: Dict) -> Dict:
        """
        available keys: 'external_urls', 'href', 'id', 'name', 'type', 'uri'
        """
        return {"name": raw["name"], "uri": raw["uri"]}

    @staticmethod
    def extract_track(raw: Dict) -> Dict:
        """
        available keys: 'album', 'artists', 'available_markets', 'disc_number', 'duration_ms', 'episode', 'explicit', 'external_ids', 'external_urls', 'href', 'id', 'is_local', 'name', 'popularity', 'preview_url', 'track', 'track_number', 'type', 'uri'
        """
        return {
            "title": raw["name"],
            "uri": raw["uri"],
            "popularity": raw["popularity"],
            "album": SpotUtils.extract_album(raw["album"]),
            "artists": [SpotUtils.extract_artist(a) for a in raw["artists"]]
        }


class GenUtils:

    @staticmethod
    def slugify(text: str) -> str:
        slug = text.strip().lower()
        slug = slug[1:] if slug[0] == "'" or slug[0] == "-" else slug
        slug = re.sub("^[\-']]", "", slug)
        slug = re.sub("\s", "-", slug)
        slug = re.sub("\.", "", slug)
        slug = re.sub("[:/]", "", slug)
        slug = re.sub("\$", "-", slug)
        slug = re.sub("\*", "", slug)
        slug = re.sub("#", "number", slug)
        slug = re.sub("%", "percent", slug)
        slug = re.sub("&amp;", "and", slug)
        slug = re.sub("&", "and", slug)
        slug = re.sub("\+", "and", slug)
        slug = re.sub("é", "e", slug)
        slug = re.sub("ó", "o", slug)
        slug = re.sub("á", "a", slug)
        slug = re.sub("@", "at", slug)
        slug = re.sub("½", "half", slug)
        slug = re.sub("ō", "o", slug)
        slug = re.sub("'", "", slug)
        slug = re.sub(",", "", slug)
        slug = re.sub("-$", "", slug)
        slug = re.sub("\?", "", slug)
        slug = re.sub("[()]", "", slug)
        slug = re.sub("\s-", "-", slug)
        return slug

    @staticmethod
    def link(artist: str, song_title: str) -> str:
        h = "https"
        g = "genius"
        c = "com"
        artist = "The " + artist[:-4] if artist.endswith(", The") else artist
        slug = GenUtils.slugify(artist + " " + song_title + "_lyrics")
        return f"{h}://{g}.{c}/{slug}"
