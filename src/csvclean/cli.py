from .cleaners import LineOrchestrator
from .IO_layer import CSVIOlayer
from .models import LineError
from .reporters import Report
from .validators import BaseValidator


def base_process(csv_path: str, outputpath: str, do_report: bool):
    """"""

    io_layer = CSVIOlayer(output_path=outputpath)
    configurate = io_layer.parse_config("tests\\fixtures\\config.txt")
    csv_reader_generator = io_layer.read_csv(csv_path)

    config = {
        "use_null": configurate.trate_nullerror,
        "use_type": configurate.trate_typeerror,
    }

    cleanner = LineOrchestrator(config)

    reporter = Report()

    while True:
        try:
            type, csv_row = next(csv_reader_generator)

            if type != "__header__":
                errors_detected: LineError = BaseValidator.validate(
                    data=csv_row, config=configurate
                )

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
