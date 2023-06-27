from django.urls import path

from . import views
from .views import addvolunteer,index,update_view

app_name = "volunteers"
urlpatterns = [
    path("add",addvolunteer,name="add"),
    path("index/",index,name="index"),
    path("update/<str:pk>/",update_view,name="update_view"),
    path("remove/<str:pk>/",views.remove_volunteer,name="remove"),
]