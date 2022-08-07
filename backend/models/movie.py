import datetime

from google.cloud import ndb

from backend import error


class TitleInvalid(error.Error):
    pass


class YearInvalid(error.Error):
    pass


class VideoTypes:
    MOVIE = 100
    EPISODE = 200
    SERIES = 300


class Movie(ndb.Model):

    title = ndb.StringProperty(indexed=True)
    poster = ndb.StringProperty()
    imdb_id = ndb.StringProperty('iid')
    year = ndb.IntegerProperty(indexed=False)
    type = ndb.IntegerProperty(indexed=False, choices=(VideoTypes.MOVIE, VideoTypes.EPISODE, VideoTypes.SERIES), default=VideoTypes.MOVIE)
    created = ndb.DateTimeProperty(indexed=False, auto_now_add=True)

    @classmethod
    def create(cls, title: str, poster: str, imdb_id: str, year: int, type: str):
        if not title or len(title) > 1024:
            raise TitleInvalid("Invalid Title.")
        if not 1888 <= year <= datetime.datetime.now().year + 50:
            raise YearInvalid(
                f"Year: {year} is invalid movie year. Valid year range is (1888-{datetime.datetime.now().year + 50}")
        entity = cls(
            title=title,
            year=year
        )
        entity.put()
        return entity

    @classmethod
    def batch_create(cls, movies: []):
        # Assuming OMDB is a trusted source.
        ndb.put_multi(movies)