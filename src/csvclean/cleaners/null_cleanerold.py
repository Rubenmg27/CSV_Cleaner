import pandas as pd
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Union, Tuple, Any
import numpy as np

# -------------------
# Enums and Models
# -------------------
class ErrorTypes(Enum):
    NULL = 1
    TYPE = 2
    DUPLICATE = 3


class CorrectionTypes(Enum):
    REMOVED_NULL = 1
    FILLED_NULL_MEAN = 2
    FILLED_NULL_UNKNOWN = 3
    FILLED_NULL_MODE = 4
    FIXED_TYPE = 5
    REMOVED_DUPLICATE = 6

@dataclass
class LineCorrection:
    """
    Represents a correction applied to a specific column in a row.
    """
    column: str
    correction_type: CorrectionTypes


@dataclass
class CorrectionReport:
    """
    Report containing all corrections applied and statistics.
    """
    correction: Dict[int, List[LineCorrection]]


# -------------------
# NullCleaner
# -------------------
class NullCleaner:
    """
    NullCleaner always removes rows with null values.
    """
    def clean(self, df: pd.DataFrame, issues: Dict[int, List[Tuple[str, ErrorTypes]]]):
        df_clean = df.copy()
        corrections: Dict[int, List[LineCorrection]] = {}

        null_rows = [idx for idx, probs in issues.items()
                    if any(err_type == ErrorTypes.NULL for _, err_type in probs)]

        # Filtramos solo los índices que realmente existen en el DF actual
        existing_null_rows = [idx for idx in null_rows if idx in df_clean.index]
        df_clean = df_clean.drop(index=existing_null_rows)

        for idx in existing_null_rows:
            corrections[idx] = [LineCorrection(column="*", correction_type=CorrectionTypes.REMOVED_NULL)]

        # IMPORTANTE: Quitamos el reset_index de aquí
        return df_clean, CorrectionReport(correction=corrections)


# -------------------
# TypeCleaner
# -------------------
class TypeCleaner:
    """
    TypeCleaner converts columns to the expected type according to type_mapping.
    """

    def __init__(self, type_mapping: Dict[str, Any]):
        self.type_mapping = type_mapping

    def clean(self, df: pd.DataFrame, issues: Dict[int, List[Tuple[str, ErrorTypes]]]):
        df_clean = df.copy()
        corrections: Dict[int, List[LineCorrection]] = {}

        for row_idx, probs in issues.items():
            for col, err_type in probs:
                if err_type != ErrorTypes.TYPE or col not in df_clean.columns:
                    continue

                expected_type = self.type_mapping.get(col)
                value = df_clean.at[row_idx, col]

                try:
                    if expected_type is int:
                        val = pd.to_numeric(value, errors="coerce")
                        if pd.notna(val):
                            val = int(val)
                        df_clean.at[row_idx, col] = val
                    elif expected_type == float:
                        df_clean.at[row_idx, col] = pd.to_numeric(value, errors="coerce")
                    elif expected_type == "datetime":
                        ts = pd.to_datetime(str(value), errors="coerce")
                        df_clean.at[row_idx, col] = ts.strftime("%Y-%m-%d") if pd.notna(ts) else pd.NA
                    else:
                        df_clean.at[row_idx, col] = str(value)

                    corrections.setdefault(row_idx, []).append(
                        LineCorrection(column=col, correction_type=CorrectionTypes.FIXED_TYPE)
                    )
                except:
                    df_clean.at[row_idx, col] = pd.NA

        return df_clean, CorrectionReport(correction=corrections)
# DuplicateCleaner
# -------------------
# -------------------
# DuplicateCleaner fijo
# -------------------
class DuplicateCleaner:
    """
    Removes duplicate rows, always keeping the first occurrence.
    """

    def clean(self, df: pd.DataFrame, issues: Dict[int, List[Tuple[str, ErrorTypes]]]) -> Tuple[pd.DataFrame, CorrectionReport]:
        df_clean = df.copy()
        corrections: Dict[int, List[LineCorrection]] = {}

        # Filas duplicadas según los issues
        dup_rows = [idx for idx, probs in issues.items()
                    if any(err_type == ErrorTypes.DUPLICATE for _, err_type in probs)]
        dup_rows = list(set(dup_rows))  # evitar repetidos

        # Drop duplicates, keep first
        df_clean = df_clean.drop_duplicates(keep="first")

        # Registra las filas eliminadas
        dropped = set(dup_rows) - set(df_clean.index)
        for idx in dropped:
            corrections[idx] = [LineCorrection(column="*", correction_type=CorrectionTypes.REMOVED_DUPLICATE)]

        return df_clean, CorrectionReport(correction=corrections) # Sin reset_index
# -------------------
# Orchestrator
# -------------------
class DataCleaner:
    """
    Orchestrates NullCleaner, TypeCleaner, and DuplicateCleaner based on user flags.
    """

    def __init__(self, use_null: bool, use_type: bool, use_duplicate: bool, type_mapping: Dict[str, Any]):
        self.cleaners = []

        if use_null:
            self.cleaners.append(NullCleaner())  # Siempre elimina nulos

        if use_type:
            if not type_mapping:
                raise ValueError("type_mapping must be provided if use_type=True")
            self.cleaners.append(TypeCleaner(type_mapping))

        if use_duplicate:
            self.cleaners.append(DuplicateCleaner())  # Siempre deja la primera

    def clean_all(self, df: pd.DataFrame, issues: dict[int, list[tuple[str, ErrorTypes]]]):
        cleaned = df.copy()
        full_report: Dict[int, List[LineCorrection]] = {}

        for cleaner in self.cleaners:
        # Pasamos el DF con los índices originales intactos
            cleaned, report = cleaner.clean(cleaned, issues)
        
            for row_idx, corr_list in report.correction.items():
             full_report.setdefault(row_idx, []).extend(corr_list)

    # REFRESCAMOS EL ÍNDICE SOLO AL FINAL
        cleaned = cleaned.reset_index(drop=True)
        return cleaned, CorrectionReport(correction=full_report)