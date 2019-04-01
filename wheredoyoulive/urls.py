from django.urls import path

from . import views

app_name = "wheredoyoulive"  # idk if I need this
urlpatterns = [
    path('', views.index, name='index'),
]
