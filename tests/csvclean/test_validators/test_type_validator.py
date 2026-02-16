import pytest

from csvclean.models.config import Configuration
from csvclean.models.data_register import ErrorTypes, LineError
from csvclean.validators.type_validator import TypeValidator


@pytest.mark.parametrize("input_text, expected_type, expected", [
    ("23", int, False),
    ("45.23", float, False),
    ("safd", str, False),

    ("23.", int, True),
    ("safd", int, True),
    ("true", float, True),
    ("", int, True),
], ids = [
    "recognize_int",
    "recognize_float",
    "recognize_str",

    "confused_float_rather_than_int",
    "confused_str_rather_than_int",
    "confused_bool_rather_than_float",
    "confused_str_rather_than_int",
])
def test_is_incorrect_type(input_text: str, expected_type: type, expected: bool):
    assert TypeValidator().is_incorrect_type(input_text, expected_type) == expected


@pytest.mark.parametrize("input_text, expected", [
    (["23.4", "manzana", "45"], {}),
    (["Manzana", "2020-3-23", "45"], {0: ErrorTypes.TYPE}),
    (["23.4", "", "45"], {1: ErrorTypes.TYPE}),
    (["23.4", "2020-3-23", "Manzana"], {2: ErrorTypes.TYPE}),
    (["Manzana", "Manzana", "Manzana"], {0: ErrorTypes.TYPE, 2: ErrorTypes.TYPE}),
], ids = [
    "content_with_correct_types_float_str_int",
    "incorrect_type_in_column_0_str_rather_than_float",
    "incorrect_type_in_column_1_str_rather_than_str",
    "incorrect_type_in_column_2_str_in_null_value",
    "incorrect_type_in_column_0_2_str_rather_than_float_int",
])
def test_validate_line(input_text: list[str], expected: LineError):
    input_config = Configuration(
        header_types=[float, str, int],
        trate_nullerror=False,
        trate_typeerror=True
    )

    assert TypeValidator().validate_line(input_text, input_config) == expected

