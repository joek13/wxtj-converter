from django import forms
from . import lib


class PlaylistForm(forms.Form):
    playlist_url = forms.URLField()
    format_old = forms.BooleanField(required=False)

    def is_valid(self) -> bool:
        # override is_valid so we can make sure playlist_url is a valid Spotify playlist URL
        if super().is_valid():
            url_clean = self.cleaned_data["playlist_url"]
            if lib.validate_spotify_playlist_url(url_clean):
                return True
            else:
                self.add_error(
                    "playlist_url", "Must be a valid Spotify playlist URL")
        else:
            return False
