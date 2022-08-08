from backend import test
from unittest.mock import patch
# @skip
from backend.handlers.constants import OMDB_URL, OMDB_API_KEY, OMDB_MOVIES_WORD_TITLE, OMDB_PAGES_COUNT
from backend.handlers.movies import _fetch_100_movies_by_a_word_in_a_title


class TestMovieHandler(test.TestCase):

    @patch('backend.handlers.movies.requests.get')
    def test_fetch_first_100_movies_by_title(self, fetch_100_movies):
        fetch_100_movies().status_code = 200
        _fetch_100_movies_by_a_word_in_a_title(OMDB_MOVIES_WORD_TITLE, )
        fetch_100_movies.assert_called()
        fetch_100_movies.assert_called_with(
            url=f'{OMDB_URL}?apikey={OMDB_API_KEY}&type=movie&s={OMDB_MOVIES_WORD_TITLE}&page={OMDB_PAGES_COUNT}')
