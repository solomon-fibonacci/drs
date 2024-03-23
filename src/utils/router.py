from functools import wraps
import logging
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi import HTTPException, status
from errors import (
    TokenValidationError,
    UserPermissionError,
    ConflictError,
    ValidationError,
    NotFoundError,
    UnauthorisedError,
    FileTooLargeError,
    UnsupportedMediaTypeError,
    RateLimitError,
)

logger = logging.getLogger(__name__)


def error_handler(route_function):

    @wraps(route_function)
    async def wrapper(*args, **kwargs):
        try:
            return await route_function(*args, **kwargs)
        except ValueError as value_error:
            logger.exception(value_error)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid argument")

        except ValidationError as validation_error:
            logger.exception(validation_error)
            raise HTTPException(status_code=status.HTTP_422_BAD_REQUEST,
                                detail=str(validation_error))

        except ConflictError as conflict_error:
            logger.exception(conflict_error)
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=str(conflict_error))

        except TokenValidationError as token_validation_error:
            logger.exception(token_validation_error)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to authenticate user",
            )
        except UnauthorisedError as unauthorised_error:
            logger.exception(unauthorised_error)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is not authorised for this action",
            )

        except UserPermissionError as user_permission_error:
            logger.exception(user_permission_error)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(
                    "User does not have the required permission to perform this operation"
                ),
            )

        except NotFoundError as not_found_error:
            logger.exception(not_found_error)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=str(not_found_error))

        except UnsupportedMediaTypeError as unsupported_media_type_error:
            logger.exception(unsupported_media_type_error)
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=str(unsupported_media_type_error),
            )

        except FileTooLargeError as file_too_large_error:
            logger.exception(file_too_large_error)
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=str(file_too_large_error),
            )

        except RateLimitError as rate_limit_error:
            logger.exception(rate_limit_error)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=str(rate_limit_error),
            )

        except HTTPException as http_exc:
            # Here you could add additional logging if needed
            print("re-raising HTTP exception")
            raise http_exc
        except Exception as e:
            # Additional logging for the general exception
            logger.exception("Unexpected exception")
            logger.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong",
            )

    return wrapper


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


error_responses = {
    status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {
        "description": "File size exceeds the maximum allowed size",
    },
    status.HTTP_409_CONFLICT: {
        "description": "Conflict error",
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Not found",
    },
    status.HTTP_403_FORBIDDEN: {
        "description":
        "User does not have the required permission to perform this operation",
    },
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Unable to authenticate user",
    },
    status.HTTP_400_BAD_REQUEST: {
        "description": "Invalid request body",
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal server error",
    },
}

get_error_responses = {
    **error_responses,
    status.HTTP_404_NOT_FOUND: {
        "description": "Not found",
    },
}
