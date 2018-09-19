from wrapper import registered


def searchable(cls):
    """
    Registering decorator. Register all instances that
    apply search functionality
    """
    registered[cls.name] = cls
    return cls
