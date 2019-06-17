from unittest import TestCase

from src.geni.utils import GenUtils
from src.models import Artist, Track


class TestUtils(TestCase):

    def test_link_bonus_track(self):
        a = Artist(name="Atmosphere")
        result = Track(name="Idiot - Bonus Track")
        result.primary_artists.extend([a])
        _artists = result.primary_artists if len(result.primary_artists) > 0 else result.featured_artists
        url = GenUtils.link([_artist.name for _artist in _artists], result.name)
        self.assertTrue(url.endswith("/atmosphere-idiot-lyrics"))

    def test_link_chopped_and_feat(self):
        a = Artist(name="Z-Ro")
        result = Track(name="Sunshine - Chopped (feat. Lil’ Keke)")
        result.featured_artists.extend([a])
        _artists = result.primary_artists if len(result.primary_artists) > 0 else result.featured_artists
        url = GenUtils.link([_artist.name for _artist in _artists], result.name)
        self.assertTrue(url.endswith("/z-ro-sunshine-lyrics"))

    def test_link_slabed(self):
        a = Artist(name="Z-Ro")
        result = Track(name="Swagger Like Us (G Mix) - S.L.A.B - Ed")
        result.featured_artists.extend([a])
        _artists = result.primary_artists if len(result.primary_artists) > 0 else result.featured_artists
        url = GenUtils.link([_artist.name for _artist in _artists], result.name)
        print(url)
        self.assertTrue(url.endswith("/z-ro-swagger-like-us-g-mix-lyrics"))

    def test_link_slabed_2(self):
        a = Artist(name="Z-Ro")
        result = Track(name="Slabed - Still Watchin")
        result.featured_artists.extend([a])
        _artists = result.primary_artists if len(result.primary_artists) > 0 else result.featured_artists
        url = GenUtils.link([_artist.name for _artist in _artists], result.name)
        self.assertTrue(url.endswith("/z-ro-still-watchin-lyrics"))
