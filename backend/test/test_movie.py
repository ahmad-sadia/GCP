from unittest.mock import patch
from backend.handlers.constants import OMDB_URL, OMDB_API_KEY, OMDB_MOVIES_WORD_TITLE, OMDB_PAGES_COUNT

from backend import test

from backend.models.movie import Movie, VideoTypes, YearInvalid, TypeInvalid, TitleInvalid, MovieNotFound


class TestMovie(test.TestCase):

    def setUp(self):
        super().setUp()
        self.movie = {
            'title': 'The Lord of the Rings: The Fellowship of the Ring',
            'poster': 'https://m.media-amazon.com/images/M/MV5BN2EyZjM3NzUtNWUzMi00MTgxLWI0NTctMzY4M2VlOTdjZWRiXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_SX300.jpg',
            'imdb_id': 'tt0120737',
            'year': '2001',
            'type': 'movie',
        }

    def test_create_movie(self):
        movie = Movie.create(**self.movie)
        self.assertIsNotNone(movie)
        self.assertEqual(movie.title, self.movie['title'])
        self.assertEqual(movie.year, self.movie['year'])
        self.assertEqual(movie.poster, self.movie['poster'])
        self.assertEqual(movie.imdb_id, self.movie['imdb_id'])
        self.assertEqual(movie.type, VideoTypes.MOVIE)
        self.assertIsNotNone(movie.created)
        self.assertIsNotNone(Movie.get_by_id(movie.key.id()))

    def test_create_movie_failed(self):
        self.movie['year'] = '0'
        self.assertRaises(YearInvalid, lambda: Movie.create(**self.movie))

        self.movie['year'] = '-1'
        self.assertRaises(YearInvalid, lambda: Movie.create(**self.movie))

        self.movie['year'] = 'invalid input'
        self.assertRaises(YearInvalid, lambda: Movie.create(**self.movie))

        self.movie['year'] = '2000'
        self.movie['type'] = 'documentary'
        self.assertRaises(TypeInvalid, lambda: Movie.create(**self.movie))

        self.movie['title'] = ''
        self.assertRaises(TitleInvalid, lambda: Movie.create(**self.movie))

        long_title = '1234567890'
        for i in range(20):
            long_title += long_title

        self.movie['title'] = long_title
        self.assertRaises(TitleInvalid, lambda: Movie.create(**self.movie))

    def test_batch_create(self):
        old_count = Movie.query().count()
        movies = [Movie(title='title1', year='2001'), Movie(title='title2', year='2002')]
        Movie.batch_create(movies)
        self.assertEqual(old_count + 2, Movie.query().count())

    def test_get_by_title(self):
        movie = Movie.create(**self.movie)
        fetched_movie = Movie.get_by_title(self.movie['title'])

        self.assertIsNotNone(fetched_movie)
        self.assertEqual(movie.key.id(), fetched_movie.key.id())
        self.assertRaises(MovieNotFound, lambda: Movie.get_by_title('not existed movie title'))

    def test_delete_by_id(self):
        movie = Movie.create(**self.movie)
        old_count = Movie.query().count()
        Movie.delete_by_id(movie.key.id())
        self.assertEqual(old_count - 1, Movie.query().count())

        self.assertRaises(MovieNotFound, lambda: Movie.delete_by_id(1000))
        self.assertRaises(MovieNotFound, lambda: Movie.delete_by_id(-1))

    def test_set_and_get_type(self):
        self.assertEqual(Movie._set_type('movie'), VideoTypes.MOVIE)
        self.assertEqual(Movie._set_type('episode'), VideoTypes.EPISODE)
        self.assertEqual(Movie._set_type('series'), VideoTypes.SERIES)

        self.assertEqual(Movie.get_type(VideoTypes.MOVIE), 'movie')
        self.assertEqual(Movie.get_type(VideoTypes.EPISODE), 'episode')
        self.assertEqual(Movie.get_type(VideoTypes.SERIES), 'series')

    def test_list(self):
        movies = [Movie(title='title1', year='2001'), Movie(title='title2', year='2002')]
        Movie.batch_create(movies)

        movies = Movie.list(0, 1)
        self.assertEqual(len(movies), 1)

        movies = Movie.list(1, 2)
        self.assertEqual(len(movies), 1)

        movies = Movie.list(0, 2)
        self.assertEqual(len(movies), 2)

        movies = Movie.list(0, 10)
        self.assertEqual(len(movies), 2)

        movies = Movie.list(0, 0)
        self.assertEqual(len(movies), 2)


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
            url=f'{OMDB_URL}?apikey={OMDB_API_KEY}&type=movie&s={OMDB_MOVIES_WORD_TITLE}&page=1')

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
        resp = self.api_client.post("user.create", dict(email="test@gmail.com", password="test"))
        access_token = resp.get("access_token")

        m = Movie.create(title='test_to be deleted', year='2000')
        old_count = Movie.query().count()
        res = self.api_client.post('movie.delete', dict(id=str(m.key.id())), headers=dict(authorization=access_token))
        self.assertEqual(res.get('error'), None)
        self.assertEqual(res, {})
        self.assertEqual(old_count - 1, Movie.query().count())
