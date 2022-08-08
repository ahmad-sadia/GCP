import time

from backend.handlers.constants import OMDB_MOVIES_WORD_TITLE
from backend.handlers.movies import _fetch_100_movies_by_a_word_in_a_title
from backend.models.movie import Movie as MovieModel
from backend.wsgi import remote, messages

from backend import api
from backend.swagger import swagger
from backend.oauth2 import oauth2, Oauth2


class CreateRequest(messages.Message):
    title = messages.StringField(1, required=True)
    poster = messages.StringField(2, required=False)
    imdb_id = messages.StringField(3, required=False)
    year = messages.StringField(4, required=True)
    type = messages.StringField(5, required=False)


class GetRequest(messages.Message):
    title = messages.StringField(1, required=True)


class GetResponse(messages.Message):
    title = messages.StringField(1)
    poster = messages.StringField(2)
    imdb_id = messages.StringField(3)
    year = messages.StringField(4)
    type = messages.StringField(5)


class ListMoviesRequest(messages.Message):
    limit = messages.IntegerField(1, default=10)
    offset = messages.IntegerField(2, default=0)


class ListMoviesResponse(messages.Message):
    movies = messages.MessageField(GetResponse, 1, repeated=True)
    page = messages.IntegerField(2)


@api.endpoint(path="movie", title="Movie API")
class Movie(remote.Service):
    @swagger("Create a movie")
    @remote.method(CreateRequest, GetResponse)
    def create(self, request):
        movie = MovieModel.create(title=request.title, poster=request.poster,
                                  imdb_id=request.imdb_id, year=request.year,
                                  _type=request.type
                                  )
        return GetResponse(
            title=movie.title,
            poster=movie.poster,
            imdb_id=movie.imdb_id,
            year=movie.year,
            type=MovieModel.get_type(movie.type),
        )

    @swagger("Get a movie by title")
    @remote.method(GetRequest, GetResponse)
    def get(self, request):
        if MovieModel.query().count() == 0:
            MovieModel.batch_create(_fetch_100_movies_by_a_word_in_a_title(OMDB_MOVIES_WORD_TITLE))

        movie = MovieModel.get_by_title(request.title)
        return GetResponse(
            title=movie.title,
            poster=movie.poster,
            imdb_id=movie.imdb_id,
            year=movie.year,
            type=MovieModel.get_type(movie.type),
        )

    @swagger("List movies")
    @remote.method(ListMoviesRequest, ListMoviesResponse)
    def list(self, request):
        if MovieModel.query().count() == 0:
            MovieModel.batch_create(_fetch_100_movies_by_a_word_in_a_title(OMDB_MOVIES_WORD_TITLE))

        movies = MovieModel.list(request.offset, request.limit)
        return ListMoviesResponse(movies=[GetResponse(
            title=m.title,
            poster=m.poster,
            imdb_id=m.imdb_id,
            year=m.year,
            type=MovieModel.get_type(m.type),
        ) for m in movies if m is not None])
