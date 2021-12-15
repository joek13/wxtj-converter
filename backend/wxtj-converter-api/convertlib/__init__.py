"""Tiny library for converting Spotify playlists to WXTJ/WTJU's format for the playlist editor.
"""

import validators
import typing
import csv
import spotipy
from datetime import date
from . import util
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
    # confirm that the url argument is actually a URL
    if validators.url(url):
        # confirm that it is a spotify playlist URL
        match = SPOTIFY_PLAYLIST_URL_VALIDATOR.findall(url)

        if match:
            return match[0]  # ... and extract the ID portion of the URL
        else:
            raise ValueError(
                "Argument url must be a valid Spotify playlist URL")
    else:
        raise ValueError("Argument url must be a valid URl")


def _get_bulk_album_info(spotify: spotipy.Spotify, playlist_items: typing.List) -> typing.Dict[str, typing.Dict]:
    """Uses the 'get several albums' endpoint to fetch the playlist items' album info all at once.

    Args:
        spotify (spotipy.Spotify): Spotify API client instance.
        playlist_items (typing.List): List of playlist items, as returned from spotify.playlist_items

    Returns:
        typing.Dict[typing.String, typing.Dict]: Mapping from album ID to album info objects.
    """
    album_ids = [
        # get the album ID of all tracks in the playlist,
        item["track"]["album"]["id"] for item in playlist_items["items"]
        # provided that:
        # - they are actually tracks
        # - and they are not local tracks
        if item["track"] is not None and not item["track"]["is_local"]
    ]

    albums = {}

    # the 'get several albums' endpoint allows a maximum of 20 album ids per request,
    # so we (potentially) have to batch requests.
    for i in range(0, len(album_ids), 20):
        # process in chunks of 20 album ids
        chunk_ids = album_ids[i:i+20]
        resp = spotify.albums(chunk_ids)

        for album_info in resp["albums"]:
            album_id = album_info["id"]
            albums[album_id] = album_info

    return albums


def write_new_playlist_csv(spotify: spotipy.Spotify, playlist_id: str, stream: typing.TextIO) -> typing.Tuple[str, typing.List[str]]:
    """Converts a Spotify playlist with the given ID into a CSV file, formatted for WTJU's new playlist editor.
    Writes the output to a given file-like object, and returns the playlist name with a list of human-readable
    warnings in case individual tracks could not be converted.

    Args:
        spotify (spotipy.Spotify): Spotify API client instance to use for API requests.
        playlist_id (str): Spotify playlist ID of the playlist to convert.
        stream (typing.TextIO): File-like object to write the converted CSV to.

    Returns:
        typing.Tuple[str, typing.List[str]]: Playlist name and list of human-readable warnings
    """

    writer = csv.writer(stream)
    warnings = []
    # write the CSV header row
    writer.writerow(NEW_EDITOR_HEADERS)

    try:
        # make API call for playlist name
        playlist_name = spotify.playlist(playlist_id, fields=["name"])["name"]
    except spotipy.SpotifyException:
        # for some reason, this API call sometimes returns 404
        # so far, have been able to reproduce on spotify wrapped playlists;
        # odd.
        playlist_name = None

    # make API call for the playlist's items (i.e., its tracks)
    playlist_items = spotify.playlist_items(playlist_id)

    # get info for all albums in this playlist
    album_info = _get_bulk_album_info(spotify, playlist_items)

    # TODO: >100 tracks in a playlist? (spotipy uses limit=100 by default)
    # responses are paginated
    for item in playlist_items["items"]:
        # fetch relevant variables
        track = item["track"]

        # for whatever reason, even when setting additional_items=["track"], Spotify Web API
        # returns entries for podcast epsiodes. Unfortunately, the response contains no
        # useful data (like the podcast name), so we just have to give this blanket error message.
        if track is None:
            warnings.append(
                "I couldn't find details on an item in your playlist, so I ignored it. (This could be caused by a podcast episode in your playlist.)")
            # just skip it
            continue

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
            album_id = album["id"]  # get album id for this track
            # lookup in the premade dictionary (as opposed to making new api request)
            album_ext = album_info[album_id]

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
        duration_minutes, duration_seconds = util._duration_from_ms(
            duration_ms)

        # pad out seconds so (3, 2) -> "3:02"
        duration_str = f"{duration_minutes}:{str(duration_seconds).zfill(2)}"

        row = [
            track_name,  # track title
            duration_str,  # track duration
            artist_name,  # artist name
            album_name,  # album name
            release_year,  # release year
            label,  # record label
            "",  # composer
            ""  # notes
        ]

        # write the row
        writer.writerow(row)

    # return any warnings we encountered
    return playlist_name, warnings


def write_old_playlist_csv(spotify: spotipy.Spotify, playlist_id: str, show_title: str, show_date: date, stream: typing.TextIO) -> typing.Tuple[str, typing.List[str]]:
    """Converts a Spotify playlist with the given ID into a CSV file, formatted for WTJU's new playlist editor.
    Writes the output to a given file-like object, and returns the playlist name with a list of human-readable 
    warnings in case individual tracks could not be converted.

    Args:
        spotify (spotipy.Spotify): Spotify API client instance to use for API calls.
        playlist_id (str): Spotify Playlist ID for the playlist to convert.
        show_title (str): Title of the show in WTJU's interface.
        show_date (datetime.date.Date): Date of this show.
        stream (typing.TextIO): File-like object to write the converted CSV file.

    Returns:
        typing.Tuple[str, typing.List[str]]: Playlist name and list of human-readable warnings
    """
    writer = csv.writer(stream)
    warnings = []

    # write row for show title, show date
    # (part of spec for old playlist editor)
    writer.writerow([show_title, date.strftime(show_date, "%m/%d/%y")])

    # write the CSV header row
    writer.writerow(OLD_EDITOR_HEADERS)

    try:
        # make API call for playlist name
        playlist_name = spotify.playlist(playlist_id, fields=["name"])["name"]
    except spotipy.SpotifyException:
        # for some reason, this API call sometimes returns 404
        # so far, have been able to reproduce on spotify wrapped playlists;
        # odd.
        playlist_name = None

    # make API call for the playlist's items (i.e., its tracks)
    playlist_items = spotify.playlist_items(playlist_id)

    # get info for all albums in this playlist
    album_info = _get_bulk_album_info(spotify, playlist_items)

    # TODO: >100 tracks in a playlist? (spotipy uses limit=100 by default)
    # responses are paginated
    for item in playlist_items["items"]:
        # fetch relevant variables
        track = item["track"]

        # for whatever reason, even when setting additional_items=["track"], Spotify Web API
        # returns entries for podcast epsiodes. Unfortunately, the response contains no
        # useful data (like the podcast name), so we just have to give this blanket error message.
        if track is None:
            warnings.append(
                "I couldn't find details on an item in your playlist, so I ignored it. (This could be caused by a podcast episode in your playlist.)")
            # just skip it
            continue

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
            album_id = album["id"]  # get album id for this track
            # lookup in the premade dictionary (as opposed to making new api request)
            album_ext = album_info[album_id]

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
        duration_minutes, duration_seconds = util._duration_from_ms(
            duration_ms)

        # pad out seconds so (3, 2) -> "3:02"
        duration_str = f"{duration_minutes}:{str(duration_seconds).zfill(2)}"

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

        # write the row
        writer.writerow(row)

    # return any warnings we encountered
    return playlist_name, warnings
