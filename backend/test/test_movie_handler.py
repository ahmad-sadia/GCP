from backend import test

# @skip
from backend.handlers.movies import _fetch_first_100_movies_by_title


class TestUser(test.TestCase):

    def test_fetch_first_100_movies_by_title(self):
        movies_pages = _fetch_first_100_movies_by_title('way')
        self.assertTrue(movies_pages is not None)

    # obj = user.User.create(email="test@gmail.com", password="test")
    #     self.assertEqual(obj, user.User.get(obj.id))
    #     self.assertTrue(obj.email == "test@gmail.com")
    #     self.assertTrue(obj.credentials.password != "test")
    #     self.assertRaises(user.EmailInvalid, lambda: user.User.create(email="test@", password="test"))
    #     user.User.create(email="test2@gmail.com", password=u"åäö")
