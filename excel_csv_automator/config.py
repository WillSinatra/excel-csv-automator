"""Global configuration for Excel CSV Automator."""

from pathlib import Path

# Directorio base del proyecto
BASE_DIR: Path = Path(__file__).parent

INPUT_DIR: Path = BASE_DIR / "sample_data"
OUTPUT_DIR: Path = BASE_DIR / "output"
LOG_DIR: Path = BASE_DIR / "logs"

DATE_FORMAT: str = "%Y-%m-%d"
ENCODING: str = "utf-8"
MAX_NULL_THRESHOLD: float = 0.5
