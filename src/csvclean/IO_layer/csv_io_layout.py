import csv
from collections.abc import Generator
from pathlib import Path

from ..models.config import Configuration
from ..models.data_register import TYPE_MAP


class CSVIOlayer:
    """"""

    def __init__(self, output_path: str):
        path = Path(output_path)
        if path.is_file() and output_path.lower().endswith(".csv"):
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
        path = Path(csv_path)

        return not path.exists() or Path(csv_path).suffix.lower() == ".csv"

    def _detect_delimiter(self, csv_path: str) -> str:
        """
        Detect the delimeter of csv file.

        :param csv_path: Path of csv file
        :type csv_path: str
        :return: the delimeter of csv file
        :rtype: str
        """
        path = Path(csv_path)
        with path.open() as f:
            line = f.readline()
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(line)
            return dialect.delimiter

    def _parse_headers(self, line: str) -> list[type]:
        header_types = []
        stripped_line = line.strip()

        if stripped_line.startswith("headers:"):
            type_str = stripped_line.split("headers:")[1].strip()

            stripped_type_str = type_str.strip("{}")

            for type in stripped_type_str.split(","):
                stripped_type = type.strip()

                if stripped_type not in TYPE_MAP:
                    raise ValueError(f"Not soported type: {stripped_type}")

                header_types.append(TYPE_MAP[stripped_type])

        return header_types

    def _parse_validators(self, line: str) -> list[str]:
        val_str = line.split("validator:")[1].strip()
        stripped_val_str = val_str.strip("{}")

        validators = []

        for val in stripped_val_str.split(","):
            stripped_val = val.strip()

            validators.append(stripped_val)

        return validators

    def parse_config(self, config_path: str) -> Configuration:
        path = Path(config_path)

        with path.open() as config_file:
            header_line = config_file.readline().strip()
            header_types = self._parse_headers(header_line)
            validators_line = config_file.readline().strip()
            validators = self._parse_validators(validators_line)

        return Configuration(
            header_types=header_types,
            trate_nullerror="Null Errors" in validators,
            trate_typeerror="Type Errors" in validators,
        )

    def read_csv(self, csv_path: str) -> Generator:
        """
        Docstring for read

        :param csv_path: Path to the CSV file
        :type csv_path: str
        :return: if CSV file exist return a Generator
        :rtype: Generator
        """
        path = Path(csv_path)

        if not self._validate_input_path(csv_path):
            raise FileNotFoundError(f"The {csv_path} doesn't exists or isn't a csv file.")

        delimiter = self._detect_delimiter(csv_path)

        with path.open() as csv_file:
            reader = csv.reader(csv_file, delimiter=delimiter)

            header = next(reader)
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
        path = Path(outputpath)

        with path.open(mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(csv_row_clean)
