# Still need to replace ADDKEY with key in AddPOI. I also have some questions in AddPOI

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Places
from .forms import CreateForm, LoginForm, UpdateForm, AddPOIForm, RemovePOIForm
import urllib.request, json
import urllib, json

# https://stackoverflow.com/questions/150505/capturing-url-parameters-in-request-get
# https://docs.djangoproject.com/en/2.1/topics/templates/
# https://stackoverflow.com/questions/53083880/django-2-reverse-for-index-not-found-index-is-not-a-valid-view-function-o
# https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression
# https://docs.djangoproject.com/en/dev/topics/db/queries/#backwards-related-objects
# https://developers.google.com/maps/documentation/geocoding/intro#geocoding
# https://www.powercms.in/blog/how-get-json-data-remote-url-python-script


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as require
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('wheredoyoulive:user_index', \
                args=(form.cleaned_data['username'],)))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
    return render(request, 'wheredoyoulive/homepage.html', \
        {'form': form, \
        'make': reverse('wheredoyoulive:make'), \
        'index': reverse('wheredoyoulive:index')})


def make(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if (User.objects.filter(username=username)):
                return render(request, 'wheredoyoulive/ErrorPage.html', \
                    {'error_name': 'Username already taken', \
                    'index': reverse('wheredoyoulive:index')})
            else:
                u = User(username=username, latitude=0, longitude=0)
                u.save()
                return HttpResponseRedirect(reverse('wheredoyoulive:user_index', \
                    args=(username,)))
    else:
        form = CreateForm()
        return render(request, 'wheredoyoulive/FormPage.html', \
            {'form': form, \
            'page': reverse('wheredoyoulive:make')})


def user_index(request, username):
    if (User.objects.filter(username=username)):
        u = User.objects.get(username=username)
        return render(request, 'wheredoyoulive/userpage.html', \
            {'username': username, \
            'name': u.name, \
            'latitude': u.latitude, \
            'longitude': u.longitude, \
            'update': reverse('wheredoyoulive:update', args=(username,)), \
            'delete': reverse('wheredoyoulive:delete', args=(username,)), \
            'add_poi': reverse('wheredoyoulive:add_poi', args=(username,)), \
            'remove_poi': reverse('wheredoyoulive:rm_poi', args=(username,))})
    else:
        return render(request, 'wheredoyoulive/ErrorPage.html', \
            {'error_name': 'User does not exist', \
            'index': reverse('wheredoyoulive:index')})


def update(request, username):
    if (User.objects.filter(username=username)):
        u = User.objects.get(username=username)
        if request.method == 'POST':
            form = UpdateForm(request.POST)
            if form.is_valid():
                u.name = form.cleaned_data['name']
                u.latitude = form.cleaned_data['latitude']
                u.longitude = form.cleaned_data['longitude']
                u.save()
                return HttpResponseRedirect(reverse('wheredoyoulive:user_index', \
                    args=(username,)))
        else:
            form = UpdateForm()
            return render(request, 'wheredoyoulive/FormPage.html', \
                {'form': form, \
                'page': reverse('wheredoyoulive:update', args=(username,))})
    else:
        return render(request, 'wheredoyoulive/ErrorPage.html', \
            {'error_name': 'User does not exist', \
            'index': reverse('wheredoyoulive:index')})



def delete(request, username):
    u = User.objects.get(username=username)
    u.delete()
    return HttpResponseRedirect(reverse('wheredoyoulive:index'))


def add_poi(request, username):
    u = User.objects.get(username=username)
    if request.method == 'POST':
        form = AddPOIForm(request.POST)
        if form.is_valid():
            #Checks to see if place with same name for same user already exists, error if it does
            if (Places.objects.filter(user_id=u.id, title=form['title'])): #Do I need form.cleaned_data['title']
                return render(request, 'wheredoyoulive/ErrorPage.html', \
                    {'error_name': 'Title already taken for this user', \
                    'index': reverse('wheredoyoulive:index')}) #Should I change where error redirects?
            address = form['address'].replace(' ', '+') #Changes address into form url query can understand
            #Next part gets Json info from google API
            url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=ADDKEY' % address #Replace ADDKEY with key
            data = json.loads(urllib.request.urlopen(url).read())
            coords = data["results"][0]["geometry"]["location"] #Uses format of json response to get info
            #Makes and saves a new place object
            p = Place(user_id=u.id, title=form.cleaned_data['title'], coordinate_lat=coords["lat"], coordinate_long=coords["lng"])
            p.save()
            #Do we want to have a page that tells you you added a POI successfully? Do we have that? For now just takes back to user home
            return HttpResponseRedirect(reverse('wheredoyoulive:user_index', \
                args=(form.cleaned_data['username'],)))
    else:
        form = AddPOIForm()
    return render(request, 'wheredoyoulive/FormPage.html', \
        {'form': form, \
         'page': reverse('wheredoyoulive:add_poi')})


def rm_poi(request, username):
    if request.method == 'POST':
        form = RemovePOIForm(request.POST)
        if form.is_valid():
            u = User(username=username)
            p = Places.objects.get(user_id=u.id, title=form['title'])
            p.delete()
            return HttpResponseRedirect(reverse('wheredoyoulive:user_index', \
                args=(form.cleaned_data['username'],)))
    else:
        form = RemovePOIForm()
    return render(request, 'wheredoyoulive/FormPage.html', \
        {'form': form, \
        'index': reverse('wheredoyoulive:rm_poi')})
