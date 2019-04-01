from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('Good job you did it')
