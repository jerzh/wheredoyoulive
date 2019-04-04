from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Places
from .forms import CreateForm, LoginForm, UpdateForm

# https://stackoverflow.com/questions/150505/capturing-url-parameters-in-request-get
# https://docs.djangoproject.com/en/2.1/topics/templates/
# https://stackoverflow.com/questions/53083880/django-2-reverse-for-index-not-found-index-is-not-a-valid-view-function-o
# https://docs.djangoproject.com/en/dev/topics/db/queries/#backwards-related-objects

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
    return render(request, 'wheredoyoulive/homepage.html', {'form': form, \
        'make': reverse('wheredoyoulive:make'), 'user_index': \
        reverse('wheredoyoulive:index')})


def user_index(request, username):
    return HttpResponse('User homepage: %s' % username)


def make(request):
    return HttpResponse('make')


# def make_info(request, dname, uname, lat, long):
#     u = User(name=dname, username=uname, latitude=lat, longitude=long)
#     u.save()
#     # return HttpResponse('Made %s' % username)
#     return HttpResponseRedirect('')


def update(request):
    return HttpResponse('update')


# def update_info(request, dname, uname, lat, long):
#     u = User.objects.get(username=uname)
#     u.update(name=dname, latitude=lat, longitude=long)


def delete(request, username):
    u = User.objects.get(username=username)
    u.delete()
    return HttpResponseRedirect(reverse('wheredoyoulive:index'))
