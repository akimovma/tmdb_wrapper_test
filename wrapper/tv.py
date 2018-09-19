from requests import HTTPError
from urllib.parse import urljoin

from . import session, ROOT_URL, TMDB_API_KEY, searchable, factories
from .exceptions import InvalidInputTMDBError, InvalidPropertyTMDBError
from .base import BaseInstance


@searchable
class TV(BaseInstance):
    instance_name = 'tv'
    URL_PATH = 'tv/'

    def __init__(self, show_id):
        super().__init__()
        self.id = show_id
        self._get_data_from_source()

    def __str__(self):
        return f"<TV show '{self.name}({self.first_air_date})'>"

    def __repr__(self):
        return f"<TV show '{self.name}({self.first_air_date})'>"

    def __getattr__(self, item):
        """
        We took every item from the cache.
        If we don't have such item - raise an Exception, maybe we need to
        update cache
        :param item: item to get from the instance
        :return: item from the response(stored in cache)
        """
        data = self._get_data_from_source()
        try:
            return data[item]
        except KeyError:
            raise InvalidPropertyTMDBError(
                "Tried bad property, if you sure that TV has such property"
                " - try to reload instance with calling instance.update()"
            )

    @classmethod
    def create(cls, data):
        show_id = data.get('id', None)
        if show_id:
            return cls(show_id)
        raise InvalidInputTMDBError

    @classmethod
    def search(cls, search_text, preferred_lang='en-US'):
        # TODO: Need to be removed to some Search class in future
        if not search_text:
            raise InvalidInputTMDBError('Search text must be not empty')
        # Todo: refactor and remove that creation of search URL
        path = '{}{}/{}'.format(ROOT_URL, 'search', 'tv')
        # update payload with search query
        payload = session.params
        payload['query'] = search_text
        payload['language'] = preferred_lang

        response = session.get(path, params=payload)
        try:
            response.raise_for_status()
        except HTTPError as e:
            raise InvalidInputTMDBError(f'Something bad happened on TMDB side.'
                                        f' Details - {e}') from None
        data = response.json()
        return factories.ShowFactory.get_tv(data.get('results', None))

    @staticmethod
    def _make_url(path, _full=False):
        if path and not isinstance(path, str):
            path = str(path)
        base_url = urljoin(ROOT_URL, TV.URL_PATH)
        url = urljoin(base_url, path)
        if not _full:
            return url
        url = urljoin(base_url, f"{path}?api_key={TMDB_API_KEY}")
        return url

    @staticmethod
    def popular(count=5):
        path = TV._make_url('popular')
        response = session.get(path)
        data = response.json()
        results = data.get('results', None)
        return factories.ShowFactory.get_tv(results, count)

    def _get_data_from_source(self, hard=False):
        """ Get data from TMDB to ssave it in cache
        If info was taken earlier, it takes that from the cache.
        """
        path = self._make_url(self.id)
        if hard:
            # hard = clear cache
            self.cache.delete_url(self._make_url(self.id, _full=True))
        response = session.get(path)
        try:
            response.raise_for_status()
        except HTTPError as e:
            # we remove all stack and raise our Exception with text from
            # cause exception
            raise InvalidInputTMDBError(f'Something bad happened on TMDB side.'
                                        f' Details - {e}') from None
        return response.json()

    def update(self):
        """
        Update method will clear cache if we have that and load the data.
        :return bool. True if we have cached page, False if we don't have that
        """
        full_url = self._make_url(self.id, _full=True)
        is_cached = self.cache.has_url(full_url)
        if is_cached:
            self._get_data_from_source(hard=True)
            return True
        self._get_data_from_source()
        return False

    def info(self):
        path = self._make_url(self.id)
        response = session.get(path)
        return response.json()
