"""Library methods for interacting with the Spotify API.
"""

from django.core import validators
import re

SPOTIFY_PLAYLIST_URL_REGEX = re.compile(
    r"(?:http|https)://open\.spotify\.com/playlist/([^?]+)(?:\?.+)", re.IGNORECASE)
"""Regular expression that matches URLs for Spotify playlist links and extracts their IDs
"""


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
