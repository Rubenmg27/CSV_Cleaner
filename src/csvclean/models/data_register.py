from enum import Enum
from typing import TypeAlias


class ErrorTypes(Enum):
    # Tipe errors
    NULL = 1
    TYPE = 2
    DUPLICATE = 3

    # Corrections
    REMOVED_NULL = 50
    FIXED_TYPE = 51


LineError: TypeAlias = dict[int, ErrorTypes]

TYPE_MAP = {"str": str, "int": int, "float": float, "bool": bool}
