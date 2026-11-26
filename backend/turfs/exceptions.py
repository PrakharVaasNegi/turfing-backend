class TurfNotFound(Exception):
    pass


class TurfAccessDenied(Exception):
    """Owner tried to touch a turf they do not own."""


class OwnerAlreadyExists(Exception):
    pass


class InvalidCredentials(Exception):
    pass
