"""Unit tests for the converter library.
"""
import convertlib.util as util
import unittest
import convertlib
import spotipy
import os
import io
from datetime import date

# TODO: find some place to put this file so we can
# test the convertlib automatically.

SPOTIFY_API_CLIENT_ID = os.environ["SPOTIFY_API_CLIENT_ID"]
SPOTIFY_API_CLIENT_SECRET = os.environ["SPOTIFY_API_CLIENT_SECRET"]

spotify_creds = spotipy.SpotifyClientCredentials(
    client_id=SPOTIFY_API_CLIENT_ID, client_secret=SPOTIFY_API_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=spotify_creds)


class TestPlaylistConverter(unittest.TestCase):
    def test_url_extractor(self):
        """Tests that the URL extractor:
        - correctly extracts IDs from playlist URLs
        - correctly rejects invalid URLs
        - correctly rejects valid URLs that are not Spotify playlist URLs
        """
        playlist_url = "https://open.spotify.com/playlist/1LOp2ieUmspXzw61pQ4LCi?si=0909c61a78814603"
        playlist_id = "1LOp2ieUmspXzw61pQ4LCi"

        self.assertEqual(convertlib.extract_playlist_id_from_url(
            playlist_url), playlist_id)

        def invalidUrl1():
            # valid URL, but not a spotify playlist url
            convertlib.extract_playlist_id_from_url(
                "https://github.com/joek13/wxtj-converter")

        def invalidUrl2():
            # invalid URL
            convertlib.extract_playlist_id_from_url(
                "pavement is a decent indie band")

        def invalidUrl3():
            # valid URL, even a spotify url
            # but this is a track URL, not a playlist url
            convertlib.extract_playlist_id_from_url(
                "https://open.spotify.com/track/11zSKLasyDuRNCKVVMi8os?si=e422ade81d2246be")

        self.assertRaises(ValueError, invalidUrl1)
        self.assertRaises(ValueError, invalidUrl2)
        self.assertRaises(ValueError, invalidUrl3)

    def test_new_playlist_converter(self):
        """Tests that the "new playlist editor" converter works without emitting any warnings
        """
        # makes sure there are no warnings/errors when converting playlist
        playlist_url = "https://open.spotify.com/playlist/1LOp2ieUmspXzw61pQ4LCi?si=0909c61a78814603"
        playlist_id = convertlib.extract_playlist_id_from_url(playlist_url)

        # allocate buffer to contain the converted csv
        buffer = io.StringIO()
        name, warnings = convertlib.write_new_playlist_csv(
            spotify, playlist_id, buffer)

        # make sure there are no warnings
        self.assertEqual(warnings, [])
        # and that the playlist name is correct
        self.assertEqual(name, "songs people wrote about their pets")

    def test_old_playlist_converter(self):
        """Tests that the "old playlist editor" converter works without emitting any warnings
        """
        # makes sure there are no warnings/errors when converting playlist
        playlist_url = "https://open.spotify.com/playlist/1LOp2ieUmspXzw61pQ4LCi?si=0909c61a78814603"
        playlist_id = convertlib.extract_playlist_id_from_url(playlist_url)

        # allocate buffer to contain the converted csv
        buffer = io.StringIO()
        name, warnings = convertlib.write_old_playlist_csv(
            spotify, playlist_id, "hot tub listening club", date.today(), buffer)

        # make sure there are no warnings
        self.assertEqual(warnings, [])
        # and that the playlist name is correct
        self.assertEqual(name, "songs people wrote about their pets")


class TestUtil(unittest.TestCase):
    def test_duration_converter(self):
        """Tests that the duration converter/formatter:
        - correctly formats times longer than one minute
        - correctly formats one minute
        - correctly formats times shorter than one minute
        """
        three_minutes_fortytwo_seconds = 3 * 60 * 1000 + 42 * 1000 + 33
        # three minutes, forty two seconds, 33 ms = 3:42

        self.assertEqual(util._duration_from_ms(
            three_minutes_fortytwo_seconds), (3, 42))

        sixty_seconds = 60 * 1000
        # sixty seconds = one minute = 1:00

        self.assertEqual(util._duration_from_ms(sixty_seconds), (1, 0))

        ten_seconds = 10 * 1000
        # ten seconds = 0:10
        self.assertEqual(util._duration_from_ms(ten_seconds), (0, 10))


if __name__ == "__main__":
    unittest.main()
