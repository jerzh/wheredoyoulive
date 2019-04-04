from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('Homepage')

# Make new user
def make(request, username):
    u = User(username=username, latitude=0, longitude=0)
    u.save()
    return HttpResponse('Made %s' % username)

def update(request, username):
    return HttpResponse('Updated %s' % username)

def delete(request, username):
    u = User.objects.get(username=username)
    u.delete()
    return HttpResponse('Deleted %s' % username)
