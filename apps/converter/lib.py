"""Library methods for interacting with the Spotify API.
"""

import re
import spotipy
import typing
import csv

from django.core import validators
from django.conf import settings

from spotipy.oauth2 import SpotifyClientCredentials

SPOTIFY_PLAYLIST_URL_REGEX = re.compile(
    r"(?:http|https)://open\.spotify\.com/playlist/([^?]+)(?:\?.+)", re.IGNORECASE)
"""Regular expression that matches URLs for Spotify playlist links and extracts their IDs
"""

cred_manager = SpotifyClientCredentials(
    client_id=settings.SPOTIFY_API_CLIENT_ID,
    client_secret=settings.SPOTIFY_API_CLIENT_SECRET
)
spotify = spotipy.Spotify(client_credentials_manager=cred_manager)


def validate_spotify_playlist_url(url: str) -> bool:
    """Validates a given URL to check if it is valid for a Spotify playlist.

    Args:
        url (str): Playlist URL to validate.

    Returns:
        bool: True if and only if the URL represents a valid spotify playlist.
    """
    # first: check if string is valid URL

    # this check is redundant if embedded in a form that uses URLField,
    # but probably a good idea to keep here anyway
    # hooray for idiot-proofing!
    url_validator = validators.URLValidator(["http", "https"])
    try:
        url_validator(url)
    except validators.ValidationError:
        return False

    # run it through our regex
    return SPOTIFY_PLAYLIST_URL_REGEX.match(url)


def extract_spotify_playlist_id(url: str) -> str:
    """Extracts the playlist id from a Spotify playlist URL.

    Args:
        url (str): URL of the playlist.

    Returns:
        str: The playlist id as extracted from the URL.
    """
    match = SPOTIFY_PLAYLIST_URL_REGEX.findall(url)
    if match:
        return match[0]
    else:
        raise ValueError("Argument url must be a valid Spotify playlist URL.")


def _duration_from_ms(duration_ms: int) -> typing.Tuple[int, int]:
    """Converts a duration in milliseconds to a tuple of 2 ints: minutes, seconds

    Args:
        duration_ms (int): The number of milliseconds in this duration.

    Returns:
        typing.Tuple[int, int]: int 2-tuple of the form (minutes, seconds)
    """
    minutes = 0
    seconds = 0

    # keep removing minute increments, while we can
    while duration_ms >= 60 * 1000:
        minutes += 1
        duration_ms -= 60 * 1000

    # keep removing second increments, while we can
    while duration_ms >= 1000:
        seconds += 1
        duration_ms -= 1000

    return (minutes, seconds)


def write_playlist_csv(url: str, stream: typing.TextIO):
    """Gets the playlist from a url, formats it as a csv file, and writes the csv to a given stream.

    Args:
        url (str): The url to get a playlist from.
        stream (typing.TextIO): The stream to write the playlist CSV to. Can be a file, a StringIO, etc.
    """
    writer = csv.writer(stream)  # create csvwriter around stream
    # write standard WXTJ header row
    # TODO: investigate why this header is nothing like the actual playlist editor headers
    writer.writerow(["title", "title_url", "duration", "performer", "performer_url",
                     "album", "album_url", "released", "label", "composer", "composer_url", "notes"])

    # fetch the playlist id
    playlist_id = extract_spotify_playlist_id(url)

    # get the items on the playlist
    playlist_items = spotify.playlist_items(playlist_id)

    for item in playlist_items["items"]:
        # fetch relevant variables
        track = item["track"]
        artist = track["artists"][0]  # just get the first artist on the track
        track_name = track["name"]

        album = track["album"]  # get album info
        album_name = album["name"]  # name of the album
        artist_name = artist["name"]  # name of the artist

        album_ext = spotify.album(album["id"])  # get additional info for album
        label = album_ext["label"]  # record label that published the album
        # get the first four chars of release date
        release_year = album["release_date"][0:4]

        duration_ms = int(track["duration_ms"])
        duration_minutes, duration_seconds = _duration_from_ms(duration_ms)

        # pad out seconds so (3, 2) -> "3:02"
        duration_str = f"{duration_minutes}:{str(duration_seconds).zfill(2)}"

        row = [
            track_name,
            duration_str,
            artist_name,
            album_name,
            release_year,
            label,
            "",
            ""
        ]

        writer.writerow(row)
