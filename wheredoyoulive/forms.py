from django import forms

# https://docs.djangoproject.com/en/2.1/topics/forms/
# https://docs.djangoproject.com/en/2.1/ref/forms/api/#django.forms.Form.cleaned_data


class CreateForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)


class UpdateForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    latitude = forms.CharField(label='Homebase Latitude', max_length=100)
    longitude = forms.CharField(label='Homebase Longitude', max_length=100)
