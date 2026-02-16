from pathlib import Path

import pytest

from csvclean.models.data_register import ErrorTypes, LineError
from csvclean.reporters.cleaning_report import Report


@pytest.mark.parametrize(
    "errors, expected",
    argvalues=[
        ({1: ErrorTypes.NULL, 2: ErrorTypes.NULL}, {"null": 2, "type": 0, "total": 2}),
        ({1: ErrorTypes.TYPE, 2: ErrorTypes.NULL}, {"null": 1, "type": 1, "total": 2}),
        ({}, {"null": 0, "type": 0, "total": 0}),
    ],
    ids=["only_null", "mix_errors", "any_error"],
)
def test_count_errors(errors: LineError, expected: dict[str, int]):
    """
    Docstring for test_count_errors

    :param tmp_path: Description
    :type tmp_path: Path
    """
    reporter = Report()

    reporter.count_errors(errors)

    assert reporter.count_errors_by_type[ErrorTypes.NULL] == expected["null"]
    assert reporter.count_errors_by_type[ErrorTypes.TYPE] == expected["type"]
    assert reporter.total_errors == expected["total"]


def test_correct_report(tmp_path: Path):
    """ """
    report = Report()

    errors1 = {0: ErrorTypes.NULL, 1: ErrorTypes.TYPE}
    errors2 = {2: ErrorTypes.NULL}

    report.count_errors(errors1)
    report.count_errors(errors2)

    report_path = tmp_path / "report.txt"

    report.do_report(str(report_path))

    content = report_path.read_text(encoding="utf-8").splitlines()

    expected = [
        f"There are 2 of {ErrorTypes.NULL}.",
        f"There are 1 of {ErrorTypes.TYPE}.",
        "There were 3 errors in total.",
        "2 rows has been fixed.",
    ]

    assert content == expected
