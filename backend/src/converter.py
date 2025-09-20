import base64
import io
import json
from datetime import date

import boto3

from spotify import extract_playlist_id_from_url, Spotify
from show import ShowPlaylist

import format

secrets_manager = boto3.client('secretsmanager')
spotify_api_key = json.loads(secrets_manager.get_secret_value(SecretId='SpotifyApiKey')['SecretString'])

def read_body(ev):
    body = base64.b64decode(ev["body"]) if ev["isBase64Encoded"] else ev["body"]
    return json.loads(body)


def ok(body):
    return {
        "statusCode": 200,
        "body": body,
        "isBase64Encoded": False
    }

def error(result, message, code=500):
    result["error"] = message

    return {
        "statusCode": code,
        "body": result,
        "isBase64Encoded": False
    }

def handle(ev, ctx):
    try:
        body = read_body(ev)
        playlist_url = body['playlist_url']
        playlist_id = extract_playlist_id_from_url(playlist_url)

        csv_format = body['format']
        if csv_format == 'old':
            is_old = True
        elif csv_format == 'new':
            is_old = False
        else:
            raise ValueError(f'invalid value for format: {csv_format}')

        show_title = None
        if body.get('show_title'):
            show_title = body['show_title']

        show_date = None
        if body.get('show_date'):
            show_date = date.fromisoformat(body["show_date"])

        client = Spotify(
            client_id = spotify_api_key['client_id'],
            client_secret = spotify_api_key['client_secret']
        )

        playlist = ShowPlaylist.from_spotify_playlist(client, playlist_id, show_title, show_date)
        buf = io.StringIO()

        if is_old:
            warnings = format.write_old_playlist_csv(playlist, buf)
        else:
            warnings = format.write_new_playlist_csv(playlist, buf)

        return ok({
            'playlistName': playlist.playlist_name,
            'warnings': warnings,
            'body': buf.getvalue()
        })

    except Exception as e:
        return error({}, repr(e))