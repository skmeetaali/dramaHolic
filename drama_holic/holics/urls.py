from django.urls import path
from . import views


app_name = "holics"
urlpatterns = [
    path("", views.home, name="home"),
    path("showList/", views.showList, name="showList"),
    path("database/", views.db, name="db"),
    path("api/", views.fetch_pop_movies, name="api")

]
