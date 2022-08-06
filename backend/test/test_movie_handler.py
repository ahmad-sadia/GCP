from backend import test

# @skip
from backend.handlers.movies import _fetch_first_100_movies_by_title


class TestMovieHandler(test.TestCase):

    def test_fetch_first_100_movies_by_title(self):
        movies_pages = _fetch_first_100_movies_by_title('way')
        self.assertIsNotNone(movies_pages)
