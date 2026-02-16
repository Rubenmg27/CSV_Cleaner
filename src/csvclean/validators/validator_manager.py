from csvclean.models import Configuration, LineError

from .data_validator import DataValidator
from .null_validator import NullValidator
from .type_validator import TypeValidator


class ValidatorManager:
    """
    Manage the validation of the input line, using the Nullvalidator and TypeValidator

    :atribute null_validator: Instance of NullValidator
    :type null_validator: NullValidator
    :atribute type_validator: Instance of TypeValidator
    :type type_validator: TypeValidator
    """

    def __init__(self):
        self.null_validator = NullValidator()
        self.type_validator = TypeValidator()


    def _join_validation_errors(
        self, current_errors: LineError, added_errors: LineError
    ) -> LineError:
        """
        Join the current errors whit the new detected errors. It has priority
        the first type error registered.

        :param current_errors: Current detected errors
        :type current_errors: LineError
        :param added_errors: New added errors
        :type added_errors: LineError
        :return: New current errors
        :rtype: LineError
        """

        new_errors: LineError = current_errors

        for key, value in added_errors.items():
            if key not in current_errors:
                new_errors[key] = value

        return new_errors


    def validate(self, data: list[str], config: Configuration) -> LineError:
        """
        Validate data with the specified validators in the configuration

        :param data: Data to check
        :type data: list[str]
        :param config: Configuration of validator
        :type config: Configuration
        :return: List of errors in data
        :rtype: LineError
        """

        DataValidator.require_list_str(data, "validator_manager.validate.data")
        DataValidator.require_configuration(config, "validator_manager.validate.config")

        validation_errors: LineError = {}

        if config.trate_nullerror:
            null_errors: LineError = self.null_validator.validate_line(data, config)
            if len(null_errors.keys()) > 0:
                validation_errors = self._join_validation_errors(validation_errors, null_errors)

        if config.trate_typeerror:
            type_errors: LineError = self.type_validator.validate_line(data, config)
            if len(type_errors.keys()) > 0:
                validation_errors = self._join_validation_errors(validation_errors, type_errors)

        return validation_errors

