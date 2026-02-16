from pathlib import Path

import pytest

from csvclean.IO_layer.csv_io_layout import CSVIOlayer


@pytest.mark.parametrize(
    "file_path",
    argvalues=[("no_existe.csv"), ("not_csv.txt")],
    ids=[
        "not_exist",
        "not_csv",
    ],
)
def test_bad_input_paths(tmp_path: Path, file_path: str):
    """
    Docstring for test_input_paths

    :param tmp_path: Description
    :type tmp_path: Path
    :param file_path: Description
    :type file_path: str
    """
    input_path = tmp_path / file_path
    output_path = tmp_path / "output.csv"

    io_layer = CSVIOlayer(str(output_path))

    with pytest.raises(FileNotFoundError):
        list(io_layer.read_csv(str(input_path)))


def test_correct_input_path(tmp_path: Path):
    """
    Docstring for test_correct_input_path

    :param tmp_path: Description
    :type tmp_path: Path
    """
    input_path = tmp_path / "exists.csv"
    output_path = tmp_path / "output.csv"

    lines = [
        "name,age,city",
        "Alice,30,Madrid",
        "Bob,,",
        "Charlie,20,London",
        ",13,Valencia",
        ",,Logroño",
    ]
    input_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    io_layer = CSVIOlayer(str(output_path))

    result = list(io_layer.read_csv(str(input_path)))

    assert len(result) == 6


@pytest.mark.parametrize(
    "file_path",
    argvalues=[("/no_existe/"), ("not_csv.txt")],
    ids=[
        "not_file",
        "not_csv",
    ],
)
def test_bad_output_paths(tmp_path: Path, file_path: str):
    """
    Docstring for test_input_paths

    :param tmp_path: Description
    :type tmp_path: Path
    :param file_path: Description
    :type file_path: str
    """
    output_path = tmp_path / file_path

    with pytest.raises(ValueError):
        CSVIOlayer(str(output_path))


@pytest.mark.parametrize(
    "lines",
    argvalues=[
        (
            [
                "name,age,city",
                "Alice,30,Madrid",
                "Bob,,",
                "Charlie,20,London",
                ",13,Valencia",
                ",,Logroño",
            ]
        ),
        (
            [
                "name;age;city",
                "Alice;30;Madrid",
                "Bob;;",
                "Charlie;20;London",
                ";13;Valencia",
                ";;Logroño",
            ]
        ),
        (
            [
                "name\tage\tcity",
                "Alice\t30\tMadrid",
                "Bob\t\t",
                "Charlie\t20\tLondon",
                "\t13\tValencia",
                "\t\tLogroño",
            ]
        ),
    ],
    ids=["comma_delimitator", "point_comma_delimitator", "space_delimitator"],
)
def test_auto_detect_delimitator(tmp_path: Path, lines: list[str]):
    """
    Docstring for test_input_paths

    :param tmp_path: Description
    :type tmp_path: Path
    :param file_path: Description
    :type file_path: str
    """
    input_path = tmp_path / "delimitator.csv"
    output_path = tmp_path / "output.csv"

    input_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    io_layer = CSVIOlayer(str(output_path))

    result = list(io_layer.read_csv(str(input_path)))

    assert len(result) == 6


def test_bad_delimitator(tmp_path: Path):
    """
    Docstring for test_bad_delimitator

    :param tmp_path: Description
    :type tmp_path: Path
    """
    input_path = tmp_path / "delimitator.csv"
    output_path = tmp_path / "output.csv"

    lines = [
        "name_age_city",
        "Alice_30_Madrid",
        "Bob__",
        "Charlie_20_London",
        "_13_Valencia",
        "__Logroño",
    ]

    input_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    io_layer = CSVIOlayer(str(output_path))

    with pytest.raises(ValueError):
        list(io_layer.read_csv(str(input_path)))


def test_reader(tmp_path: Path):
    """
    Docstring for test_reader

    :param tmp_path: Description
    :type tmp_path: Path
    """
    input_path = tmp_path / "example.csv"
    output_path = tmp_path / "output.csv"
    expected = [
        ("__header__", ["name", "age", "city"]),
        ("__row__", ["Alice", "30", "Madrid"]),
        ("__row__", ["Bob", "", ""]),
    ]

    lines = [
        "name,age,city",
        "Alice,30,Madrid",
        "Bob,,",
    ]

    input_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    io_layer = CSVIOlayer(str(output_path))

    for actual, exp in zip(io_layer.read_csv(str(input_path)), expected, strict=False):
        assert actual == exp


def test_writer(tmp_path: Path):
    """
    Docstring for test_writer

    :param tmp_path: Description
    :type tmp_path: Path
    """
    output_path = tmp_path / "output.csv"
    expected = ["Alice;30;Madrid"]

    io_layer = CSVIOlayer(str(output_path))

    row = ["Alice", "30", "Madrid"]
    io_layer.write(str(output_path), row)

    content = output_path.read_text(encoding="utf-8").splitlines()

    assert content == expected


def test_bad_header(tmp_path: Path):
    """
    Docstring for test_bad_header

    :param tmp_path: Description
    :type tmp_path: Path
    """
    config_path = tmp_path / "config.txt"
    output_path = tmp_path / "output.csv"
    lines = ["headers:{str,ienteront,str}", "validator:{Null Errors, Type Errors}"]

    config_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    io_layer = CSVIOlayer(str(output_path))

    with pytest.raises(ValueError):
        io_layer.parse_config(str(config_path))


def test_good_header(tmp_path: Path):
    """
    Docstring for test_bad_header

    :param tmp_path: Description
    :type tmp_path: Path
    """
    config_path = tmp_path / "config.txt"
    output_path = tmp_path / "output.csv"
    lines = ["headers:{str,int,str}", "validator:{Null Errors, Type Errors}"]
    expected = [str, int, str]

    config_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    io_layer = CSVIOlayer(str(output_path))

    configurate = io_layer.parse_config(str(config_path))

    assert configurate.header_types == expected


@pytest.mark.parametrize(
    "lines, expected",
    argvalues=[
        (["headers:{str,int,str}", "validator:{Null Errors, Type Errors}"], [True, True]),
        (["headers:{str,int,str}", "validator:{X, Type Errors}"], [False, True]),
    ],
    ids=["all_validators", "one_validator"],
)
def test_validator(tmp_path: Path, lines: str, expected: list[bool]):
    """
    Docstring for test_bad_header

    :param tmp_path: Description
    :type tmp_path: Path
    """
    config_path = tmp_path / "config.txt"
    output_path = tmp_path / "output.csv"

    config_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    io_layer = CSVIOlayer(str(output_path))

    configure = io_layer.parse_config(str(config_path))

    assert configure.trate_nullerror == expected[0]
    assert configure.trate_typeerror == expected[1]


def test_empty_validator(tmp_path: Path):
    config_path = tmp_path / "config.txt"
    output_path = tmp_path / "output.csv"

    lines = ["headers:{str,int,str}", "validator:{}"]

    config_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    io_layer = CSVIOlayer(str(output_path))

    with pytest.raises(ValueError):
        io_layer.parse_config(str(config_path))
