"""File format conversion utilities.

Converts between CSV, Excel (XLSX), and JSON, preserving the original
filename stem and saving output to ``OUTPUT_DIR``.
"""

from pathlib import Path

import pandas as pd

import config
from modules.logger import get_logger

logger = get_logger(__name__)

SUPPORTED_FORMATS: frozenset[str] = frozenset({"csv", "excel", "json"})
_READABLE_EXTENSIONS: frozenset[str] = frozenset({".csv", ".xlsx", ".xls", ".json"})


def convert_file(input_path: str | Path, output_format: str) -> Path:
    """Convert a file to the specified format.

    Args:
        input_path: Path to the source file.
        output_format: Target format — ``"csv"``, ``"excel"``, or ``"json"``.

    Returns:
        Path to the converted output file.

    Raises:
        FileNotFoundError: If ``input_path`` does not exist.
        ValueError: If ``output_format`` is unsupported or the file cannot be read.
    """
    input_path = Path(input_path)
    output_format = output_format.lower().strip()

    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    if output_format not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported output format '{output_format}'. "
            f"Choose from: {', '.join(sorted(SUPPORTED_FORMATS))}"
        )

    ext = input_path.suffix.lower()
    if ext not in _READABLE_EXTENSIONS:
        raise ValueError(f"Cannot read format '{ext}'.")

    # Leer archivo de entrada
    if ext == ".csv":
        df = pd.read_csv(input_path, encoding=config.ENCODING)
    elif ext in {".xlsx", ".xls"}:
        df = pd.read_excel(input_path)
    else:
        df = pd.read_json(input_path)

    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stem = input_path.stem

    # Escribir en el formato destino
    if output_format == "csv":
        output_path = config.OUTPUT_DIR / f"{stem}.csv"
        df.to_csv(output_path, index=False, encoding=config.ENCODING)

    elif output_format == "excel":
        output_path = config.OUTPUT_DIR / f"{stem}.xlsx"
        df.to_excel(output_path, index=False, engine="openpyxl")

    else:  # json
        output_path = config.OUTPUT_DIR / f"{stem}.json"
        df.to_json(output_path, orient="records", indent=2, force_ascii=False)

    logger.info(f"Converted: {input_path.name} → {output_path.name}")
    return output_path
