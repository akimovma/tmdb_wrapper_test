from wrapper import registered
from .exceptions import NotAccessibleTMDBError


class Finder:

    def __init__(self, instance_name=None):
        if not instance_name:
            self.instance = None
            # TODO functionality for full search
            super().__init__()
            return
        self.instance = registered.get(instance_name, None)
        if not self.instance:
            raise NotImplementedError(
                f'There is no way to search in {instance_name}')

    def __str__(self):
        return f"<Finder ({self.instance if self.instance else 'full'})>"

    def __repr__(self):
        return f"<Finder ({self.instance if self.instance else 'full'})>"

    def search(self, text):
        return self.instance.search(text)

    def popular(self, count=10):
        if self.instance:
            return self.instance.popular(count)
        raise NotAccessibleTMDBError(
            "Can't perform popular search with this Finder. You can ask "
            "popular from Finder only with some entity(TV or similar)")
