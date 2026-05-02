from django.urls import path
from . import views


app_name = "holics"
urlpatterns = [
    path("", views.home, name="home"),
    path("showList/", views.showList, name="showList")
]
