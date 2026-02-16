import datetime

import pytest

from csvclean.models import Configuration
from csvclean.models.data_register import ErrorTypes, LineError
from csvclean.validators.validator_manager import ValidatorManager


@pytest.fixture
def sample_config() -> Configuration:
    """Configuration to check validator manager"""
    return Configuration(
        header_types=[float, datetime, int],
        trate_nullerror=True,
        trate_typeerror=True
    )


@pytest.mark.parametrize("current_errors, added_errors, expected", [
    ({0: ErrorTypes.NULL},
    {2: ErrorTypes.TYPE},
    {0: ErrorTypes.NULL, 2: ErrorTypes.TYPE}),

    ({0: ErrorTypes.NULL},
    {0: ErrorTypes.TYPE},
    {0: ErrorTypes.NULL}),

    ({0: ErrorTypes.NULL, 1: ErrorTypes.NULL},
    {0: ErrorTypes.TYPE, 2: ErrorTypes.NULL},
    {0: ErrorTypes.NULL, 1: ErrorTypes.NULL, 2: ErrorTypes.NULL}),

], ids = [
    "correct_add_new_error",
    "correct_blocked_add_new_error",
    "correct_add_new_two_errors",
])

def test__join_validation_errors(
    current_errors: LineError,
    added_errors: LineError,
    expected: LineError
):
    assert ValidatorManager()._join_validation_errors(current_errors, added_errors) == expected

