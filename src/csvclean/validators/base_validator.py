from abc import ABC, abstractmethod

import pandas as pd

from csvclean.models.data_register import LineError, ValidationError

from .null_validator import NullValidator


class BaseValidator(ABC):

    @abstractmethod
    def validate_line(self, line: list[str | int]) -> list[LineError]: ...


    def validate_file(self, data: pd.DataFrame) -> ValidationError:
        validation_errors: ValidationError = ValidationError({})

        for line_number, row in enumerate(data.iterrows()):

            line: list[str | int] =  list(row[1])

            errors: list[LineError] = []

            errors += NullValidator().validate_line(line)
            ##  MORE ERRORS
            ##  errors +=

            if errors != []:
                validation_errors.error[line_number] = errors

        return validation_errors





    def validate(self, data: str | pd.DataFrame) -> ValidationError:
        if isinstance(data, str):
            pass #PARA LINEA
        else:
            return self.validate_file(data)
        return ValidationError({})
