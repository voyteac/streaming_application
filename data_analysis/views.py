from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def analysis(request: HttpRequest) -> HttpResponse:
    context = {}

    return render(request, 'data_analysis_main.html', context)
