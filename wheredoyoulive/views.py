from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('Homepage')

# Make new user
def make(request, id):
    return HttpResponse('Made %s' % id)

def update(request, id):
    return HttpResponse('Updated %s' % id)

def delete(request, id):
    return HttpResponse('Im afraid you cant do that %s' % id)
