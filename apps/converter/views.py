from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.contrib import messages
from django.utils import text
from django.urls import reverse
import urllib.parse

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
                warnings = lib.write_playlist_csv(playlist_url, csvstream)

                # has the user already been warned? should we proceed with the download?
                not_yet_warned = "warned" not in request.GET or request.GET["warned"] != "1"
                if warnings and not_yet_warned:
                    # if there are warnings, and the user hasn't yet seen them, don't start the download.
                    # instead, render the warnings page, and provide a link that will actually start the download.
                    for warning in warnings:
                        messages.add_message(
                            request, messages.WARNING, warning)

                    download_view_root = reverse("generate_playlist")

                    # grab some GET parameters from the request
                    csrf = urllib.parse.quote(
                        request.GET["csrfmiddlewaretoken"])  # csrf token
                    playlist_url = urllib.parse.quote(
                        request.GET["playlist_url"])  # original playlist url

                    # note the appended "&warned=1"
                    continue_download_url = f"{download_view_root}?csrfmiddlewaretoken={csrf}&playlist_url={playlist_url}&warned=1"

                    return render(request, "warnings.html", {
                        "continue_download_url": continue_download_url
                    })
                csvstream.seek(0)

                playlist_name = lib.get_playlist_name(playlist_url)

                if not playlist_name:
                    # in case playlist_name = ""
                    playlist_name = "playlist"

                filename = text.slugify(playlist_name) + ".csv"

                # create response object
                resp = HttpResponse(csvstream, content_type="text/csv")
                # force download
                resp["Content-Disposition"] = f"attachment; filename={filename}"
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
