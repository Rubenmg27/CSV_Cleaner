import pandas as pd
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Union, Tuple
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
    stats: Dict[str, int]


# -------------------
# NullCleaner
# -------------------
class NullCleaner:
    """
    Cleans null values in a DataFrame.

    Attributes:
        strategy: "drop" to remove rows, "impute" to fill them.
        string_strategy: How to fill string nulls: "unknown" or "mode".
    """

    def __init__(self, strategy: str = "impute", impute_strategy: str = "unknown") -> None:
        if strategy not in ("drop", "impute"):
            raise ValueError(f"Invalid strategy '{strategy}'. Must be 'drop' or 'impute'.")
        
        # Validar string_strategy
        if impute_strategy not in ("unknown", "mode"):
            raise ValueError(f"Invalid string_strategy '{impute_strategy}'. Must be 'unknown' or 'mode'.")
        self.strategy = strategy
        self.imput_strategy = impute_strategy

    def clean(self, df: pd.DataFrame, issues: Dict[int, List[Tuple[str, str]]]) -> Tuple[pd.DataFrame, CorrectionReport]:
        """
        Cleans null values in the DataFrame based on the provided issues.

        Args:
            df: Original DataFrame.
            issues: Dict mapping row indices to list of tuples (column, error_type).

        Returns:
            A tuple with the cleaned DataFrame and a CorrectionReport.
        """
        
        df_clean = df.copy()
        corrections: Dict[int, List[LineCorrection]] = {}
        n_filled = 0
        n_removed = 0

        # Identify rows with nulls
        null_rows = [idx for idx, probs in issues.items() if any(err_type == ErrorTypes.NULL for _, err_type in probs)]

        if self.strategy == "drop":
            df_clean = df_clean.drop(index=null_rows)
            n_removed = len(null_rows)
            for idx in null_rows:
                corrections[idx] = [LineCorrection(column="*", correction_type=CorrectionTypes.REMOVED_NULL)]

        else:  # impute
            for row_idx, probs in issues.items():
                for col, err_type in probs:
                    if err_type != ErrorTypes.NULL or col not in df_clean.columns:
                        continue

                    if pd.api.types.is_numeric_dtype(df_clean[col]):
                        mean_val = df_clean[col].mean()
                        if pd.isna(mean_val):
                            mean_val = 0
                        df_clean.at[row_idx, col] = mean_val
                        corrections.setdefault(row_idx, []).append(
                            LineCorrection(column=col, correction_type=CorrectionTypes.FILLED_NULL_MEAN)
                        )
                    else:
                        if self.imput_strategy == "unknown":
                            df_clean.at[row_idx, col] = "Desconocido"
                            corrections.setdefault(row_idx, []).append(
                                LineCorrection(column=col, correction_type=CorrectionTypes.FILLED_NULL_UNKNOWN)
                            )
                        elif self.imput_strategy == "mode":
                            mode_val = df_clean[col].mode()
                            fill = mode_val.iloc[0] if len(mode_val) > 0 else "Desconocido"
                            df_clean.at[row_idx, col] = fill
                            corrections.setdefault(row_idx, []).append(
                                LineCorrection(column=col, correction_type=CorrectionTypes.FILLED_NULL_MODE)
                            )
                    n_filled += 1

        stats = {"nulos_filled": n_filled, "nulos_removed": n_removed}
        return df_clean.reset_index(drop=True), CorrectionReport(correction=corrections, stats=stats)


