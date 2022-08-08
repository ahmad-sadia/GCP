from typing import Any, Optional, List

import requests
from backend.handlers.constants import OMDB_API_KEY, OMDB_URL, OMDB_PAGES_COUNT
from backend.models.movie import Movie


def _fetch_100_movies_by_a_word_in_a_title(word: str) -> Optional[List[Any]]:
    if not word or type(word) is not str:
        return None
    result = []
    for i in range(1, OMDB_PAGES_COUNT + 1):
        res = requests.get(url=_build_omdb_url(word, i))
        if res.status_code == 200:
            res_json = res.json()
            if res_json['Response'] == 'True':
                result += [Movie(title=m['Title'], year=m['Year'], poster=m['Poster'], imdb_id=m['imdbID']) for m in res_json['Search']]
            else:
                break
        else:
            break
    return result


def _build_omdb_url(search: str, page: int):
    return f'{OMDB_URL}?apikey={OMDB_API_KEY}&type=movie&s={search}&page={page}'
