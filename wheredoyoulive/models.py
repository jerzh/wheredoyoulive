from django.db import models

# https://docs.djangoproject.com/en/2.1/topics/db/models/
# https://stackoverflow.com/questions/2257635/django-unique-field-generation


class User(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    def __str__(self):
        return self.username
