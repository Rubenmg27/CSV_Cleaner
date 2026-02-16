from dataclasses import dataclass


@dataclass()
class Configuration:
    header_types: list[type]

    trate_nullerror: bool = True
    trate_typeerror: bool = True
