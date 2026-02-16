from csvclean.models.config import Configuration
from csvclean.models.data_register import ErrorTypes, LineError

from .base_validator import BaseValidator


class NullValidator(BaseValidator):
    def is_null(self, value: str) -> bool:
        """
        Check of "value" has a null value

        :param value: Value to check
        :type line: str
        :return: Boolean to indicate if it is null value
        :rtype: bool
        """

        return bool(value == "")


    def validate_line(self, line: list[str], config: Configuration) -> LineError:
        """
        Validate there is not null errors in line

        :param line: Line to check
        :type line: list[str]
        :param config: Configuration of validator
        :type config: Configuration
        :return: List of null errors in line
        :rtype: LineError
        """

        null_errors: LineError = {}

        # Puede que falta listar por el numero de columnas poruqe puede haber menos elementos de los debidos
        for column_number, element in enumerate(line):
            if self.is_null(element):
                null_errors[column_number] = ErrorTypes.NULL

        return null_errors
