from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.contrib import messages
from . import forms

# Create your views here.


def index(request: HttpRequest) -> HttpResponse:
    # render static template (sort of inefficient)
    return render(request, "index.html", {})


def generate_playlist(request: HttpResponse) -> HttpResponse:
    if request.method == "GET":
        form = forms.PlaylistForm(request.GET)

        if form.is_valid():
            # Great!
            pass
        else:
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
