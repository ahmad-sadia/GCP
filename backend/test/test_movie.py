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

        # Assuming OMDB is a trusted source.
        old_count = Movie.query().count()
        movies = []

        mov1 = Movie(title='title1', year='2001')
        mov2 = Movie(title='title2', year='2002')

        movies.extend([mov1, mov2])

        Movie.batch_create(movies)

        self.assertEqual(old_count + 2, Movie.query().count())

    # title = messages.StringField(1, required=True)
    # poster = messages.StringField(2, required=False)
    # imdb_id = messages.StringField(3, required=False)
    # year = messages.IntegerField(4, required=True)
    # type = messages.EnumField(VideoType.Type, 5, default='m', required=False)
class TestMovieApi(test.TestCase):
    def test_create(self):
        movie = {
            'title': 'The Lord of the Rings: The Fellowship of the Ring',
            'poster': 'https://m.media-amazon.com/images/M/MV5BN2EyZjM3NzUtNWUzMi00MTgxLWI0NTctMzY4M2VlOTdjZWRiXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_SX300.jpg',
            'imdb_id': 'tt0120737',
            'year': '2001',
            'type': 'movie',

        }
        resp = self.api_client.post("movie.create", movie)
        self.assertEqual(resp.get("error"), None)
        # resp = self.api_client.post("user.me", headers=dict(authorization=access_token))
        # self.assertEqual(resp.get("error"), None)
        # self.assertEqual(resp.get("email"), "test@gmail.com")
        # resp = self.api_client.post("user.get", dict(id=resp.get("id")), headers=dict(authorization=access_token))
        # self.assertEqual(resp.get("error"), None)

    def test_list(self):
        movies = []
        for i in range(10):
            mov = Movie(title=f'title{i}', year=f'200{i}', poster='"https://m.media-amazon.com/images/M/MV5B')
            movies.append(mov)
        mov1 = Movie(title='z', year=f'2001', poster='"https://m.media-amazon.com/images/M/MV5B')
        mov2 = Movie(title='a', year=f'2001', poster='"https://m.media-amazon.com/images/M/MV5B')
        mov3 = Movie(title='c', year=f'2001', poster='"https://m.media-amazon.com/images/M/MV5B')
        movies.append(mov1)
        movies.append(mov2)
        movies.append(mov3)

        Movie.batch_create(movies)

        resp = self.api_client.post("movie.list", dict(offset=0, limit=10))
        self.assertEqual(len(resp.get("movies")), 10)
        self.assertEqual(resp.get("error"), None)

        resp = self.api_client.post("movie.list", dict(offset=0, limit=30))
        self.assertEqual(resp.get("error"), None)
        self.assertEqual(resp.get("movies")[-1]['title'], 'z')
        self.assertEqual(resp.get("movies")[0]['title'], 'a')
        self.assertEqual(len(resp.get("movies")), 13)

        # test default offset and limits
        resp = self.api_client.post("movie.list")
        self.assertEqual(len(resp.get("movies")), 10)