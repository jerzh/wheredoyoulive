from django import forms

# https://docs.djangoproject.com/en/2.1/topics/forms/
# https://docs.djangoproject.com/en/2.1/ref/forms/api/#django.forms.Form.cleaned_data


# form for creating new user
class CreateForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    name = forms.CharField(label='Name', max_length=100)
    latitude = forms.CharField(label='Homebase Latitude', max_length=100)
    longitude = forms.CharField(label='Homebase Longitude', max_length=100)


# form for logging in
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)


# form for updating user properties (we intentionally made it so that usernames
# can't be changed)
class UpdateForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    latitude = forms.CharField(label='Homebase Latitude', max_length=100)
    longitude = forms.CharField(label='Homebase Longitude', max_length=100)


# form for adding or updating POIs
class AddPOIForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    address = forms.CharField(label='Address', max_length=100)


# form for removing POIs
class RemovePOIForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
