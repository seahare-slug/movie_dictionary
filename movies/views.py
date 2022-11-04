from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from .models import Movie


# Create your views here.
@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == "GET":
        movies = Movie.objects.all()
        context = {
            "movies": movies,
        }
        return render(request, "movies/index.html", context)

@require_safe
def detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    genres = [genre.name for genre in movie.genres.all()]
    context = {
        "movie": movie,
        "genres": genres,
    }
    return render(request, "movies/detail.html", context)

@require_safe
def recommended(request):
    movies = Movie.objects.all()
    movies_list = []
    popularity_movies_list = []
    vote_average_movies_list = []
    for movie in movies:
        movies_list.append([movie.pk, movie.title, movie.popularity, movie.vote_average])
    popularity_movies_list = sorted(movies_list, key=lambda x: x[2], reverse=True)
    vote_average_movies_list = sorted(movies_list, key=lambda x: x[3], reverse=True)
    context = {
        "popularity_sorted_movies": popularity_movies_list[:10],
        "vote_average_sorted_movies": vote_average_movies_list[:10],
    }
    return render(request, "movies/recommended.html", context)