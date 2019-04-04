from django.db import models
from django import forms

# https://docs.djangoproject.com/en/2.1/topics/db/models/
# https://stackoverflow.com/questions/2257635/django-unique-field-generation
# https://docs.djangoproject.com/en/2.1/topics/forms/


class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    def __str__(self):
        return self.username


class Places(models.Model):
    user_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    coordinate_lat = models.IntegerField()
    coordinate_long = models.IntegerField()


class CreateForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)


class UpdateForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    latitude = forms.CharField(label='Homebase Latitude', max_length=100)
    longitude = forms.CharField(label='Homebase Longitude', max_length=100)
