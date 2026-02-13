from csvclean.models.data_register import ErrorTypes, LineError

from .base_validator import BaseValidator


class NullValidator(BaseValidator):

    def is_null(self, value: str) -> bool:
        return value == ""

    def validate_line(self, line: list[str | int]) -> list[LineError]:
        null_errors: list[LineError] = []
        for column in range(1, len(line) + 1):

           if self.is_null(str(line[column - 1])):
                null_errors.append(LineError(column, ErrorTypes.NULL))

        return null_errors

