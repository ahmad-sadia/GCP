from unittest.mock import patch
from backend.handlers.constants import OMDB_URL, OMDB_API_KEY, OMDB_MOVIES_WORD_TITLE, OMDB_PAGES_COUNT

from backend import test

from backend.models.movie import Movie


class TestMovie(test.TestCase):

    def test_create_movie(self):
        _title = 'title1'
        _year = '2000'
        movie = Movie.create(title='title1', year='2000')
        self.assertIsNotNone(movie)
        self.assertEqual(movie.title, _title)
        self.assertEqual(movie.year, _year)
        self.assertIsNotNone(movie.created)
        self.assertIsNotNone(Movie.get_by_id(movie.key.id()))

    # TODO: TEST ASSERTION (ERRORS)

    def test_batch_create(self):
        old_count = Movie.query().count()
        movies = []
        mov1 = Movie(title='title1', year='2001')
        mov2 = Movie(title='title2', year='2002')
        movies.extend([mov1, mov2])
        Movie.batch_create(movies)
        self.assertEqual(old_count + 2, Movie.query().count())


class TestMovieApi(test.TestCase):
    @patch('backend.handlers.movies.requests.get')
    def test_create(self, fetch_100_movies):
        movie = {
            'title': 'The Lord of the Rings: The Fellowship of the Ring',
            'poster': 'https://m.media-amazon.com/images/M/MV5BN2EyZjM3NzUtNWUzMi00MTgxLWI0NTctMzY4M2VlOTdjZWRiXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_SX300.jpg',
            'imdb_id': 'tt0120737',
            'year': '2001',
            'type': 'movie',

        }
        resp = self.api_client.post('movie.create', movie)
        self.assertEqual(resp.get('error'), None)
        self.assertEqual(resp.get('title'), movie['title'])
        self.assertEqual(resp.get('type'), movie['type'])
        self.assertEqual(resp.get('year'), movie['year'])
        self.assertEqual(resp.get('imdb_id'), movie['imdb_id'])
        self.assertEqual(resp.get('poster'), movie['poster'])

        resp = self.api_client.post('movie.get', dict(title=movie['title']))
        fetch_100_movies.assert_not_called()
        self.assertEqual(resp.get('error'), None)

    @patch('backend.handlers.movies.requests.get')
    def test_list(self, fetch_100_movies):
        movies = []
        for i in range(10):
            mov = Movie(title=f'title{i}', year=f'200{i}', poster='https://m.media-amazon.com/images/M/MV5B')
            movies.append(mov)
        movies.append(Movie(title='z', ))
        movies.append(Movie(title='a', ))
        movies.append(Movie(title='c', ))

        Movie.batch_create(movies)
        fetch_100_movies.assert_not_called()
        resp = self.api_client.post('movie.list', dict(offset=0, limit=10))
        fetch_100_movies.assert_not_called()
        self.assertEqual(len(resp.get('movies')), 10)
        self.assertEqual(resp.get('error'), None)

        resp = self.api_client.post('movie.list', dict(offset=0, limit=30))
        fetch_100_movies.assert_not_called()
        self.assertEqual(resp.get('error'), None)
        self.assertEqual(resp.get('movies')[-1]['title'], 'z')
        self.assertEqual(resp.get('movies')[0]['title'], 'a')
        self.assertEqual(len(resp.get('movies')), 13)

        # test default limits
        resp = self.api_client.post('movie.list')
        fetch_100_movies.assert_not_called()
        self.assertEqual(len(resp.get('movies')), 10)

    @staticmethod
    def _assert_calling_get_request(fetch_100_movies):
        fetch_100_movies.assert_called()
        fetch_100_movies.assert_called_with(
            url=f'{OMDB_URL}?apikey={OMDB_API_KEY}&type=movie&s={OMDB_MOVIES_WORD_TITLE}&page={OMDB_PAGES_COUNT}')

    @patch('backend.handlers.movies.requests.get')
    def test_attempting_to_populate_empty_db_on_list(self, fetch_100_movies):
        fetch_100_movies.assert_not_called()
        self.api_client.post('movie.list', dict(offset=0, limit=10))
        self._assert_calling_get_request(fetch_100_movies)

    @patch('backend.handlers.movies.requests.get')
    def test_attempting_to_populate_empty_db_on_get(self, fetch_100_movies):
        fetch_100_movies.assert_not_called()
        self.api_client.post('movie.get', dict(title='test'))
        self._assert_calling_get_request(fetch_100_movies)

    def test_delete_by_id(self):
        m = Movie.create(title='test_to be deleted', year='2000')
        res = self.api_client.post('movie.delete', dict(id=str(m.key.id())))
        self.assertEqual(res.get('error'), None)
        self.assertEqual(res, {})

