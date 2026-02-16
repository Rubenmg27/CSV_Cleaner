from typing import Any

from csvclean.models import Configuration


class DataValidator:
    """Reusable validator for common data checks in "validators" package."""

    @staticmethod
    def require_configuration(data: Any, name: str = "data") -> Configuration:
        """
        Ensure input is a Configuration object

        :param data: Input to validate
        :type data: Any
        :param name: Name for error messages
        :type name: str
        :return: Validated configuration object
        :rtype: Configuration
        :raises TypeError: If not a Configuration object
        """
        if not isinstance(data, Configuration):
            raise TypeError(f"{name} must be Configuration object, got {type(data).__name__}")
        return data

    @staticmethod
    def require_configuration__header_types(
        config: Configuration, name: str = "data"
    ) -> None:
        """
        Ensure configuration has header_types no empty

        :param config: Configuration to validate
        :type config: Configuration
        :param name: Name for error messages
        :type name: str
        :raises ValueError: No type
        """

        if len(config.header_types) > 0:
            raise ValueError(f"{name} must has types in the list rather than to be a empty list")

    @staticmethod
    def require_type(data: Any, name: str = "data") -> type:
        """
        Ensure input is a type

        :param data: Input to validate
        :type data: Any
        :param name: Name for error messages
        :type name: str
        :return: Validated type
        :rtype: type
        :raises TypeError: If not a type
        """
        if not isinstance(data, type):
            raise TypeError(f"{name} must be type, got {type(data).__name__}")
        return data

    @staticmethod
    def require_list_str(data: Any, name: str = "data") -> list[str]:
        """
        Ensure input is a list[str]

        :param data: Input to validate
        :type data: Any
        :param name: Name for error messages
        :type name: str
        :return: Validated list[str]
        :rtype: list[str]
        :raises TypeError: If not a list[str]
        """
        if not isinstance(data, list) and all(isinstance(element, str) for element in data):
            raise TypeError(f"{name} must be list[str], got {type(data).__name__}")
        return data
