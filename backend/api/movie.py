import time

from backend.models.movie import Movie as MovieModel
from backend.wsgi import remote, messages

from backend import api
from backend.swagger import swagger


class VideoType(messages.Message):

    class Type(messages.Enum):
        MOVIE = 'm'
        EPISODE = 'e'
        SERIES = 's'


class CreateRequest(messages.Message):
    title = messages.StringField(1, required=True)
    poster = messages.StringField(2, required=False)
    imdb_id = messages.StringField(3, required=False)
    year = messages.IntegerField(4, required=True)
    type = messages.EnumField(VideoType.Type, 5, default='m', required=False)


class GetMoviesResponse(messages.Message):
    movies = messages.MessageField(CreateRequest, 1, repeated=True)


@api.endpoint(path="movie", title="Movie API")
class Movie(remote.Service):
    @swagger("Create a movie")
    @remote.method(CreateRequest, GetMoviesResponse)
    def create(self, request):
        movie = MovieModel.create(title=request.title,
                                  poster=request.poster,
                                  imdb_id=request.imdb_id, year=request.year,
                                  type=request.type
                                  )
        return GetMoviesResponse(
            title=movie.title,
            poster=movie.movie,
            imdb_id=movie.imdb_id,
            year=movie.year,
            type=movie.type,
        )
