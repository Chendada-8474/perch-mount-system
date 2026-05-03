import flask
import http


class _HTTPError(Exception):
    status_code = 0

    def __init__(self, message: str):
        self.message = message

    def json_response(self):
        response = flask.jsonify({"message": self.message})
        response.status_code = self.status_code
        return response


class _ClientError(_HTTPError):
    def __init__(self, message):
        super().__init__(message)


class _ServerError(_HTTPError):
    def __init__(self, message):
        super().__init__(message)


class Unauthorized(_ClientError):
    status_code = http.HTTPStatus.UNAUTHORIZED

    def __init__(self, message):
        super().__init__(message)


class NotFoundError(_ClientError):
    status_code = http.HTTPStatus.NOT_FOUND

    def __init__(self, message):
        super().__init__(message)


class BadRequestError(_ClientError):
    status_code = http.HTTPStatus.BAD_REQUEST

    def __init__(self, message):
        super().__init__(message)


class StringQueryMissingError(BadRequestError):
    def __init__(self, required_field: str):
        message = f"'{required_field}' is a required field in string query."
        super().__init__(message)


class StatusError(BadRequestError):
    def __init__(self, status: str):
        message = f"this operation is not allowed in '{status}' status."
        super().__init__(message)


class UploadMediaCanNotBeEmptyError(BadRequestError):
    def __init__(self, message):
        message = "uploaded media can not be empty."
        super().__init__(message)


class SuperAdminUnpatchableError(BadRequestError):
    def __init__(self, message="attributes of super admin is not able to be updated."):
        super().__init__(message)


class MediaStatusError(BadRequestError):
    def __init__(self, message="this status now allow this operation."):
        super().__init__(message)


class MediaStatusRollbackError(BadRequestError):
    def __init__(self, message="Status rollback only form reviewed to unreviewed."):
        super().__init__(message)


class ResourceNotFoundError(NotFoundError):
    def __init__(self, resource_name: str):
        message = f"{resource_name} not found."
        super().__init__(message)


class SectionAlreadyGotDataError(BadRequestError):
    def __init__(
        self, message="This section already got data. It's not a new section."
    ):
        super().__init__(message)
