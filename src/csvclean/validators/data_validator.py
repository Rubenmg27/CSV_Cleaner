from typing import Any

import pandas as pd

from csvclean.models.config import Configuration
from csvclean.models.data_register import CsvContent
from typing import get_args


class DataValidator:
    """Reusable validator for common data checks in "validators" package."""

    @staticmethod
    def require_dataframe(
        data: Any,
        name: str = "data",
    ) -> pd.DataFrame:
        """
        Ensure input is a DataFrame.

        :param data: Input to validate
        :type data: Any
        :param name: Name for error messages
        :type name: str
        :return: Validated dataframe
        :rtype: pd.DataFrame
        :raises TypeError: If not a DataFrame
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError(
                f"{name} must be DataFrame, got {type(data).__name__}"
            )
        return data

    @staticmethod
    def require_one_row(
        df: pd.DataFrame,
        name: str = "DataFrame"
    ) -> None:
        """
        Ensure input has only one row of content

        :param df: DataFrame to check
        :type df: pf.DataFrame
        :param name: Name for error messages
        :type name: str
        :raises ValueError: DataFrame has not one row of content
        """

        for column_key in df.columns:
            rows_number_in_column = len(df[column_key])
            if(not rows_number_in_column == 1):
                raise ValueError(
                    f"{name} must has only one row in its content, column: {column_key}"
                )

    @staticmethod
    def require_configuration(
        data: Any,
        name: str = "data"
    ) -> Configuration:
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
            raise TypeError(
                f"{name} must be Configuration object, got {type(data).__name__}"
            )
        return data

    @staticmethod
    def require_configuration__header_types__columns(
        config: Configuration,
        df: pd.DataFrame,
        name: str = "Configuration_header_types"
    ) -> None:
        """
        Ensure configuration has header_types with the same number
        of columns than DataFrame

        :param config: Configuration to validate
        :type config: Configuration
        :param df: Reference DataFrame
        :type df: pd.DataFrame
        :param name: Name for error messages
        :type name: str
        :raises ValueError: Incorrect number of elements in list of type of configuration
        """

        if len(config.header_types) != len(df.columns):
            raise ValueError(
                f"{name} must has the same number of columns than DataFrame line"
            )

    @staticmethod
    def require_csvcontent(
        data: Any,
        name: str = "data"
    ) -> CsvContent:
        """
        Ensure input has CsvContent type

        :param data: Input to validate
        :type data: Any
        :param name: Name for error messages
        :type name: str
        :return: Validated csvcontent
        :rtype: CsvContent
        :raises TypeError: If not a CsvContent
        """
        if not isinstance(data, get_args(CsvContent)):
            raise TypeError(
                f"{name} must has CsvContent type, got {type(data).__name__}"
            )
        return data

    @staticmethod
    def require_type(
        data: Any,
        name: str = "data"
    ) -> type:
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
            raise TypeError(
                f"{name} must be type, got {type(data).__name__}"
            )
        return data

