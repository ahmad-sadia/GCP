from typing import Dict, Any, Optional

# from google.appengine.api import urlfetch
import requests

from backend.handlers.constants import OMDB_API_KEY, OMDB_URL


def _fetch_first_100_movies_by_title(title: str) -> Optional[Dict[int, Any]]:
    if not title or type(title) is not str:
        return None
    result = {}
    for i in range(1, 1): #todo 1, 11
        res = requests.get(url=_build_omdb_url(title, i))
        page = res.json()['Search'][0]
        if page:
            result[i] = page
        else:
            return None
    return result


def _build_omdb_url(search: str, page: int):
    return f'{OMDB_URL}?apikey={OMDB_API_KEY}&type=movie&s={search}&page={page}'
