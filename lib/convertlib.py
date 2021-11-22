"""Tiny library for converting Spotify playlists to WXTJ/WTJU's format for the playlist editor.
"""

import validators
import re


SPOTIFY_PLAYLIST_URL_VALIDATOR = re.compile(
    r"(?:http|https)://open\.spotify\.com/playlist/([^?]+)(?:\?.+)?", re.IGNORECASE)
"""Regex for validating Spotify playlist URLs, and extracting the ID from them
"""

NEW_EDITOR_HEADERS = [
    "title",  # track title
    "duration",  # track duration mm:ss
    "performer",  # track artist
    "album",  # alubm title
    "year",  # release year
    "label",  # record label
    "composer",  # track composer
    "notes"  # generic notes
]
""".csv headers for WTJU's new playlist editor
"""

OLD_EDITOR_HEADERS = [
    "title",  # track title
    "title_url",  # URL to the track
    "duration",  # track duration mm:ss
    "performer",  # track artist
    "performer_url",  # URL to the artist
    "album",  # album title
    "album_url",  # URL to the album
    "released",  # release year
    "label",  # record label
    "composer",  # track composer
    "composer_url",  # URL to the composer
    "notes"  # notes
]
""".csv headers for WTJU's old playlist editor
"""


def extract_playlist_id_from_url(url: str) -> str:
    """Extracts Spotify playlist ID from its URL.

    Args:
        url (str): URL to the Spotify playlist.

    Returns:
        str: The playlist ID extracted from the URL.

    Raises:
        ValueError: if url is not a valid Spotify playlist URL.
    """
    if validators.url(url):
        match = SPOTIFY_PLAYLIST_URL_VALIDATOR.findall(url)

        if match:
            return match[0]
        else:
            raise ValueError(
                "Argument url must be a valid Spotify playlist URL")
    else:
        raise ValueError("Argument url must be a valid URl")