# -------------------
# TypeCleaner
# -------------------
class TypeCleaner:
    def __init__(self, type_mapping: dict):
        """
        type_mapping: dict de columna → tipo esperado
        tipo esperado puede ser int, float, str, "datetime"
        """
        self.type_mapping = type_mapping

    def clean(self, df: pd.DataFrame, issues: dict):
        df_clean = df.copy()
        corrections = {}
        n_fixed = 0

        for row_idx, probs in issues.items():
            for col, err_type in probs:
                if err_type != ErrorTypes.TYPE or col not in df_clean.columns:
                    continue

                expected_type = self.type_mapping.get(col)
                value = df_clean.at[row_idx, col]

                try:
                    # INT
                    if expected_type == int:
                        val = pd.to_numeric(value, errors="coerce")
                        if pd.notna(val):
                            val = int(val)
                        df_clean.at[row_idx, col] = val

                    # FLOAT
                    elif expected_type == float:
                        df_clean.at[row_idx, col] = pd.to_numeric(value, errors="coerce")

                    # DATETIME
                    elif expected_type == "datetime":
                        ts = pd.to_datetime(str(value), errors="coerce")
                        if pd.isna(ts):
                            df_clean.at[row_idx, col] = pd.NA
                        else:
                            df_clean.at[row_idx, col] = ts.strftime("%Y-%m-%d")

                    # STRING u otros
                    else:
                        df_clean.at[row_idx, col] = str(value)

                    corrections.setdefault(row_idx, []).append(
                        LineCorrection(column=col, correction_type=CorrectionTypes.FIXED_TYPE)
                    )
                    n_fixed += 1

                except Exception:
                    # Si no se puede convertir, dejar NaN o NaT
                    if expected_type == "datetime":
                        df_clean.at[row_idx, col] = pd.NaT
                    else:
                        df_clean.at[row_idx, col] = np.nan

        stats = {"types_fixed": n_fixed}
        return df_clean, CorrectionReport(correction=corrections, stats=stats)
# DuplicateCleaner
# -------------------
class DuplicateCleaner:
    """
    Cleans duplicate rows in a DataFrame.
    """

    def __init__(self, strategy: str = "keep_first") -> None:
        """
        Args:
            strategy: "drop_all", "keep_first", or "keep_last"
        """
        self.strategy = strategy

    def clean(self, df: pd.DataFrame, issues: Dict[int, List[Tuple[str, str]]]) -> Tuple[pd.DataFrame, CorrectionReport]:
        """
        Removes duplicate rows based on the strategy.

        Args:
            df: Original DataFrame.
            issues: Dict mapping row indices to list of tuples (column, error_type).

        Returns:
            Cleaned DataFrame and CorrectionReport.
        """
        df_clean = df.copy()
        corrections: Dict[int, List[LineCorrection]] = {}
        rows_before = df_clean.shape[0]

        dup_rows = [idx for idx, probs in issues.items() if any(err_type == ErrorTypes.DUPLICATE for _, err_type in probs)]
        dup_rows = list(set(dup_rows))

        if self.strategy == "drop_all":
            df_clean = df_clean.drop(index=dup_rows)
            for idx in dup_rows:
                corrections[idx] = [LineCorrection(column="*", correction_type=CorrectionTypes.REMOVED_DUPLICATE)]
        else:  # keep_first or keep_last
            keep = "first" if self.strategy == "keep_first" else "last"
            df_clean = df_clean.drop_duplicates(keep=keep)
            dropped = set(range(rows_before)) - set(df_clean.index)
            for idx in dropped:
                corrections[idx] = [LineCorrection(column="*", correction_type=CorrectionTypes.REMOVED_DUPLICATE)]

        rows_after = df_clean.shape[0]
        stats = {"duplicates_removed": rows_before - rows_after}

        return df_clean.reset_index(drop=True), CorrectionReport(correction=corrections, stats=stats)


# -------------------
# Orchestrator
# -------------------
class DataCleaner:
    """
    Orchestrates multiple cleaners (Null, Type, Duplicate) on a DataFrame.
    """

    def __init__(self, cleaners: List[Union[NullCleaner, TypeCleaner, DuplicateCleaner]]) -> None:
        """
        Args:
            cleaners: List of cleaner instances to apply sequentially.
        """
        self.cleaners = cleaners

    def clean_all(self, df: pd.DataFrame, issues: Dict[int, List[Tuple[str, str]]]) -> Tuple[pd.DataFrame, CorrectionReport]:
        """
        Applies all cleaners sequentially and aggregates corrections and statistics.

        Args:
            df: Original DataFrame.
            issues: Dict mapping row indices to list of tuples (column, error_type).

        Returns:
            Cleaned DataFrame and aggregated CorrectionReport.
        """
        cleaned = df.copy()
        full_report: Dict[int, List[LineCorrection]] = {}
        total_stats = {"nulos_filled": 0, "nulos_removed": 0, "types_fixed": 0, "duplicates_removed": 0}

        for cleaner in self.cleaners:
            cleaned, report = cleaner.clean(cleaned, issues)
            # Merge corrections
            for row, corr_list in report.correction.items():
                full_report.setdefault(row, []).extend(corr_list)
            # Merge stats
            for k, v in report.stats.items():
                total_stats[k] = total_stats.get(k, 0) + v

        return cleaned, CorrectionReport(correction=full_report, stats=total_stats)
