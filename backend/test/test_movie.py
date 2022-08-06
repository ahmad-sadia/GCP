from backend import test

from backend.handlers.movies import _fetch_first_100_movies_by_title
from backend.models.movie import Movie


class TestMovie(test.TestCase):

    def test_create_movie(self):
        _title = 'title1'
        _year = 2000
        movie = Movie.create(title='title1', year=2000)
        self.assertIsNotNone(movie)
        self.assertEqual(movie.title, _title)
        self.assertEqual(movie.year, _year)
        self.assertIsNotNone(movie.created)
        self.assertIsNotNone(Movie.get_by_id(movie.key.id()))

    # TODO: TEST ASSERTION (ERRORS)

    def test_batch_create(self):

        # Assuming OMDB is a trusted source.
        old_count = Movie.query().count()
        movies = []

        mov1 = Movie(title='title1', year=2001)
        mov2 = Movie(title='title2', year=2002)

        movies.extend([mov1, mov2])

        Movie.batch_create(movies)

        self.assertEqual(old_count + 2, Movie.query().count())
