from collections.abc import Generator

from csvclean.models.config import Configuration

from .cleaners import LineOrchestrator
from .IO_layer import CSVIOlayer
from .models import LineError
from .reporters import Report
from .validators import ValidatorManager


def base_process(csv_path: str, outputpath: str, do_report: bool):
    """
    Base Process to organize all classes of CSV Cleanner

    :param csv_path: path of the csv to clean
    :type csv_path: str
    :param outputpath: path to save the new clean csv
    :type outputpath: str
    :param do_report: Boolean to decide if a report is desired
    :type do_report: bool
    """

    io_layer = CSVIOlayer(output_path=outputpath)
    configurate: Configuration = io_layer.parse_config("tests\\fixtures\\config.txt")
    csv_reader_generator: Generator = io_layer.read_csv(csv_path)

    cleanner = LineOrchestrator(configurate)

    reporter = Report()

    validator = ValidatorManager()

    while True:
        try:
            type, csv_row = next(csv_reader_generator)

            if type != "__header__":
                errors_detected: LineError = validator.validate(data=csv_row, config=configurate)

                csv_row_clean, data_errors = cleanner.process(csv_row, errors_detected)

                if do_report:
                    reporter.count_errors(data_errors)

            else:
                csv_row_clean = csv_row

            if csv_row_clean != []:
                io_layer.write(outputpath, csv_row_clean)

        except StopIteration:
            reporter.do_report()
            break
