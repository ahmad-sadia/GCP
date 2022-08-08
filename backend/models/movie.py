import datetime

from google.cloud import ndb

from backend import error


class TitleInvalid(error.Error):
    pass


class YearInvalid(error.Error):
    pass


class TypeInvalid(error.Error):
    pass


class MovieNotFound(error.Error):
    pass


class VideoTypes:
    MOVIE = 100
    EPISODE = 200
    SERIES = 300


class Movie(ndb.Model):
    title = ndb.StringProperty(indexed=True)
    poster = ndb.StringProperty()
    imdb_id = ndb.StringProperty('iid')
    year = ndb.StringProperty()
    type = ndb.IntegerProperty(indexed=False, choices=(VideoTypes.MOVIE, VideoTypes.EPISODE, VideoTypes.SERIES),
                               default=VideoTypes.MOVIE)
    created = ndb.DateTimeProperty(indexed=False, auto_now_add=True)

    @classmethod
    def create(cls, title: str, year: str, type: str = 'movie', poster: str = None, imdb_id: str = None):
        if not title or len(title) > 1024:
            raise TitleInvalid(f'Invalid Title: {title}')
        if type:
            type = cls._set_type(type)
        try:
            if not 1888 <= int(year) <= datetime.datetime.now().year + 50:
                raise YearInvalid(
                    f'Year: {year} is invalid movie year. Valid year range is (1888-{datetime.datetime.now().year + 20}')
        except ValueError:
            raise YearInvalid('Number must be provided.')
        entity = cls(
            title=title,
            poster=poster,
            imdb_id=imdb_id,
            year=year,
            type=type,
        )
        entity.put()
        return entity

    @classmethod
    def batch_create(cls, movies: []):
        if movies:
            ndb.put_multi(movies)

    @classmethod
    def list(cls, offset: int = 0, limit: int = 10):
        return cls.query().order(Movie.title).fetch(offset=offset, limit=limit)

    @classmethod
    def get_by_title(cls, title: str):
        movie = cls.query(Movie.title == title).get()
        if movie is None or not isinstance(movie, cls):
            raise MovieNotFound(f'No movie with title: {title}')
        return movie

    @classmethod
    def delete_by_id(cls, _id: int):
        movie = Movie.get_by_id(_id)
        if movie is None or not isinstance(movie, cls):
            raise MovieNotFound(f'No movie with id: {_id}')
        movie.key.delete()

    @staticmethod
    def _set_type(_type: str) -> int:
        if _type == 'movie':
            return VideoTypes.MOVIE
        elif _type == 'episode':
            return VideoTypes.EPISODE
        elif _type == 'series':
            return VideoTypes.SERIES
        else:
            raise TypeInvalid(f'Invalid Type: {_type}')

    @staticmethod
    def get_type(_type: int) -> str:
        if _type == VideoTypes.MOVIE:
            return 'movie'
        elif _type == VideoTypes.EPISODE:
            return 'episode'
        elif _type == VideoTypes.SERIES:
            return 'series'
        else:
            raise TypeInvalid(f'Invalid Type: {_type}')
