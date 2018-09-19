from wrapper import registered


def searchable(cls):
    registered[cls.name] = cls
    return cls
