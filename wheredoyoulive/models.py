from django.db import models

# https://docs.djangoproject.com/en/2.1/topics/db/models/
# https://stackoverflow.com/questions/2257635/django-unique-field-generation


class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    def __str__(self):
        return self.values()


class Places(models.Model):
    user_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    coordinate_lat = models.CharField(max_length=100)
    coordinate_long = models.CharField(max_length=100)
    def __str__(self):
        return self.values()
