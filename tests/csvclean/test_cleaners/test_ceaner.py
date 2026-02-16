# --- Fixtures: Reusable setups for tests ---
from dataclasses import dataclass

import pytest

# Importamos desde el nombre del paquete definido en el __init__.py de src/csvclean
from csvclean.cleaners import (
    LineOrchestrator,
    NullCleaner,
    TypeCleaner,
)
from csvclean.models import ErrorTypes


@dataclass
class MockConfig:
    trate_nullerror: bool = True
    trate_typeerror: bool = True

@pytest.fixture
def base_config():
    """Returns a configuration OBJECT instead of a dict."""
    return MockConfig(trate_nullerror=True, trate_typeerror=True)
@pytest.fixture
def orchestrator(base_config):
    """Returns an instance of LineOrchestrator."""
    return LineOrchestrator(base_config)

# --- Unit Tests for individual Cleaners ---

def test_null_cleaner_removes_row():
    """Check if NullCleaner returns an empty list when a NULL error is present."""
    cleaner = NullCleaner()
    row = ["data", ""]
    errors = {1: ErrorTypes.NULL} 
    result_row, _ = cleaner.clean(row, errors)
    assert result_row == []

def test_multiple_null_errors_removal():
    """Ensure a row with multiple null errors is handled correctly by NullCleaner."""
    cleaner = NullCleaner()
    row = ["", "", "2024"]
    errors = {0: ErrorTypes.NULL, 1: ErrorTypes.NULL} 
    result_row, _ = cleaner.clean(row, errors)
    assert result_row == []


def test_null_cleaner_ignores_type_errors():
    """Ensure NullCleaner doesn't accidentally remove a row with only TYPE errors."""
    cleaner = NullCleaner()
    row = ["1", "invalid"]
    errors = {1: ErrorTypes.TYPE}
    
    result_row, _ = cleaner.clean(row, errors)
    assert result_row == row  # Row should be kept

def test_type_cleaner_removes_row():
    """Check if TypeCleaner returns an empty list when a TYPE error is present."""
    cleaner = TypeCleaner()
    row = ["1", "not_a_number"]
    errors = {1: ErrorTypes.TYPE}
    
    result_row, _ = cleaner.clean(row, errors)
    assert result_row == []

def test_type_cleaner_ignores_null_errors():
    """Ensure TypeCleaner doesn't remove a row with only NULL errors."""
    cleaner = TypeCleaner()
    row = ["", "valid"]
    errors = {0: ErrorTypes.NULL}
    
    result_row, _ = cleaner.clean(row, errors)
    assert result_row == row  # Row should be kept

# --- Integration Tests for LineOrchestrator ---
def test_orchestrator_handles_already_empty_row(orchestrator):
    """Ensure the orchestrator gracefully handles receiving an already empty row."""
    row = []
    errors = {1: ErrorTypes.NULL}
    
    # Should not raise an exception and should return empty row
    result_row, _ = orchestrator.process(row, errors)
    assert result_row == []


def test_orchestrator_valid_row(orchestrator):
    """Ensure a row with no errors passes through safely."""
    row = ["1", "Valid Name", "2024"]
    errors = {}
    
    clean_row, _ = orchestrator.process(row, errors)
    assert clean_row == row

def test_orchestrator_stops_at_first_error(orchestrator):
    """Ensure that if an error is found, the row is emptied immediately."""
    row = ["", "invalid_type"]
    # Column 0 is null, Column 1 has type error
    errors = {0: ErrorTypes.NULL, 1: ErrorTypes.TYPE}
    
    clean_row, _ = orchestrator.process(row, errors)
    assert clean_row == []

def test_orchestrator_ignores_disabled_cleaner():
    """Verify that if a cleaner is set to False in config, the row is kept."""
    config = {"use_null": False, "use_type": True}
    orchestrator = LineOrchestrator(config)
    
    row = ["1", ""]
    errors = {1: ErrorTypes.NULL} # Error exists but cleaner is OFF
    
    clean_row, _ = orchestrator.process(row, errors)
    assert clean_row == row


def test_orchestrator_returns_original_errors(orchestrator):
    """Verify the errors dictionary is returned exactly as it was received."""
    row = ["1", "Valid"]
    errors = {0: ErrorTypes.TYPE}
    
    _, returned_errors = orchestrator.process(row, errors)
    assert returned_errors == errors
    assert id(returned_errors) == id(errors) # Should be the same object or identical