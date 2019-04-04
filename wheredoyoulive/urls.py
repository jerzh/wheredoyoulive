from django.urls import path

from . import views

app_name = "wheredoyoulive"  # idk if I need this
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>', views.user_index, name='user_index'),
    path('make_user', views.make, name='make'),
    # path('make_user/<str:dname>/<str:uname>/<str:lat>/<str:long>', views.make_info),
    path('upd_user', views.update, name='update'),
    # path('upd_user/<str:dname>/<str:uname>/<str:lat>/<str:long>', views.update_info),
    path('del_user/<str:username>', views.delete, name='delete'),
]
