from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def index(request):
    return HttpResponse('Homepage')


def make(request):
    # get info from form
    return HttpResponseRedirect()

def make_info(request, dname, uname, lat, long):
    u = User(name=dname, username=uname, latitude=lat, longitude=long)
    u.save()
    # return HttpResponse('Made %s' % username)
    return HttpResponseRedirect('')

def update(request):
    # return HttpResponse('Updated %s' % username)

def update_info(request, dname, uname, lat, long):
    u = User.objects.get(username=uname)
    u.update(name=dname, latitude=lat, longitude=long)

def delete(request, username):
    u = User.objects.get(username=username)
    u.delete()
    # return HttpResponse('Deleted %s' % username)
    return HttpResponseRedirect('')
