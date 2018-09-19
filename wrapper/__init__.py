import os
import requests
import requests_cache

TMDB_API_KEY = os.environ.get('TMDB_API_KEY', None)
ROOT_URL = 'https://api.themoviedb.org/3/'


class APIKeyMissingError(Exception):
    pass


if TMDB_API_KEY is None:
    raise APIKeyMissingError(
        "All methods require an API key. See "
        "https://developers.themoviedb.org/3/getting-started/introduction "
        "for how retrieve an authentication token from The Movie Database")


# we will add caching to not sending requests every time we need info for the
# same service(For example TV show)
requests_cache.install_cache(cache_name='tmdb_cache',
                             backend='redis',
                             expire_after=1360)

session = requests.Session()
session.params['api_key'] = TMDB_API_KEY

registered = dict()

from .decorators import searchable
from .search import Finder
from . import factories
from .tv import TV
