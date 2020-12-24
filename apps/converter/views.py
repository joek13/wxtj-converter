from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.


def index(request: HttpRequest) -> HttpResponse:
    # render static template (sort of inefficient)
    return render(request, "index.html", {})
