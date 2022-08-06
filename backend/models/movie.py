import datetime

from google.cloud import ndb

from backend import error


class TitleInvalid(error.Error):
    pass


class YearInvalid(error.Error):
    pass


class Movie(ndb.Model):

    def __int__(self):
        self.super(Movie, self).__init__()

    title = ndb.StringProperty(indexed=True)
    year = ndb.IntegerProperty(indexed=False)
    created = ndb.DateTimeProperty(indexed=False, auto_now_add=True)

    @classmethod
    def create(cls, title: str, year: int):
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