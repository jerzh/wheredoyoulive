from django.urls import path

from . import views

app_name = "wheredoyoulive"  # idk if I need this
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>', views.user_index, name='user_index'),
    path('make_user', views.make, name='make'),
    path('<str:username>/upd_user', views.update, name='update'),
    path('<str:username>/del_user', views.delete, name='delete'),
    path('<str:username>/add_poi', views.add_poi, name='add_poi'),
    path('<str:username>/rm_poi', views.rm_poi, name='rm_poi'),
]
