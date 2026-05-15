from django.urls import path
from . import views


app_name = "holics"
urlpatterns = [
    path("", views.home, name="home"),
    path("add", views.add, name="add"),
    path("showList/", views.showList, name="showList"),
    path("api/", views.fetch_pop_movies, name="api"),
    path("add_anime", views.add_anime, name="add_anime"),
    path("add_manga", views.add_manga, name="add_manga")
]
