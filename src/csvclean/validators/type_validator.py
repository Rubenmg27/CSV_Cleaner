import re

from csvclean.models.config import Configuration
from csvclean.models.data_register import ErrorTypes, LineError

from .base_validator import BaseValidator
from .data_validator import DataValidator


class TypeValidator(BaseValidator):
    def is_incorrect_type(self, value: str, expected_type: type) -> bool:
        """
        Check of "value" has the same type than expected_type

        :param value: Value to check
        :type line: str
        :param expected_type: Expected tipe in value
        :type expected_type: type
        :return: Boolean to indicate if it is not the expected type
        :rtype: bool
        """
        DataValidator.require_type(expected_type, "null_validator.is_incorrect_type.expected_type")

        knonw_types: dict[str, str] = {
            "int": r"^-?\d+$",
            "float": r"^-?\d+\.\d+$",
            "str": r".+",
            "bool": r"^(?i)(true|false|1|0|yes|no)$",
            "datetime": r"^\d{4}-\d{2}-\d{2}( \d{2}:\d{2}:\d{2})?$",
        }

        return not bool(re.fullmatch(knonw_types[expected_type.__name__], value))

    def validate_line(self, line: list[str], config: Configuration) -> LineError:
        """
        Validate there is not type errors in line

        :param line: Line to check
        :type line: list[str]
        :param config: Configuration of validator
        :type config: Configuration
        :return: List of type errors in line
        :rtype: LineError
        """
        DataValidator.require_configuration__header_types(
            config, "type_validator.validate_line.config"
        )

        type_errors: LineError = {}

        for column_number, element in enumerate(line):
            if self.is_incorrect_type(element, config.header_types[column_number]):
                type_errors[column_number] = ErrorTypes.TYPE

        return type_errors
