from requests import HTTPError

from . import session, ROOT_URL, TMDB_API_KEY, searchable
from .exceptions import InvalidInputTMDBError, InvalidPropertyTMDBError
from .base import BaseInstance


@searchable
class TV(BaseInstance):
    name = 'tv'
    URL_PATH = 'tv/'

    def __init__(self, show_id):
        super().__init__()
        self.id = show_id
        self._get_data_from_source()

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
    def search(cls, search_text, preferred_lang='en-US'):
        # TODO: Need to be removed to some Search class in future
        #
        if not search_text:
            raise InvalidInputTMDBError('Search text must be not empty')
        # Todo: refactor and remove that creation of search URL
        path = '{}{}/{}'.format(ROOT_URL, 'search', 'tv')
        # update paload wirh search query
        payload = session.params
        payload['query'] = search_text
        payload['language'] = preferred_lang

        response = session.get(path, params=payload)
        try:
            response.raise_for_status()
        except HTTPError as e:
            raise InvalidInputTMDBError(f'Something bad happened on TMDB side.'
                                        f' Details - {e}') from None
        # todo: return list of TV instances
        return response.json()

    @staticmethod
    def _make_url(path, _full=False):
        if not _full:
            return f'{ROOT_URL}{TV.URL_PATH}{path}'
        return f'{ROOT_URL}{TV.URL_PATH}{path}?api_key={TMDB_API_KEY}'

    @staticmethod
    def popular(count=0):
        # todo: return list[1..count] of TV instances
        path = TV._make_url('popular')
        response = session.get(path)
        return response.json()

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
