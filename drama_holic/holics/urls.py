from django.urls import path
from . import views


app_name = "holics"
urlpatterns = [
    path("", views.home, name="homepage"),
    path("add", views.add, name="add"),
    path("showList/", views.showList, name="showList"),
    path("add_drama/", views.add_drama, name="add_drama"),
    path("add_anime/", views.add_anime, name="add_anime"),
    path("add_movie", views.add_movies, name="add_movie"),
    path("add_manga", views.add_manga, name="add_manga"),
    path("delete_drama/<uuid:id>", views.delete_drama, name="delete_drama"),
    path("delete_anime/<uuid:id>", views.delete_anime, name="delete_anime"),
    path("delete_manga/<uuid:id>", views.delete_manga, name="delete_manga"),
    path("delete_movie/<uuid:id>", views.delete_movie, name="delete_movie"),
    path("minus_ep_anime/<uuid:id>", views.minus_ep_anime, name="minus_ep_anime"),
    path("plus_ep_anime/<uuid:id>", views.plus_ep_anime, name="plus_ep_anime"),
]
