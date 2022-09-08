import unidecode
from django.shortcuts import render
from django.views import View

from database.models import Movie, Actor


class SearchMoviesView(View):
    def get(self, request):
        return render(request, 'search.html')

    def post(self, request):
        found_movies = []
        found_actors = []
        if search_string := unidecode.unidecode(request.POST.get('searched_value')):
            found_movies = Movie.objects.filter(name_unified__icontains=search_string)
            found_actors = Actor.objects.filter(name_unified__icontains=search_string)
        return render(request, 'search.html', {'movie_list': found_movies, 'actors_list': found_actors})


class MovieDetailView(View):
    def get(self, request, movie_id):
        movie = Movie.objects.get(pk=movie_id)
        return render(request, 'movie_detail.html', {'movie': movie})


class ActorDetailView(View):
    def get(self, request, actor_id):
        actor = Actor.objects.get(pk=actor_id)
        return render(request, 'actor_detail.html', {'actor': actor})
