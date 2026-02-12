from enum import Enum


class ErrorTypes(Enum):
    NULL = 1

class CorrectionTypes(Enum):
    REMOVED_NULL = 1



class LineError(Enum):
    column: int
    type_error: ErrorTypes


class ValidationError:
    error: dict[int, list[LineError]]



class LineCorrection:
    column: int
    correction_type: CorrectionTypes


class CorrectionError:
    correction: dict[int, list[LineCorrection]]


