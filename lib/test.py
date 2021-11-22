import unittest
import convertlib
import spotipy
import os

SPOTIFY_API_CLIENT_ID = os.environ["SPOTIFY_API_CLIENT_ID"]
SPOTIFY_API_CLIENT_SECRET = os.environ["SPOTIFY_API_CLIENT_SECRET"]

spotify_creds = spotipy.SpotifyClientCredentials(
    client_id=SPOTIFY_API_CLIENT_ID, client_secret=SPOTIFY_API_CLIENT_SECRET)
spotify = spotipy.Spotify(auth=spotify_creds)


class TestPlaylistConverter(unittest.TestCase):
    def test_url_extractor(self):
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
    pass


if __name__ == "__main__":
    unittest.main()
