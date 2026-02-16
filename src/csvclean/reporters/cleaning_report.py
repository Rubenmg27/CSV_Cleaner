from pathlib import Path

from csvclean.models.data_register import ErrorTypes, LineError


class Report:
    def __init__(self):
        self.count_errors_by_type = {
            ErrorTypes.NULL: 0,
            ErrorTypes.TYPE: 0,
        }
        self.total_errors = 0
        self.fixed_rows = 0

    def count_errors(self, errors: LineError):
        """
        Report the statistics into ./src/tests/fixtures/report.txt.

        :param errors: Dictionary with the errors in each row.
        :type errors: DataError
        """

        for _, error in errors.items():
            self.count_errors_by_type[error] += 1
            self.total_errors += 1

        if len(errors) > 0:
            self.fixed_rows += 1

    def do_report(self):
        path = Path("./tests/fixtures/report.txt")
        with path.open("w") as f:
            for type_error, count_error in self.count_errors_by_type.items():
                f.write(f"There are {count_error} of {type_error}.\n")

            f.write(f"There were {self.total_errors} errors in total.\n")
            f.write(f"{self.fixed_rows} rows has been fixed.")
