from django.urls import path

from . import views


app_name = "hospital"
urlpatterns = [
    path("add/",views.addhospital,name="add"),
    path("index/",views.index,name="index"),
    path("update/<str:pk>/",views.update_view,name="update_view"),
    #path('update/<int:pk>/',views.update_view, name='update_view')
]
