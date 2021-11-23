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

spotify_creds = spotipy.SpotifyClientCredentials(
    client_id=SPOTIFY_API_CLIENT_ID, client_secret=SPOTIFY_API_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=spotify_creds)


def convert_new_playlist(event, context):
    playlist_url = event["playlist_url"]

    try:
        playlist_id = convertlib.extract_playlist_id_from_url(playlist_url)
    except ValueError as e:
        response = {
            "statusCode": 400,
            "body": {
                "error": str(e)
            }
        }

        return response

    try:
        buffer = io.StringIO()
        warnings = convertlib.write_new_playlist_csv(
            spotify, playlist_id, buffer)

    except SpotifyException as e:
        response = {
            "statusCode": 400,
            "body": {
                "error": str(e)
            }
        }

        return response

    buffer.seek(0)

    response = {
        "statusCode": 200,
        "body": {
            "warnings": warnings,
            "body": buffer.read()
        }
    }

    return response


def convert_old_playlist(event, context):
    playlist_url = event["playlist_url"]
    show_title = event["show_title"]
    show_date = date.fromisoformat(event["show_date"])

    try:
        playlist_id = convertlib.extract_playlist_id_from_url(playlist_url)
    except ValueError as e:
        response = {
            "statusCode": 400,
            "body": {
                "error": str(e)
            }
        }

        return response

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

        return response

    buffer.seek(0)

    response = {
        "statusCode": 200,
        "body": {
            "warnings": warnings,
            "body": buffer.read()
        }
    }

    return response


def hello(event, context):
    body = {
        "message": "Go Serverless v2.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
