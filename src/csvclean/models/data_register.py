from _typeshed import Self
from enum import Enum
from dataclasses import dataclass


class ErrorTypes(Enum):
    #Tipe errors
    NULL = 1

    #Corrections
    REMOVED_NULL = 50


@dataclass()
class LineError:
    column: int
    type_error: ErrorTypes
@dataclass()
class DataError:
    error: dict[int, list[LineError]]

