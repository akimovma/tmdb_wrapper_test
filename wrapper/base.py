import requests_cache
import abc


class BaseInstance(metaclass=abc.ABCMeta):

    def __init__(self):
        self.cache = requests_cache.get_cache()

    def __getattr__(self, item):
        return NotImplemented

    @classmethod
    @abc.abstractclassmethod
    def create(cls, data):
        return NotImplemented

    @classmethod
    @abc.abstractclassmethod
    def search(cls, search_text, preferred_lang):
        return NotImplemented

    @staticmethod
    @abc.abstractmethod
    def _make_url(path, _full=False):
        return NotImplemented

    def _get_data_from_source(self, hard=False):
        return NotImplemented

    def update(self):
        return NotImplemented
