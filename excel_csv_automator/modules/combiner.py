"""File combining utilities.

Merges multiple CSV and XLSX files vertically into a single output file,
adding a ``source_file`` column to track provenance.
"""

from pathlib import Path

import pandas as pd

import config
from modules.logger import get_logger

logger = get_logger(__name__)

_SUPPORTED_EXTENSIONS: frozenset[str] = frozenset({".csv", ".xlsx", ".xls"})


def combine_files(
    file_paths: list[str | Path],
    output_path: Path | None = None,
) -> Path:
    """Combine multiple CSV/XLSX files into one merged CSV.

    Args:
        file_paths: Paths to input files (.csv or .xlsx).
        output_path: Destination path for the merged file.  Defaults to
            ``OUTPUT_DIR/combined_output.csv``.

    Returns:
        Path to the saved combined file.

    Raises:
        FileNotFoundError: If any input file does not exist.
        ValueError: If a file format is unsupported or all files are empty.
    """
    if output_path is None:
        output_path = config.OUTPUT_DIR / "combined_output.csv"

    dataframes: list[pd.DataFrame] = []

    for raw_path in file_paths:
        path = Path(raw_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        ext = path.suffix.lower()
        if ext not in _SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported format '{ext}'. Supported: "
                + ", ".join(sorted(_SUPPORTED_EXTENSIONS))
            )

        # Cargar según extensión
        if ext == ".csv":
            df = pd.read_csv(path, encoding=config.ENCODING)
        else:
            df = pd.read_excel(path)

        if df.empty:
            logger.warning(f"Skipping empty file: {path.name}")
            continue

        df["source_file"] = path.name
        dataframes.append(df)
        logger.info(f"Loaded {path.name} — {len(df):,} rows")

    if not dataframes:
        raise ValueError("No valid data found in the provided files.")

    combined = pd.concat(dataframes, ignore_index=True, join="outer")

    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    combined.to_csv(output_path, index=False, encoding=config.ENCODING)

    logger.info(
        f"Combined {len(dataframes)} file(s) → {output_path.name} "
        f"({len(combined):,} total rows)"
    )
    return output_path
