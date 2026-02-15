from numpy import nan
from csvclean.models.data_register import ErrorTypes, LineErrors, CsvContent
from csvclean.models.config import Configuration

from .base_validator import BaseValidator
from .data_validator import DataValidator
import pandas as pd
from math import isnan

class NullValidator(BaseValidator):

    def is_null(self, value: str) -> bool:
        """
            Check of "value" has a null value

            :param value: Value to check
            :type line: CsvContent
            :return: Boolean to indicate if is null value
            :rtype: bool
        """

        # DataValidator.require_csvcontent(value, "value")

        return bool(pd.isna(value))


    # def is_null(self, value: CsvContent) -> bool:
    #     """
    #         Check of "value" has a null value

    #         :param value: Value to check
    #         :type line: CsvContent
    #         :return: Boolean to indicate if is null value
    #         :rtype: bool
    #     """

    #     DataValidator.require_csvcontent(value, "value")

    #     return bool(pd.isna(value))

    # def validate_line(self, line: list[str | int]) -> list[LineError]:
    #     null_errors: list[LineError] = []
    #     for column in range(1, len(line) + 1):

    #        if self.is_null(str(line[column - 1])):
    #             null_errors.append(LineError(column, ErrorTypes.NULL))

    #     return null_errors


    def validate_line(self, line: list[str], config: Configuration) -> LineErrors:
        """
            Validate there is not null errors in line

            :param line: Line to check
            :type line: pd.DataFrame
            :param config: Configuration of validator
            :type config: Configuration
            :return: List of null errors in line
            :rtype: list[LineError]
        """
        # DataValidator.require_one_row(line, "null_validator.validate_line.line")

        null_errors: LineErrors = {}

        #Puede que falta listar por el numero de columnas poruqe puede haber menos elementos de los debidos
        for  column_number, element in enumerate(line):

            if self.is_null(element):
                null_errors[column_number] = ErrorTypes.NULL

        return null_errors







    # def validate_line(self, line: pd.DataFrame, config: Configuration) -> list[LineError]:
    #     """
    #         Validate there is not null errors in line

    #         :param line: Line to check
    #         :type line: pd.DataFrame
    #         :param config: Configuration of validator
    #         :type config: Configuration
    #         :return: List of null errors in line
    #         :rtype: list[LineError]
    #     """
    #     # DataValidator.require_one_row(line, "null_validator.validate_line.line")

    #     null_errors: list[LineError] = []

    #     dict_line: dict[str, dict[int, CsvContent]] = line.to_dict()

    #     for  column_number, column_key in enumerate(dict_line):

    #         if self.is_null(dict_line[column_key][0]):
    #             null_errors.append(LineError(column_number, ErrorTypes.NULL))

    #     return null_errors
