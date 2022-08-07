import time

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


class GetMovieResponse(messages.Message):
    title = messages.StringField(1)
    poster = messages.StringField(2)
    imdb_id = messages.StringField(3)
    year = messages.StringField(4)
    type = messages.StringField(5)


class ListMoviesRequest(messages.Message):
    limit = messages.IntegerField(1, default=10)
    offset = messages.IntegerField(2, default=0)


class ListMoviesResponse(messages.Message):
    movies = messages.MessageField(GetMovieResponse, 1, repeated=True)
    page = messages.IntegerField(2)


@api.endpoint(path="movie", title="Movie API")
class Movie(remote.Service):
    @swagger("Create a movie")
    @remote.method(CreateRequest, GetMovieResponse)
    def create(self, request):
        movie = MovieModel.create(title=request.title, poster=request.poster,
                                  imdb_id=request.imdb_id, year=request.year,
                                  _type=request.type
                                  )
        return GetMovieResponse(
            title=movie.title,
            poster=movie.poster,
            imdb_id=movie.imdb_id,
            year=movie.year,
            type=MovieModel.get_type(movie.type),
        )

    @swagger("List movies")
    @remote.method(ListMoviesRequest, ListMoviesResponse)
    def list(self, request):
        movies = MovieModel.list(request.offset, request.limit)
        return ListMoviesResponse(movies=[GetMovieResponse(
            title=m.title,
            poster=m.poster,
            imdb_id=m.imdb_id,
            year=m.year,
            type=MovieModel.get_type(m.type)
        ) for m in movies if m is not None])
