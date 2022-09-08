import requests
import unidecode
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
import logging
import re

from database.models import Movie, Actor

_logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Gets data of 300 best movies from CSFD"

    def handle(self, *args, **options):
        self._get_300_movies()
        # _get_actors_from_movie('/film/2294-vykoupeni-z-veznice-shawshank/')
        self.stdout.write(self.style.SUCCESS('Success'))

    def _get_300_movies(self):
        counter = 0
        from_filter = 0
        while counter < 300:
            url = f'https://www.csfd.cz/zebricky/filmy/nejlepsi/?from={from_filter}'
            if 300 - counter < 100:
                counter += self._get_movies_from_url(url, 300 - counter)
            else:
                counter += self._get_movies_from_url(url)
            from_filter += 100

    def _get_movies_from_url(self, url: str, num_of_movies: int = 1000) -> int:
        movie_processed_counter = 0
        r = requests.get(url, headers={'User-agent': 'my_bot v1.0'})
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")
            movies = soup.findAll('article')
            for movie in movies[:num_of_movies]:
                the_movie = movie.find('a', {'class': 'film-title-name'})
                movie_name = the_movie.text.strip()
                movie_url = f"https://www.csfd.cz{the_movie['href']}"
                try:
                    the_movie = Movie.objects.create(name=movie_name, url=movie_url,
                                                     name_unified=unidecode.unidecode(movie_name))
                    movie_processed_counter += 1
                    self._get_actors_from_movie(the_movie)
                    self.stdout.write(self.style.SUCCESS(f'Movie {the_movie.name} has been processed'))


                except IntegrityError:
                    self.stdout.write(self.style.SUCCESS(f'Movie {movie_name} already exists in DB'))

                    movie_processed_counter += 1

        else:
            raise CommandError(f'Cannot get data from {url} - status code: {r.status_code}')

        return movie_processed_counter

    def _get_actors_from_movie(self, movie: Movie):
        r = requests.get(movie.url, headers={'User-agent': 'my_bot v1.0'})
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")
            all_actors_tag = soup.find('h4', text=re.compile('Hrají:')).parent.findAll('a')
            actors_list = []
            for actor_tag in all_actors_tag[:-1]:  # excluding last one since its a more/less details link
                actor_url = f"https://www.csfd.cz/{actor_tag['href']}"
                actor_name = actor_tag.text.strip()
                try:
                    the_actor = Actor.objects.get(url=actor_url)
                except Actor.DoesNotExist:
                    the_actor = Actor.objects.create(url=actor_url, name=actor_name,
                                                     name_unified=unidecode.unidecode(actor_name))
                actors_list.append(the_actor)
            movie.actors.add(*actors_list)

        else:
            raise CommandError(f'Cannot get data from {movie.url} - status code: {r.status_code}')
