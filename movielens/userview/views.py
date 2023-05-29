from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .models import Genre, Movie

from .forms import MovieForm, RegisterForm, LoginForm

#############################################
### Views
#############################################

def homeRequest(request : HttpRequest):
    context = {
        'tab': 'home',
    }

    template = loader.get_template('userview/home.html')
    return HttpResponse(template.render(context, request))


def moviesRequest(request : HttpRequest):
    movies = Movie.objects.order_by('title')
    paginator = Paginator(movies, 24)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'tab': 'movies',
        'movies' : page_obj,
    }

    template = loader.get_template('userview/movies.html')
    return HttpResponse(template.render(context, request))


def movieRequest(request : HttpRequest, id : int):
    movie = get_object_or_404(Movie, id=id)

    context = {
        'tab': 'movies',
        'movie' : movie,
    }

    template = loader.get_template('userview/movie.html')
    return HttpResponse(template.render(context, request))


def genresRequest(request : HttpRequest):
    genres = Genre.objects.order_by('name')

    context = {
        'tab': 'genres',
        'genres' : genres,
    }

    template = loader.get_template('userview/genres.html')
    return HttpResponse(template.render(context, request))


def genreRequest(request : HttpRequest, id : int):
    genre = get_object_or_404(Genre, id=id)
    movies = Movie.objects.filter(genres=genre).order_by('title')
    paginator = Paginator(movies, 24)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'tab': 'genres',
        'genre' : genre,
        'movies' : page_obj,
    }

    template = loader.get_template('userview/genre.html')
    return HttpResponse(template.render(context, request))


def profileRequest(request : HttpRequest):
    context = {
        'tab': 'profile',
    }

    template = loader.get_template('userview/profile.html')
    return HttpResponse(template.render(context, request))


#############################################
### Authentication views
#############################################
def registerRequest(request : HttpRequest):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        
    context = {
        'form': form,
    }
    template = loader.get_template('userview/register.html')
    return HttpResponse(template.render(context, request))


def loginRequest(request : HttpRequest):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
        
    context = {
        'form': form,
    }
    template = loader.get_template('userview/login.html')
    return HttpResponse(template.render(context, request))


def logoutRequest(request : HttpRequest):
    if request.method == 'POST':
        logout(request)

    return redirect('home')


#############################################
### Admin views
#############################################

def admin(request : HttpRequest):
    if (request.user.is_superuser == False):
        return HttpResponseForbidden()
    
    context = {
        'tab': 'admin',
    }
    template = loader.get_template('userview/admin.html')
    return HttpResponse(template.render(context, request))


def addMovieRequest(request : HttpRequest):
    if (request.user.is_superuser == False):
        return HttpResponseForbidden()
    
    form = MovieForm()

    if request.method == 'POST' and request.user.is_superuser:
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movie "' + form.cleaned_data['title'] + '" added successfully')
            form = MovieForm()
        else:
            messages.error(request, 'Movie could not be added') 
            
    context = {
        'tab': 'admin',
        'form': form,
    }
    template = loader.get_template('userview/add_movie.html')
    return HttpResponse(template.render(context, request))
