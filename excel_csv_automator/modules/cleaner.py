"""Data cleaning utilities for CSV and Excel DataFrames.

Provides ``clean_dataframe`` which applies a standard cleaning pipeline
and returns a summary of all changes performed.
"""

from typing import Any

import pandas as pd

from modules.logger import get_logger

logger = get_logger(__name__)


def clean_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Clean a DataFrame and return it alongside a change summary.

    Cleaning steps:
    - Remove duplicate rows.
    - Remove fully-empty rows.
    - Strip leading/trailing whitespace from string columns.
    - Normalize column names (lowercase, underscores).
    - Detect columns with more than ``MAX_NULL_THRESHOLD`` null rate.

    Args:
        df: Raw input DataFrame.

    Returns:
        A tuple of (cleaned_df, summary_dict).
    """
    import config  # noqa: PLC0415

    summary: dict[str, Any] = {
        "original_rows": len(df),
        "original_columns": len(df.columns),
        "duplicates_removed": 0,
        "empty_rows_removed": 0,
        "columns_normalized": [],
        "high_null_columns": [],
    }

    # 1. Eliminar duplicados exactos
    before = len(df)
    df = df.drop_duplicates()
    summary["duplicates_removed"] = before - len(df)
    logger.debug(f"Duplicates removed: {summary['duplicates_removed']}")

    # 2. Eliminar filas completamente vacías
    before = len(df)
    df = df.dropna(how="all")
    summary["empty_rows_removed"] = before - len(df)
    logger.debug(f"Empty rows removed: {summary['empty_rows_removed']}")

    # 3. Normalizar nombres de columnas
    original_cols = list(df.columns)
    df.columns = pd.Index(
        [str(col).strip().lower().replace(" ", "_") for col in df.columns]
    )
    summary["columns_normalized"] = [
        f"{old} → {new}"
        for old, new in zip(original_cols, df.columns)
        if str(old) != str(new)
    ]

    # 4. Limpiar espacios en columnas de texto
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].str.strip()

    # 5. Detectar columnas con alto porcentaje de nulos
    null_pct = df.isnull().mean()
    summary["high_null_columns"] = [
        f"{col} ({pct:.1%})"
        for col, pct in null_pct.items()
        if pct > config.MAX_NULL_THRESHOLD
    ]

    summary["final_rows"] = len(df)
    summary["final_columns"] = len(df.columns)

    logger.info(
        f"Cleaning complete — "
        f"{summary['duplicates_removed']} duplicates removed, "
        f"{summary['empty_rows_removed']} empty rows dropped."
    )
    return df, summary
