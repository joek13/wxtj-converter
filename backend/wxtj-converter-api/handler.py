import json

from spotipy.exceptions import SpotifyException
import convertlib
import spotipy
import io
import json
import os
from datetime import date


SPOTIFY_API_CLIENT_ID = os.environ["SPOTIFY_API_CLIENT_ID"]
SPOTIFY_API_CLIENT_SECRET = os.environ["SPOTIFY_API_CLIENT_SECRET"]

# use memory cache handler
# we only need to store one token, and Lambda instances don't have filesystem access
cache_handler = spotipy.cache_handler.MemoryCacheHandler()

# initialize login credentials
spotify_creds = spotipy.SpotifyClientCredentials(
    client_id=SPOTIFY_API_CLIENT_ID, client_secret=SPOTIFY_API_CLIENT_SECRET, cache_handler=cache_handler)
spotify = spotipy.Spotify(client_credentials_manager=spotify_creds)


def _make_response(response: dict) -> dict:
    """Takes a response object and adds CORS headers.
    """
    # base response
    base_response = {
        "headers": {
            # allow requests from all origins
            "Access-Control-Allow-Origin": "*"
        }
    }

    # merge dictionaries, with the argument taking precedence
    return {**base_response, **response}


def convert_new_playlist(event, context):
    body = json.loads(event.get("body", "{}"))
    playlist_url = body["playlist_url"]

    try:
        playlist_id = convertlib.extract_playlist_id_from_url(playlist_url)
    except ValueError as e:
        response = {
            "statusCode": 400,
            "body": json.dumps({
                "error": str(e)
            })
        }

        return _make_response(response)

    try:
        buffer = io.StringIO()
        warnings = convertlib.write_new_playlist_csv(
            spotify, playlist_id, buffer)

    except SpotifyException as e:
        response = {
            "statusCode": 400,
            "body": json.dumps({
                "error": str(e)
            })
        }

        return _make_response(response)

    buffer.seek(0)

    response = {
        "statusCode": 200,
        "body": json.dumps({
            "warnings": warnings,
            "body": buffer.read()
        })
    }

    return _make_response(response)


def convert_old_playlist(event, context):
    body = json.loads(event.get("body", "{}"))
    playlist_url = body["playlist_url"]
    show_title = body["show_title"]
    show_date = date.fromisoformat(body["show_date"])

    try:
        playlist_id = convertlib.extract_playlist_id_from_url(playlist_url)
    except ValueError as e:
        response = {
            "statusCode": 400,
            "body": json.dumps({
                "error": str(e)
            })
        }

        return _make_response(response)

    try:
        buffer = io.StringIO()
        warnings = convertlib.write_old_playlist_csv(
            spotify, playlist_id, show_title, show_date, buffer)

    except SpotifyException as e:
        response = {
            "statusCode": 400,
            "body": {
                "error": str(e)
            }
        }

        return _make_response(response)

    buffer.seek(0)

    response = {
        "statusCode": 200,
        "body": json.dumps({
            "warnings": warnings,
            "body": buffer.read()
        })
    }

    return _make_response(response)
