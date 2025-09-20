import re
from typing import Iterator
import requests

from dataclasses import dataclass
from datetime import datetime, timedelta

SPOTIFY_PLAYLIST_URL_VALIDATOR = re.compile(r"(?:http|https)://open\.spotify\.com/playlist/([^?]+)(?:\?.+)?", re.IGNORECASE)

def extract_playlist_id_from_url(url: str) -> str:
    match = SPOTIFY_PLAYLIST_URL_VALIDATOR.findall(url)
    if match:
        return match[0]
    else:
        raise ValueError("Argument must be a valid Spotify playlist URL")

@dataclass
class Playlist:
    id: str
    name: str
    description: str

@dataclass
class Artist:
    id: str
    name: str

@dataclass
class Album:
    id: str
    name: str
    label: str
    release_year: str

@dataclass
class Track:
    id: str
    name: str
    album_id: str
    artists: list[Artist]
    duration_ms: int
    is_local: bool

class SpotifyError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

ACCOUNTS_API_BASE = 'https://accounts.spotify.com/api'
API_BASE = 'https://api.spotify.com/v1'

class Spotify:
    def __init__(self, client_id: str, client_secret: str):
        self._client_id = client_id
        self._client_secret = client_secret
        self._token = None
        self._token_expires = None
        
        # set up session
        self._session = requests.Session()
        self._session.auth = lambda r: self._set_authorization(r)

    def _token_valid(self, at: datetime | None = None) -> bool:
        if at is None:
            at = datetime.now()

        return self._token is not None and self._token_expires is not None and at < self._token_expires

    def _resp_body(self, resp: requests.Response) -> dict:
        if resp.ok:
            return resp.json()

        try:
            # try to read detailed error message
            error = resp.json()["error"]
        except:
            # fall back to response text
            error = resp.text

        raise SpotifyError(resp.status_code, error)

    def _fetch_token(self) -> str:
        if self._token_valid():
            return self._token

        # this is the only request that doesn't use the session.
        resp = requests.post(
            f"{ACCOUNTS_API_BASE}/token",
            data={
                'client_id': self._client_id,
                'client_secret': self._client_secret,
                'grant_type': 'client_credentials'
            }
        )
        body = self._resp_body(resp)

        self._token = body['access_token']
        self._token_expires = datetime.now() + timedelta(seconds=int(body['expires_in']))

        return self._token

    def _set_authorization(self, r: requests.PreparedRequest) -> requests.PreparedRequest:
        r.headers['Authorization'] = f'Bearer {self._fetch_token()}'
        return r

    def _get(self, path, *args, **kwargs) -> dict:
        resp = self._session.get(API_BASE + path, *args, **kwargs)
        return self._resp_body(resp)

    def get_playlist(self, playlist_id: str) -> Playlist:
        """
        Gets playlist details.
        """
        body = self._get(f'/playlists/{playlist_id}')

        return Playlist(
            body['id'],
            body['name'],
            body['description']
        )

    def _to_artist(self, artist: dict) -> Artist:
        return Artist(artist['id'], artist['name'])

    def _to_track(self, item: dict) -> Track:
        track = item['track']

        if track is None:
            return None

        return Track(
            track['id'],
            track['name'],
            track['album']['id'],
            [self._to_artist(artist) for artist in track['artists']],
            track['duration_ms'],
            track['is_local']
        )

    def get_playlist_tracks(self, playlist_id: str) -> Iterator[Track]:
        """
        Returns a generator that lazily loads all of a playlist's tracks.
        """
        offset = 0

        while True:
            body = self._get(f'/playlists/{playlist_id}/tracks', params={
                'fields': 'items(track(id,name,album(id),artists(name,id),duration_ms,is_local))',
                'limit': 50,
                'offset': offset
            })

            items = body['items']
            if not items:
                break

            offset += len(items)
            yield from filter(lambda t: t is not None, map(self._to_track, items))

    def _to_album(self, album: dict) -> Album:
        return Album(album['id'], album['name'], album['label'], album['release_date'][:4])

    def get_several_albums(self, album_ids: list[str]) -> dict[str, Album]:
        results = {}
        album_ids = list(set(album_ids)) # filter duplicates
        for start in range(0, len(album_ids), 20): # process in batches of 20 (max request size)
            batch = album_ids[start:start+20]
            body = self._get("/albums", params={
                'ids': ','.join(batch)
            })
            for album_dict in body['albums']:
                album = self._to_album(album_dict)
                results[album.id] = album
        return results