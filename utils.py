import os

from requests import Response


class NotFoundError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class ForbiddenError(Exception):
    pass


class TooManyRequestsError(Exception):
    pass


def validate_response(response: Response):
    """Validate response for 401, 403, 404 and 429 status codes
    and raises corresponding error.
    """
    if response.status_code == 401:
        raise UnauthorizedError('401 Unauthorized')
    if response.status_code == 403:
        raise ForbiddenError('403 Forbidden')
    if response.status_code == 404:
        raise NotFoundError('404 Not Found')
    if response.status_code == 429:
        raise TooManyRequestsError('429 Too Many Requests')


def get_environment_variable(variable: str) -> str:
    """Return environment variable or raise Exception."""
    try:
        var = os.environ[variable]
        return var
    except KeyError:
        raise KeyError(f'Environment variable "{variable}" not set.')
