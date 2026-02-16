from pathlib import Path

from csvclean.models.data_register import ErrorTypes, LineError


class Report:
    """
    Class that count the errors and generate a report with them.

    :attribute count_errors_by_type: Number of errors by type.
    :type count_errors_by_type: dict{ErrorTypes: int}
    :attribute total_errors: Total of errors.
    :type total_errors: int
    :attribute fixed_rows: Number of fixed rows.
    :type fixed_rows: int
    """

    def __init__(self):
        """
        Initialize all counters to 0

        """
        self.count_errors_by_type = {
            ErrorTypes.NULL: 0,
            ErrorTypes.TYPE: 0,
        }
        self.total_errors = 0
        self.fixed_rows = 0

    def count_errors(self, errors: LineError):
        """
        Report the statistics into ./src/tests/fixtures/report.txt.

        :param errors: Dictionary with the errors in one row.
        :type errors: LineError
        """

        for _, error in errors.items():
            self.count_errors_by_type[error] += 1
            self.total_errors += 1

        if len(errors) > 0:
            self.fixed_rows += 1

    def do_report(self, report_path: str = "./tests/fixtures/report.txt"):
        """
        Do the report with the statics saved.

        :param report_path: path to save the report
        :type report_path: str
        """
        path: Path = Path(report_path)
        with path.open("w") as f:
            for type_error, count_error in self.count_errors_by_type.items():
                f.write(f"There are {count_error} of {type_error}.\n")

            f.write(f"There were {self.total_errors} errors in total.\n")
            f.write(f"{self.fixed_rows} rows has been fixed.")
