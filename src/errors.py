class UserPermissionError(Exception):
    """Raise for user permission error"""


class EmailVerificationError(Exception):
    """Raise for email verification error"""


class TokenValidationError(Exception):
    """Raise for token validation error"""


class UnauthorisedError(Exception):
    """
    Raise for when user is not authorised for an action
    """


class ValidationError(Exception):
    """
    Raise when an invalid input is supplied from the client
    """


class RateLimitError(Exception):
    """
    Raise when the rate limit has been exceeded
    """


class ConflictError(Exception):
    """
    Raise when there is a conflict with the data
    """


class NotFoundError(Exception):
    """
    Raise when the resource is not found
    """


class UnsupportedMediaTypeError(Exception):
    """
    Raise when the media type is not supported
    """


class FileTooLargeError(Exception):
    """
    Raise when the file is too large
    """
