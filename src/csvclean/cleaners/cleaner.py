from dataclasses import dataclass
from typing import Dict, List, Tuple, TypeAlias

from csvclean.cleaners.null_cleanerold import ErrorTypes

# Type alias for a dictionary where key is column index and value is the error type
LineError: TypeAlias = dict[int, ErrorTypes]

@dataclass
class CleanResult:
    """
    Represents the result of a row cleaning operation.
    
    Attributes:
        row (List[str]): The processed row. Empty if the row was discarded.
        correction (LineError): The dictionary of errors associated with the row.
    """
    row: List[str]  
    correction: LineError


class NullCleaner:
    """Cleaner specialized in handling null value errors."""

    def clean(self, row: List[str], errors: LineError) -> Tuple[List[str], LineError]:
        """
        Validates if the row contains any NULL type errors.

        Args:
            row (List[str]): The input data row as a list of strings.
            errors (LineError): Dictionary mapping column indices to ErrorTypes.

        Returns:
            Tuple[List[str], LineError]: An empty list and the errors if a NULL 
                is found; otherwise, the original row and errors.
        """
        if ErrorTypes.NULL in errors.values():
            return [], errors
        return row, errors

class TypeCleaner:
    """Cleaner specialized in handling data type mismatch errors."""

    def clean(self, row: List[str], errors: LineError) -> Tuple[List[str], LineError]:
        """
        Validates if the row contains any TYPE mismatch errors.

        Args:
            row (List[str]): The input data row as a list of strings.
            errors (LineError): Dictionary mapping column indices to ErrorTypes.

        Returns:
            Tuple[List[str], LineError]: An empty list and the errors if a TYPE 
                error is found; otherwise, the original row and errors.
        """
        if any(err == ErrorTypes.TYPE for err in errors.values()):
            return [], errors
        return row, errors
    
class DuplicateCleaner:
    """Cleaner specialized in handling duplicate record errors."""

    def clean(self, row: List[str], errors: LineError) -> Tuple[List[str], LineError]:
        """
        Validates if the row is marked as a DUPLICATE.

        Args:
            row (List[str]): The input data row as a list of strings.
            errors (LineError): Dictionary mapping column indices to ErrorTypes.

        Returns:
            Tuple[List[str], LineError]: An empty list and the errors if a DUPLICATE 
                error is found; otherwise, the original row and errors.
        """
        if any(e == ErrorTypes.DUPLICATE for e in errors.values()):
            return [], errors
        return row, errors
    
class LineOrchestrator:
    """
    Orchestrates the cleaning process by executing multiple cleaners 
    based on a provided configuration.
    """

    def __init__(self, config: Dict[str, bool]):
        """
        Initializes the orchestrator with specific cleaning toggles.

        Args:
            config (Dict[str, bool]): Configuration dictionary (e.g., 
                {"use_null": True, "use_type": True, "use_duplicate": True}).
        """
        self.config = config
        self.null_cleaner = NullCleaner()
        self.type_cleaner = TypeCleaner()
        self.duplicate_cleaner = DuplicateCleaner()

    def process(self, row: List[str], errors: LineError) -> Tuple[List[str], LineError]:
        """
        Sequentially runs the enabled cleaners on a single row.
        
        If a cleaner invalidates a row (returns an empty list), subsequent 
        cleaning steps are skipped for that row.

        Args:
            row (List[str]): The raw data row.
            errors (LineError): The pre-detected errors for this specific row.

        Returns:
            Tuple[List[str], LineError]: The final state of the row (original or empty) 
                and the associated error map.
        """
        current_row = list(row)

        # 1. Null Cleaning
        if self.config.get("use_null", False):
            current_row, _ = self.null_cleaner.clean(current_row, errors)

        # 2. Type Cleaning (only if row is still valid)
        if current_row and self.config.get("use_type", False):
            current_row, _ = self.type_cleaner.clean(current_row, errors)

        # 3. Duplicate Cleaning (only if row is still valid)
        if current_row and self.config.get("use_duplicate", False):
            current_row, _ = self.duplicate_cleaner.clean(current_row, errors)

        return current_row, errors