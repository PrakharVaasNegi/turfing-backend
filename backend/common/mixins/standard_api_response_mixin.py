from typing import List

from common import response


class StandardAPIError:
    def __init__(self, err_type: str, message: str, key: str = None):
        self.error_type = err_type
        self.message = message
        self.key = key

    def get_serialized(self):
        error = {
            "error_type": self.error_type,
            "message": self.message,
        }
        if self.key:
            error["key"] = self.key
        return error


class StandardAPIResponseMixin:
    """
    Sample usage for data_response:
        return response.Ok(
            data=self.data_response(data=some_serialized_data)
        )

    Sample usage for error_response:
        return response.BadRequest(
            data=self.error_response(errors=[
                StandardAPIError(err_type="SomeError1", message="Error 1 message"),
            ])
        )
    """

    @classmethod
    def data_response(cls, data: dict = None):
        return {"result": data or {}}

    @classmethod
    def error_response(cls, errors: List[StandardAPIError]):
        serialized = []
        for error in errors:
            if type(error) is not StandardAPIError:
                raise ValueError("'errors' should be a list of StandardAPIError.")
            serialized.append(error.get_serialized())
        return {"errors": serialized}

    @classmethod
    def convert_serializer_errors(cls, serializer_errors) -> List[StandardAPIError]:
        errors = []
        for field, messages in serializer_errors.items():
            if isinstance(messages, list):
                for message in messages:
                    errors.append(
                        StandardAPIError(
                            err_type="ValidationError", message=str(message), key=field
                        )
                    )
            else:
                errors.append(
                    StandardAPIError(
                        err_type="ValidationError", message=str(messages), key=field
                    )
                )
        return errors
