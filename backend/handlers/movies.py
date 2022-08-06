from typing import Dict, Any, Optional, List

# from google.appengine.api import urlfetch
import requests

from backend.handlers.constants import OMDB_API_KEY, OMDB_URL

# json.loads(res.content.decode('utf8').replace("'", '"'))
from backend.models.movie import Movie


def _fetch_first_100_movies_by_title(title: str) -> Optional[List[Any]]:
    if not title or type(title) is not str:
        return None
    result = []
    pages_count = 1  # todo 1, 11
    for i in range(1, pages_count):
        res = requests.get(url=_build_omdb_url(title, i))
        if res.status_code == 200:
            res_json = res.json()
            if res_json['Response'] == 'True':
                result += [Movie(title=m['Title'], year=int(m['Year'])) for m in res_json['Search']]
            else:
                break
        else:
            break
    return result


def _build_omdb_url(search: str, page: int):
    return f'{OMDB_URL}?apikey={OMDB_API_KEY}&type=movie&s={search}&page={page}'
