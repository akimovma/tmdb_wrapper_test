
class BaseTMDBException(Exception):
    pass


class HTTPTMDBError(BaseTMDBException):
    pass


class InvalidInputTMDBError(BaseTMDBException):
    pass


class InvalidPropertyTMDBError(BaseTMDBException):
    pass

class NotAccessibleTMDBError(BaseTMDBException):
    pass