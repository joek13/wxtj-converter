from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.contrib import messages

import spotipy

from . import forms, lib
import io

# Create your views here.


def index(request: HttpRequest) -> HttpResponse:
    # render static template (sort of inefficient)
    return render(request, "index.html", {})


def generate_playlist(request: HttpResponse) -> HttpResponse:
    if request.method == "GET":
        # instantiate form based on get parameters
        form = forms.PlaylistForm(request.GET)

        if form.is_valid():
            # Great! form is valid
            playlist_url = form.cleaned_data["playlist_url"]
            # Generate the playlist csv
            try:
                csvstream = io.StringIO()
                lib.write_playlist_csv(playlist_url, csvstream)
                csvstream.seek(0)

                # create response object
                resp = HttpResponse(csvstream, content_type="text/csv")
                # force download
                resp["Content-Disposition"] = "attachment; filename=playlist.csv"
                return resp
            except ValueError as e:
                messages.add_message(request, messages.ERROR, e.message)
                return render(request, "index.html", {})
            except spotipy.SpotifyException as e:
                # clean up the message
                msg = e.msg  # messages take form of "http://<api url>: reason"
                # split by colons, remove url beforehand
                msg = msg.split(":")[2:]
                msg = ":".join(msg)  # join back with colons
                messages.add_message(
                    request, messages.ERROR, "Spotify returned an error: "+msg)
                return render(request, "index.html", {})
        else:
            # form is invalid: display errors
            for field_name, errors in form.errors.items():
                for error in errors:
                    if field_name != None:
                        messages.add_message(
                            request, messages.ERROR, f"Error in field {field_name}: {error}")
                    else:
                        messages.add_message(request, messages.ERROR, error)
            return render(request, "index.html", {})
    else:
        return HttpResponseNotAllowed(["GET"])
