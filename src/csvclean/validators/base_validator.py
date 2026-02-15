from abc import ABC, abstractmethod

import pandas as pd

from csvclean.models.data_register import LineErrors
from csvclean.models.config import Configuration

from .null_validator import NullValidator
from .type_validator import TypeValidator
from .data_validator import DataValidator
from csvclean.validators import null_validator



class BaseValidator(ABC):

    @abstractmethod
    def validate_line(self, line: list[str], config: Configuration) -> LineErrors: ...

    def join_validation_errors(
        self,
        current_errors: LineErrors,
        added_errors: LineErrors
    ) -> LineErrors:
        """
        FALTA POR RELLENAR Y HACER VALIDACION DE TIPOS
        """
        new_errors: LineErrors = current_errors

        for key, value in added_errors.items():
            if key not in current_errors:
                new_errors[key] = value

        return new_errors


    def validate(self, data: list[str], config: Configuration) -> LineErrors:
        """
            Validate data with the specified validators in the configuration

            :param data: Data to check
            :type data: list[str]
            :param config: Configuration of validator
            :type config: Configuration
            :return: List of errors in data
            :rtype: DataError
        """

        #DataValidator.require_dataframe(data, "base_validator.validate.data")
        DataValidator.require_configuration(config, "base_validator.validate.config")

        validation_errors: LineErrors = {}

        if config.trate_NullError:
            null_errors: LineErrors = NullValidator().validate_line(data, config)
            if len(null_errors.keys()) > 0:
                validation_errors = self.join_validation_errors(validation_errors, null_errors)

        if config.trate_TypeError:
            type_errors: LineErrors = TypeValidator().validate_line(data, config)
            if len(type_errors.keys()) > 0:
                validation_errors = self.join_validation_errors(validation_errors, type_errors)

        return validation_errors



    # @abstractmethod
    # def validate_line(self, line: list[str | int]) -> list[LineError]: ...

    # def validate_file(self, data: pd.DataFrame) -> DataError:
    #     validation_errors: DataError = DataError({})

    #     for line_number, row in enumerate(data.iterrows()):

    #         line: list[str | int] =  list(row[1])

    #         errors: list[LineError] = []

    #         errors += NullValidator().validate_line(line)
    #         ##  MORE ERRORS
    #         ##  errors +=

    #         if errors != []:
    #             validation_errors.error[line_number] = errors

    #     return validation_errors


    # def validate(self, data: str | pd.DataFrame) -> DataError:
    #     if isinstance(data, str):
    #         pass #PARA LINEA
    #     # else:
    #     #     return self.validate_file(data)
    #     return DataError({})
