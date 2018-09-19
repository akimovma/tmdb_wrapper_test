import abc

from wrapper.exceptions import HTTPTMDBError


class AbstractFactory(metaclass=abc.ABCMeta):

    @classmethod
    @abc.abstractclassmethod
    def get_tv(cls, data, count):
        return NotImplemented

    @classmethod
    @abc.abstractclassmethod
    def get_person(cls, data):
        return NotImplemented


class ShowFactory(AbstractFactory):

    @classmethod
    def get_tv(cls, data, count=None):
        from wrapper import TV

        if data is None:
            raise HTTPTMDBError('No data to show')

        if isinstance(data, list):
            tv_shows = list()
            if count and len(data) > count:
                for show in data[:count]:
                    tv_shows.append(TV.create(show))
            else:
                for show in data:
                    tv_shows.append(TV.create(show))
            return tv_shows
