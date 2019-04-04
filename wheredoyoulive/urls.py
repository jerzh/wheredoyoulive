from django.urls import path

from . import views

app_name = "wheredoyoulive"  # idk if I need this
urlpatterns = [
    path('', views.index),
    path('make_user/<str:username>', views.make),
    path('upd_user/<str:username>', views.update),
    path('del_user/<str:username>', views.delete),
]
