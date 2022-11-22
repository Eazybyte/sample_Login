from django.urls import path
from . import views
urlpatterns = [
    path('home', views.home, name='adm_home'),
    path('', views.signin, name='adm_signin'),
    path('signout', views.signout, name='adm_signout'),


    path("add/",views.adduser,name="add"),
    path("delete/<int:id>",views.delete_user,name="delete"),
    path("edit/<int:id>",views.update,name="edit"),
    path("search/",views.search,name="search"),
]