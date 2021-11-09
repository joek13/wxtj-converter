"""Library methods for interacting with the Spotify API.
"""

import re
import spotipy
import typing
import csv
import enum

from django.core import validators
from django.conf import settings

from spotipy.oauth2 import SpotifyClientCredentials

SPOTIFY_PLAYLIST_URL_REGEX = re.compile(
    r"(?:http|https)://open\.spotify\.com/playlist/([^?]+)(?:\?.+)?", re.IGNORECASE)
"""Regular expression that matches URLs for Spotify playlist links and extracts their IDs
"""

cred_manager = SpotifyClientCredentials(
    client_id=settings.SPOTIFY_API_CLIENT_ID,
    client_secret=settings.SPOTIFY_API_CLIENT_SECRET
)
spotify = spotipy.Spotify(client_credentials_manager=cred_manager)


class OutputFormat(enum.Enum):
    """Enum whose values represent the possible output formats for the converter.
    """

    NEW_PLAYLIST_EDITOR = "NEW"
    """
    Format for the WTJU "new" playlist editor.
    """
    OLD_PLAYLIST_EDITOR = "OLD"
    """
    Format for the WTJU "old" playlist editor.
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


def get_playlist_name(url: str) -> str:
    """Gets the name of a playlist from its url.

    Args:
        url (str): The url of the playlist to get a name from.

    Returns:
        str: The name of the playlist indicated.
    """
    # fetch the playlist id
    playlist_id = extract_spotify_playlist_id(url)
    # return just the name field
    playlist = spotify.playlist(playlist_id, fields=["name"])
    return playlist["name"]


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


def write_playlist_csv(url: str, stream: typing.TextIO, format: OutputFormat = OutputFormat.NEW_PLAYLIST_EDITOR) -> typing.List[str]:
    """Gets the playlist from a url, formats it as a csv file, and writes the csv to a given stream.

    Args:
        url (str): The url to get a playlist from.
        stream (typing.TextIO): The stream to write the playlist CSV to. Can be a file, a StringIO, etc.
        format (OutputFormat): Output format for the .csv playlist file.

    Returns:
        warnings (typing.List[str]): A list-like of strings describing any pertinent warnings.
    """
    writer = csv.writer(stream)  # create csvwriter around stream
    warnings = []
    # write standard WXTJ header row
    if format == OutputFormat.NEW_PLAYLIST_EDITOR:
        writer.writerow(["title", "duration", "performer", "album",
                         "year", "label", "composer", "notes"])
    elif format == OutputFormat.OLD_PLAYLIST_EDITOR:
        writer.writerow(["title", "title_url", "duration", "performer", "performer_url",
                         "album", "album_url", "released", "label", "composer", "composer_url", "notes"])
    else:
        raise ValueError(f"Unrecognized output format {format}")

    # fetch the playlist id
    playlist_id = extract_spotify_playlist_id(url)

    # get the items on the playlist
    playlist_items = spotify.playlist_items(playlist_id)

    for item in playlist_items["items"]:
        # fetch relevant variables
        track = item["track"]
        # is this track local? (imported from personal library)
        is_local_track = track["is_local"]
        artist = track["artists"][0]  # just get the first artist on the track
        track_name = track["name"]

        album = track["album"]  # get album info
        album_name = album["name"]  # name of the album
        artist_name = artist["name"]  # name of the artist

        label = None
        release_year = None
        # we can only get additional album info on non-local tracks.
        # Spotify doesn't carry extended album info for imports from
        # local library.
        if not is_local_track:
            # get additional info for album
            album_ext = spotify.album(album["id"])
            label = album_ext["label"]  # record label that published the album
            # get the first four chars of release date
            release_year = album["release_date"][0:4]
        else:
            # we can't get this info ourselves, so it'll just have to be filled in manually.
            # TODO: music database?
            label = ""
            release_year = ""
            # add warning
            warnings.append(
                f"Track '{track_name}' was imported from your library, so I can't find its record label or release year automatically. Other fields for this song may be missing or incomplete. You'll have to enter this track's information into the station's interface manually.")

        duration_ms = int(track["duration_ms"])
        duration_minutes, duration_seconds = _duration_from_ms(duration_ms)

        # pad out seconds so (3, 2) -> "3:02"
        duration_str = f"{duration_minutes}:{str(duration_seconds).zfill(2)}"

        if format == OutputFormat.NEW_PLAYLIST_EDITOR:
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
        elif format == OutputFormat.OLD_PLAYLIST_EDITOR:
            row = [
                track_name,  # track title
                "",  # title_url
                duration_str,  # duration
                artist_name,  # performer
                "",  # performer_url
                album_name,  # album
                "",  # album_url
                release_year,  # released
                label,  # label
                "",  # composer
                "",  # composer url
                ""  # notes
            ]
        else:
            raise ValueError(f"Unrecognized output format {format}")

        writer.writerow(row)

    return warnings
