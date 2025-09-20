from dataclasses import dataclass
from spotify import SpotifyError, Track, Artist, Album, Spotify
from datetime import date

@dataclass
class ShowTrack:
    track: Track
    album: Album

@dataclass
class ShowPlaylist:
    playlist_name: str | None
    show_title: str | None
    show_date: date | None
    tracks: list[ShowTrack]

    @classmethod
    def from_spotify_playlist(cls, client: Spotify, playlist_id: str, show_title: str | None = None, show_date: date | None = None) -> 'ShowPlaylist':
        playlist_name = None

        try:
            playlist = client.get_playlist(playlist_id)
            playlist_name = playlist.name
        except SpotifyError as e:
            if e.status_code != 404:
                raise e

        try:
            tracks = list(client.get_playlist_tracks(playlist_id))
        except SpotifyError as e:
            if e.status_code == 404:
                raise RuntimeError("The playlist wasn't found. Is it marked as private?")
            else:
                raise e

        albums = client.get_several_albums([tr.album_id for tr in tracks])

        show_tracks = [ ShowTrack(tr, albums[tr.album_id]) for tr in tracks ]
        show_playlist = ShowPlaylist(
            playlist_name,
            show_title,
            show_date,
            show_tracks
        )
        return show_playlist