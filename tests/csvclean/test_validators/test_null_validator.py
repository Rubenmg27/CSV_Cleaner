import pytest

from csvclean.models.config import Configuration
from csvclean.models.data_register import ErrorTypes, LineError
from csvclean.validators.null_validator import NullValidator


@pytest.fixture
def sample_config() -> Configuration:
    """Configuration to check null validator"""
    return Configuration(header_types=[], trate_nullerror=True, trate_typeerror=False)


@pytest.mark.parametrize("input_text, expected", [
    ("23", False),
    ("45.23", False),
    ("safd", False),
    ("true", False),
    ("2020-3-23", False),
    ("", True),
], ids = [
    "content_int",
    "content_float",
    "content_str",
    "content_bool",
    "content_datetime",
    "content_null",
])
def test_is_null(input_text: str, expected: bool):
    assert NullValidator().is_null(input_text) == expected


@pytest.mark.parametrize("input_text, input_config, expected", [
    (["Mercado", "manzana", "45"], sample_config, {}),
    (["", "manzana", "45"], sample_config,
    {0: ErrorTypes.NULL}),
    (["Mercado", "", "45"], sample_config,
    {1: ErrorTypes.NULL}),
    (["Mercado", "manzana", ""], sample_config,
    {2: ErrorTypes.NULL}),
    (["", "", "45"], sample_config,
    {0: ErrorTypes.NULL, 1: ErrorTypes.NULL}),

], ids = [
    "content_without_null_errors",
    "null_error_in_column_0",
    "null_error_in_column_1",
    "null_error_in_column_2",
    "null_error_in_three_columns",
])
def test_validate_line(input_text: list[str], input_config: Configuration, expected: LineError):
    assert NullValidator().validate_line(input_text, input_config) == expected
