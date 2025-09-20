import csv
import typing
from datetime import date

from show import ShowPlaylist

def _ms_to_duration_string(milliseconds):
    # Convert milliseconds to total seconds
    total_seconds = milliseconds // 1000
    
    # Calculate minutes and remaining seconds
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    
    # Format as m:ss with zero-padded seconds
    return f"{minutes}:{seconds:02d}"

NEW_EDITOR_HEADERS = [
    "title",  # track title
    "duration",  # track duration mm:ss
    "performer",  # track artist
    "album",  # album title
    "year",  # release year
    "label",  # record label
    "composer",  # track composer
    "notes"  # generic notes
]

def write_new_playlist_csv(playlist: ShowPlaylist, stream: typing.TextIO) -> list[str]:
    writer = csv.writer(stream)
    warnings = []

    writer.writerow(NEW_EDITOR_HEADERS)
    for track in playlist.tracks:
        writer.writerow([
            track.track.name, # track title
            _ms_to_duration_string(track.track.duration_ms), # track duration
            ', '.join(ar.name for ar in track.track.artists), # track artist
            track.album.name, # album name
            track.album.release_year, # release year
            track.album.label, # record label
            '',
            ''
        ])

    return warnings

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

def write_old_playlist_csv(playlist: ShowPlaylist, stream: typing.TextIO) -> list[str]:
    writer = csv.writer(stream)
    warnings = []

    if playlist.show_title is None or playlist.show_date is None:
        raise ValueError('show_title and show_date are required for old playlist editor')

    writer.writerow([playlist.show_title, date.strftime(playlist.show_date, "%m/%d/%y")])
    writer.writerow(OLD_EDITOR_HEADERS)
    for track in playlist.tracks:
        writer.writerow([
            track.track.name, # track title
            '', # track URL
            _ms_to_duration_string(track.track.duration_ms),
            ', '.join(ar.name for ar in track.track.artists), # track artist
            '', # artist url
            track.album.name, # album name
            '', # album url
            track.album.release_year, # release year
            track.album.label, # record label
            '', # composer
            '', # composer url
            '' # notes
        ])

    return warnings