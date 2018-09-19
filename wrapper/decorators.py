from wrapper import registered


def searchable(cls):
    """
    Registering decorator. Register all instances that
    apply search functionality
    """
    registered[cls.instance_name] = cls
    return cls
