from django.urls import path
from . import views

urlpatterns = [
    path("", views.homeRequest, name="home"),
    path("movies", views.moviesRequest, name="movies"),
    path("movie/<int:id>", views.movieRequest, name="movie"),
    path("genres", views.genresRequest, name="genres"),
    path("genre/<int:id>", views.genreRequest, name="genre"),
    path("profile", views.profileRequest, name="profile"),
    path("register", views.registerRequest, name="register"),
    path("login", views.loginRequest, name="login"),
    path("logout", views.logoutRequest, name="logout"),
    path("_admin", views.admin, name="admin"),
    path("_add_movie", views.addMovieRequest, name="addmovie"),
]