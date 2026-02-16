import csv
from collections.abc import Generator, Iterable
from pathlib import Path
from xmlrpc.client import boolean

from ..models.config import Configuration
from ..models.data_register import TYPE_MAP


class CSVIOlayer:
    """Class to read inputs from CSV and file text and write the clean CSV."""

    def __init__(self, output_path: str):
        """
        Check the output file is valid and prepare it for writing.

        :param output_path: Path to check if is valid
        :type output_path: str
        """
        path: Path = Path(output_path)
        if output_path.lower().endswith(".csv"):
            path.open("w", encoding="utf-8").close()
        else:
            raise ValueError("The output path is incorrect.")

    def _validate_input_path(self, csv_path: str) -> bool:
        """
        Validate if the file is a csv and exists

        :param csv_path: Path of csv file
        :type csv_path: str
        :return: Retrurn True if csv file exists or return false if csv file doesnt exists
        :rtype: bool
        """
        path: Path = Path(csv_path)

        return not path.exists() or Path(csv_path).suffix.lower() == ".csv"

    def _detect_delimiter(self, csv_path: str) -> tuple[str, boolean]:
        """
        Detect the delimeter of csv file and check if is valid.

        :param csv_path: Path of csv file
        :type csv_path: str
        :return: tuple that contains the delimeter and check if is a valid delimeter
        :rtype: tuple[str, bool]
        """
        path: Path = Path(csv_path)
        with path.open() as f:
            line = f.readline()
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(line)
            delimiter = dialect.delimiter
            return delimiter, delimiter in [",", ";", "\t"]

    def _parse_headers(self, line: str) -> list[type]:
        """
        Parse the config text and extract the type of columns.

        :param line: the config text
        :type line: str
        :return: list of types of each column of csv
        :rtype: list[type]
        """
        header_types: list = []
        stripped_line: str = line.strip()

        if stripped_line.startswith("headers:"):
            type_str: str = stripped_line.split("headers:")[1].strip()

            stripped_type_str: str = type_str.strip("{}")

            if not stripped_type_str:
                return header_types

            for type in stripped_type_str.split(","):
                stripped_type: str = type.strip()

                if stripped_type not in TYPE_MAP:
                    raise ValueError(f"Not soported type: {stripped_type}")

                header_types.append(TYPE_MAP[stripped_type])

        return header_types

    def _parse_validators(self, line: str) -> list[str]:
        """
        Parse the config text and extract the validators to aply.

        :param line: the config text
        :type line: str
        :return: list with the names of each validator to be applied.
        :rtype: list[str]
        """
        val_str: str = line.split("validator:")[1].strip()
        stripped_val_str: str = val_str.strip("{}")

        validators: list[str] = []

        for val in stripped_val_str.split(","):
            stripped_val: str = val.strip()

            validators.append(stripped_val)

        return validators

    def parse_config(self, config_path: str) -> Configuration:
        """
        Parse the configuration file text and create the dataclass Configuration.

        :param config_path: path of configuration file
        :type config_path: str
        :return: Configuration class with the user indications.
        :rtype: Configuration
        """
        path: Path = Path(config_path)

        with path.open() as config_file:
            header_line: str = config_file.readline().strip()
            header_types: list[type] = self._parse_headers(header_line)
            validators_line: str = config_file.readline().strip()
            validators: list[str] = self._parse_validators(validators_line)

        return Configuration(
            header_types=header_types,
            trate_nullerror="Null Errors" in validators,
            trate_typeerror="Type Errors" in validators,
        )

    def read_csv(self, csv_path: str) -> Generator:
        """
        Read the csv file line by line.

        :param csv_path: Path to the CSV file
        :type csv_path: str
        :return: if CSV file exist return a Generator
        :rtype: Generator
        """
        path: Path = Path(csv_path)

        if not self._validate_input_path(csv_path):
            raise FileNotFoundError(f"The {csv_path} doesn't exists or isn't a csv file.")

        delimiter, correct_delimiter = self._detect_delimiter(csv_path)

        if not correct_delimiter:
            raise ValueError("Delimiter is incorrect.")

        with path.open() as csv_file:
            reader: Iterable = csv.reader(csv_file, delimiter=delimiter)

            header: list[str] = next(reader)
            yield ("__header__", header)

            yield from (("__row__", fila) for fila in reader)

    def write(self, outputpath: str, csv_row_clean: list[str]):
        """
        Write the clean csv Data Frame into outputpath.

        :param outputpath: Path of clean csv
        :type outputpath: str
        :param csv_row_clean: List with the row of clean csv
        :type csv_row_clean: list[str]
        """
        path: Path = Path(outputpath)

        with path.open(mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(csv_row_clean)
