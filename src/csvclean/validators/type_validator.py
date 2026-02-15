from typing import ClassVar
from csvclean.models.data_register import ErrorTypes, LineErrors, CsvContent
from csvclean.models.config import Configuration

from .base_validator import BaseValidator
from .data_validator import DataValidator
import pandas as pd
import re


class TypeValidator(BaseValidator):
    # def is_incorrect_type(self, value: CsvContent, expected_type: type) -> bool:
    #     """
    #         Check of "value" has the same type than expected_type

    #         :param value: Value to check
    #         :type line: CsvContent
    #         :param expected_type: Expected tipe in value
    #         :type expected_type: type
    #         :return: Boolean to indicate if is not the expected type
    #         :rtype: bool
    #     """
    #     DataValidator.require_csvcontent(value, "null_validator.is_incorrect_type.value")
    #     DataValidator.require_type(expected_type, "null_validator.is_incorrect_type.expected_type")


    #     return not isinstance(value, expected_type)

    def is_incorrect_type(self, value: str, expected_type: type) -> bool:
        """
            Check of "value" has the same type than expected_type

            :param value: Value to check
            :type line: CsvContent
            :param expected_type: Expected tipe in value
            :type expected_type: type
            :return: Boolean to indicate if is not the expected type
            :rtype: bool
        """
        # DataValidator.require_csvcontent(value, "null_validator.is_incorrect_type.value")
        DataValidator.require_type(expected_type, "null_validator.is_incorrect_type.expected_type")

        knonw_types: dict[str, str]= {
        "int": r"^-?\d+$",
        "float": r"^-?\d+\.\d+$",
        "str": r".+",  # Cualquier cadena que no esté vacía
        "bool": r"^(?i)(true|false|1|0|yes|no)$",
        "datetime": r"^\d{4}-\d{2}-\d{2}( \d{2}:\d{2}:\d{2})?$" # Formato ISO: YYYY-MM-DD o YYYY-MM-DD HH:MM:SS
        }


        return bool(re.fullmatch(knonw_types[expected_type.__name], value))

    def validate_line(self, line: list[str], config: Configuration) -> LineErrors:
        """
            Validate there is not type errors in line

            :param line: Line to check
            :type line: pd.DataFrame
            :param config: Configuration of validator
            :type config: Configuration
            :return: List of type errors in line
            :rtype: list[LineError]
        """
        # DataValidator.require_one_row(line, "null_validator.validate_line.line")
        # DataValidator.require_configuration__header_types__columns(config, line)

        type_errors: LineErrors = {}

        for  column_number, element in enumerate(line):

            if self.is_incorrect_type(element, config.header_types[column_number]):
                type_errors[column_number] = ErrorTypes.TYPE


        return type_errors

        # type_errors: list[LineError] = []

        # dict_line: dict[str, dict[int, CsvContent]] = line.to_dict()

        # for  column_number, column_key in enumerate(dict_line):

        #     if self.is_incorrect_type(dict_line[column_key][0], config.header_types[column_number]):
        #         type_errors.append(LineError(column_number, ErrorTypes.TYPE))


        # return type_errors
