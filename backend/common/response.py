"""
See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""

from rest_framework.response import Response


class Ok(Response):
    status_code = 200


class Created(Response):
    status_code = 201


class Accepted(Response):
    status_code = 202


class NoContent(Response):
    status_code = 204


class BadRequest(Response):
    status_code = 400


class UnAuthorized(Response):
    status_code = 401


class Forbidden(Response):
    status_code = 403


class NotFound(Response):
    status_code = 404


class Conflict(Response):
    status_code = 409


class TooManyRequests(Response):
    status_code = 429


class InternalServerError(Response):
    status_code = 500
