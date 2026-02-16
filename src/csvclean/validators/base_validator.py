from abc import ABC, abstractmethod

from csvclean.models.config import Configuration
from csvclean.models.data_register import LineError

# from .data_validator import DataValidator
from .null_validator import NullValidator
from .type_validator import TypeValidator


class BaseValidator:
    @classmethod
    def join_validation_errors(
        cls, current_errors: LineError, added_errors: LineError
    ) -> LineError:
        """
        FALTA POR RELLENAR Y HACER VALIDACION DE TIPOS
        """
        new_errors: LineError = current_errors

        for key, value in added_errors.items():
            if key not in current_errors:
                new_errors[key] = value

        return new_errors

    @classmethod
    def validate(cls, data: list[str], config: Configuration) -> LineError:
        """
        Validate data with the specified validators in the configuration

        :param data: Data to check
        :type data: list[str]
        :param config: Configuration of validator
        :type config: Configuration
        :return: List of errors in data
        :rtype: DataError
        """

        # DataValidator.require_dataframe(data, "base_validator.validate.data")
        # DataValidator.require_configuration(config, "base_validator.validate.config")

        validation_errors: LineError = {}

        if config.trate_nullerror:
            null_errors: LineError = NullValidator().validate_line(data, config)
            if len(null_errors.keys()) > 0:
                validation_errors = cls.join_validation_errors(validation_errors, null_errors)

        if config.trate_typeerror:
            type_errors: LineError = TypeValidator().validate_line(data, config)
            if len(type_errors.keys()) > 0:
                validation_errors = cls.join_validation_errors(validation_errors, type_errors)

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
