# Still need to replace ADDKEY with key in AddPOI. I also have some questions in AddPOI
#Also should we add ability to set home right when a user is made instead of making them update it

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Places
from .forms import CreateForm, LoginForm, UpdateForm, AddPOIForm, RemovePOIForm
import urllib.request
import urllib, json

'''Sources used:
https://stackoverflow.com/questions/150505/capturing-url-parameters-in-request-get
https://docs.djangoproject.com/en/2.1/topics/templates/
https://stackoverflow.com/questions/53083880/django-2-reverse-for-index-not-found-index-is-not-a-valid-view-function-o
https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression
https://docs.djangoproject.com/en/dev/topics/db/queries/#backwards-related-objects
https://developers.google.com/maps/documentation/geocoding/intro#geocoding
https://www.powercms.in/blog/how-get-json-data-remote-url-python-script
https://simpleisbetterthancomplex.com/tutorial/2016/07/27/how-to-return-json-encoded-response.html
https://stackoverflow.com/questions/20168582/programmingerror-column-genre-id-of-relation-music-album-does-not-exist-w
https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''

# this is the basic structure for rendering and processing forms: most other
# pages are a variation on this (to avoid repetitiveness, comments explaining
# form code will be omitted for other pages)
def index(request):
    # if this is a POST request, process form data
    if request.method == 'POST':
        # stick the data into a form object
        form = LoginForm(request.POST)
        # check whether it's valid
        if form.is_valid():
            # the data is in form.cleaned_data
            # redirect to user homepage (will check there whether user exists)
            # args=(form.cleaned_data['username'],) is to tell the user_index
            # page which user it is
            return HttpResponseRedirect(reverse('wheredoyoulive:user_index', \
                args=(form.cleaned_data['username'],)))
    # if a GET (or any other method) create a blank form
    else:
        form = LoginForm()
    # render the page (the third parameter is a dict of variable definitions;
    # for example form replaces the {{ form }} variable in homepage.html)
    # reverse takes the name of a page and outputs its URL; avoids hard-coding
    # URLs
    return render(request, 'wheredoyoulive/homepage.html', \
        {'form': form, \
        'make': reverse('wheredoyoulive:make'), \
        'index': reverse('wheredoyoulive:index')})

#Shows all users
def show_users(request):
    # list with the properties of every user
    uList = list(User.objects.all().values())
    return render(request, 'wheredoyoulive/listpage.html', \
        {'obj_list': uList, \
        'index': reverse('wheredoyoulive:index')})

#Makes new user
def make(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            #Makes sure username not already taken
            if (User.objects.filter(username=username)):
                # if it is, redirect to error page
                return render(request, 'wheredoyoulive/ErrorPage.html', \
                    {'error_name': 'Username already taken', \
                    'index': reverse('wheredoyoulive:index')})
            else:
                # create new user
                u = User(username=username, name=form.cleaned_data['name'], \
                    latitude=form.cleaned_data['latitude'], \
                    longitude=form.cleaned_data['longitude'])
                # gotta save manually
                u.save()
                return HttpResponseRedirect(reverse('wheredoyoulive:user_index', \
                    args=(username,)))
    else:
        form = CreateForm()
        return render(request, 'wheredoyoulive/FormPage.html', \
            {'form': form, \
            'page': reverse('wheredoyoulive:make')})

#Homepage for a user, has links to many useful features
def user_index(request, username):
    # check if user exists
    if (User.objects.filter(username=username)):
        # get user object
        u = User.objects.get(username=username)
        return render(request, 'wheredoyoulive/userpage.html', \
            {'username': username, \
            'name': u.name, \
            'latitude': u.latitude, \
            'longitude': u.longitude, \
            'update': reverse('wheredoyoulive:update', args=(username,)), \
            'delete': reverse('wheredoyoulive:delete', args=(username,)), \
            'add_poi': reverse('wheredoyoulive:add_poi', args=(username,)), \
            'remove_poi': reverse('wheredoyoulive:rm_poi', args=(username,)), \
            'view_poi': reverse('wheredoyoulive:poi', args=(username,)), \
            'update_poi': reverse('wheredoyoulive:upd_poi', args=(username,))})
    else:
        # redirect to error page
        return render(request, 'wheredoyoulive/ErrorPage.html', \
            {'error_name': 'User does not exist', \
            'index': reverse('wheredoyoulive:index')})

#Updates user info
def update(request, username):
    # check if user exists
    if (User.objects.filter(username=username)):
        # get user object
        u = User.objects.get(username=username)
        if request.method == 'POST':
            form = UpdateForm(request.POST)
            if form.is_valid():
                # set properties of user (overwrites previous)
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
        # redirect to error page
        return render(request, 'wheredoyoulive/ErrorPage.html', \
            {'error_name': 'User does not exist', \
            'index': reverse('wheredoyoulive:index')})

#Deletes user
# pretty straightforward: get user object and delete
def delete(request, username):
    u = User.objects.get(username=username)
    u.delete()
    return HttpResponseRedirect(reverse('wheredoyoulive:index'))

#Shows all POIs (POI stands for Point of Interest)
def show_pois(request):
    # list with the properties of every POI
    pList = list(Places.objects.all().values())
    return render(request, 'wheredoyoulive/listpage.html', \
        {'obj_list': pList, \
        'index': reverse('wheredoyoulive:index')})

#Gets all POIs for a user
def poi(request, username):
    # list with the properties of every POI belonging to username
    pList = list(Places.objects.filter(user_id=User.objects.get(username=username).id).values())
    return render(request, 'wheredoyoulive/listpage.html', \
        {'obj_list': pList, \
        'index': reverse('wheredoyoulive:user_index', args=(username,))})

#Adds POI
def add_poi(request, username):
    # get user object (we already know it exists because this page is only
    # reachable from user_index; I guess you could manually type in the URL but why)
    u = User.objects.get(username=username)
    if request.method == 'POST':
        form = AddPOIForm(request.POST)
        if form.is_valid():
            #Checks to see if place with same name for same user already exists, error if it does
            if (Places.objects.filter(user_id=u.id, title=form.cleaned_data['title'])):
                return render(request, 'wheredoyoulive/ErrorPage.html', \
                    {'error_name': 'Title already taken for this user', \
                    'index': reverse('wheredoyoulive:user_index', \
                        args=(username,))})
            address = form.cleaned_data['address'].replace(' ', '+') #Changes address into form url query can understand
            #Next part gets Json info from google API
            url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyCzUxXT3ppgnFHypo_jNUnihhJPY5pqXeg' % address #Replace ADDKEY with key
            data = json.loads(urllib.request.urlopen(url).read())
            coords = data["results"][0]["geometry"]["location"] #Uses format of json response to get info
            #Makes and saves a new place object
            p = Places(user_id=u.id, title=form.cleaned_data['title'], address=form.cleaned_data['address'], coordinate_lat=coords["lat"], coordinate_long=coords["lng"])
            p.save()
            #Takes back to user home
            return HttpResponseRedirect(reverse('wheredoyoulive:user_index', \
                args=(username,)))
    else:
        form = AddPOIForm()
    return render(request, 'wheredoyoulive/FormPage.html', \
        {'form': form, \
         'page': reverse('wheredoyoulive:add_poi', args=(username,))})

#Removes POI
def rm_poi(request, username):
    if request.method == 'POST':
        form = RemovePOIForm(request.POST)
        if form.is_valid():
            # get user object
            u = User.objects.get(username=username)
            #Checks to see if place with same name for same user already exists, error if it does
            if not (Places.objects.filter(user_id=u.id, title=form.cleaned_data['title'])):
                return render(request, 'wheredoyoulive/ErrorPage.html', \
                              {'error_name': 'No such POI exists', \
                               'index': reverse('wheredoyoulive:user_index', args=(username,))})
            # get POI object and delete
            p = Places.objects.get(user_id=u.id, title=form.cleaned_data['title'])
            p.delete()
            return HttpResponseRedirect(reverse('wheredoyoulive:user_index', \
                args=(username,)))
    else:
        form = RemovePOIForm()
    return render(request, 'wheredoyoulive/FormPage.html', \
        {'form': form, \
        'index': reverse('wheredoyoulive:rm_poi', args=(username,))})

#Updates POI (basically deletes old one and makes a new one, same as updating fields, so a lot is copied from add_poi)
def upd_poi(request, username):
    # get user object
    u = User.objects.get(username=username)
    if request.method == 'POST':
        form = AddPOIForm(request.POST)
        if form.is_valid():
            #Checks to make sure POI actually exists
            if not (Places.objects.filter(user_id=u.id, title=form.cleaned_data['title'])):
                return render(request, 'wheredoyoulive/ErrorPage.html', \
                              {'error_name': 'No such POI exists', \
                               'index': reverse('wheredoyoulive:user_index', args=(username,))})
            # get old POI object and delete
            p1 = Places.objects.get(user_id=u.id, title=form.cleaned_data['title'])
            p1.delete()
            #Everything after here is straight from add_poi
            address = form.cleaned_data['address'].replace(' ', '+')  # Changes address into form url query can understand
            # Next part gets Json info from google API
            url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyCzUxXT3ppgnFHypo_jNUnihhJPY5pqXeg' % address  # Replace ADDKEY with key
            data = json.loads(urllib.request.urlopen(url).read())
            coords = data["results"][0]["geometry"]["location"]  # Uses format of json response to get info
            # Makes and saves a new place object
            p = Places(user_id=u.id, title=form.cleaned_data['title'], address=form.cleaned_data['address'],
                      coordinate_lat=coords["lat"], coordinate_long=coords["lng"])
            p.save()
            #Takes back to user home
            return HttpResponseRedirect(reverse('wheredoyoulive:user_index', \
                                                args=(username,)))
    else:
        form = AddPOIForm()
    return render(request, 'wheredoyoulive/FormPage.html', \
                  {'form': form, \
                   'page': reverse('wheredoyoulive:upd_poi', args=(username,))})
