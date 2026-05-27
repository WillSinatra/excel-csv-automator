"""Excel CSV Automator — CLI entry point.

Run ``python main.py --help`` for usage information.
"""

import argparse
import sys
from pathlib import Path

import pandas as pd
from colorama import Fore, Style, init

import config
from modules.logger import get_logger

init(autoreset=True)

logger = get_logger("main")

_BANNER = (
    f"\n{Fore.CYAN}"
    "╔══════════════════════════════════════════════════════╗\n"
    "║      Excel & CSV Automator  ·  v1.0.0                ║\n"
    "║      Professional Data Automation Toolkit            ║\n"
    "╚══════════════════════════════════════════════════════╝"
    f"{Style.RESET_ALL}\n"
)


# ─── Output helpers ──────────────────────────────────────────────────────────

def _ok(msg: str) -> None:
    print(f"\n{Fore.GREEN}  ✅  {msg}{Style.RESET_ALL}")


def _err(msg: str) -> None:
    print(f"\n{Fore.RED}  ❌  {msg}{Style.RESET_ALL}")


def _info(msg: str) -> None:
    print(f"{Fore.CYAN}  ➜   {msg}{Style.RESET_ALL}")


def _divider() -> None:
    print(f"{Fore.CYAN}  {'─' * 52}{Style.RESET_ALL}")


def _load_dataframe(path: Path) -> pd.DataFrame:
    """Read CSV or XLSX into a DataFrame."""
    ext = path.suffix.lower()
    if ext == ".csv":
        return pd.read_csv(path, encoding=config.ENCODING)
    elif ext in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError(f"Unreadable format '{ext}'. Use .csv or .xlsx.")


# ─── Sub-commands ────────────────────────────────────────────────────────────

def cmd_clean(args: argparse.Namespace) -> None:
    """Clean and normalize a CSV/XLSX file."""
    from modules.cleaner import clean_dataframe

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    _info(f"Loading  →  {input_path.name}")
    df = _load_dataframe(input_path)
    _info(f"Cleaning  {len(df):,} rows × {len(df.columns)} columns …")

    cleaned_df, summary = clean_dataframe(df)

    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = config.OUTPUT_DIR / f"cleaned_{input_path.name}"
    if input_path.suffix.lower() == ".csv":
        cleaned_df.to_csv(output_path, index=False, encoding=config.ENCODING)
    else:
        cleaned_df.to_excel(output_path, index=False, engine="openpyxl")

    _ok(f"Saved  →  {output_path}")
    print()
    print(f"{Fore.YELLOW}  📋  Cleaning Summary{Style.RESET_ALL}")
    print(f"     Rows before          {summary['original_rows']:>6}")
    print(f"     Rows after           {summary['final_rows']:>6}")
    print(f"     Duplicates removed   {summary['duplicates_removed']:>6}")
    print(f"     Empty rows dropped   {summary['empty_rows_removed']:>6}")
    if summary["columns_normalized"]:
        print(f"     Columns normalized   {len(summary['columns_normalized']):>6}")
    if summary["high_null_columns"]:
        print(f"\n  {Fore.YELLOW}⚠   High-null columns:{Style.RESET_ALL}")
        for col in summary["high_null_columns"]:
            print(f"      • {col}")


def cmd_combine(args: argparse.Namespace) -> None:
    """Combine multiple CSV/XLSX files into one."""
    from modules.combiner import combine_files

    file_paths = [Path(p) for p in args.inputs]
    _info(f"Combining {len(file_paths)} file(s) …")

    output_path = config.OUTPUT_DIR / "combined_output.csv"
    result = combine_files(file_paths, output_path)
    _ok(f"Combined file saved  →  {result}")


def cmd_convert(args: argparse.Namespace) -> None:
    """Convert a file to another format."""
    from modules.converter import convert_file

    input_path = Path(args.input)
    _info(f"Converting  {input_path.name}  →  {args.format.upper()} …")

    result = convert_file(input_path, args.format)
    _ok(f"Converted file saved  →  {result}")


def cmd_report(args: argparse.Namespace) -> None:
    """Generate a professional Excel report."""
    from modules.reporter import generate_report

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    _info(f"Loading  →  {input_path.name}")
    df = _load_dataframe(input_path)
    _info(f"Generating report for  {len(df):,} rows × {len(df.columns)} columns …")

    output_path = config.OUTPUT_DIR / f"report_{input_path.stem}.xlsx"
    result = generate_report(df, output_path)
    _ok(f"Report saved  →  {result}")
    print(f"\n  Open {Fore.CYAN}{result}{Style.RESET_ALL} in Excel to explore the results.")


# ─── CLI setup ───────────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="excel_csv_automator",
        description="Professional Excel & CSV Automation Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python main.py clean   --input sample_data/sample_input.csv\n"
            "  python main.py combine --inputs file1.csv file2.xlsx\n"
            "  python main.py convert --input sample_data/sample_input.csv --format json\n"
            "  python main.py report  --input sample_data/sample_input.csv\n"
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True, title="commands")

    # clean
    p_clean = sub.add_parser("clean", help="Remove duplicates, fix nulls, normalize columns")
    p_clean.add_argument("--input", required=True, metavar="FILE",
                         help="Path to input .csv or .xlsx file")

    # combine
    p_combine = sub.add_parser("combine", help="Merge multiple CSV/XLSX files into one")
    p_combine.add_argument("--inputs", nargs="+", required=True, metavar="FILE",
                           help="Paths to two or more input files")

    # convert
    p_convert = sub.add_parser("convert", help="Convert a file to csv / excel / json")
    p_convert.add_argument("--input", required=True, metavar="FILE",
                           help="Path to input file")
    p_convert.add_argument("--format", required=True, choices=["csv", "excel", "json"],
                           metavar="FORMAT", help="Target format: csv | excel | json")

    # report
    p_report = sub.add_parser("report", help="Generate a professional multi-sheet Excel report")
    p_report.add_argument("--input", required=True, metavar="FILE",
                          help="Path to input .csv or .xlsx file")

    return parser


def main() -> None:
    """CLI entry point."""
    print(_BANNER)
    parser = _build_parser()
    args = parser.parse_args()

    dispatch = {
        "clean":   cmd_clean,
        "combine": cmd_combine,
        "convert": cmd_convert,
        "report":  cmd_report,
    }

    try:
        dispatch[args.command](args)
    except FileNotFoundError as exc:
        _err(str(exc))
        logger.error(str(exc))
        sys.exit(1)
    except ValueError as exc:
        _err(str(exc))
        logger.error(str(exc))
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}  Interrupted by user.{Style.RESET_ALL}\n")
        sys.exit(0)
    except Exception as exc:
        _err(f"Unexpected error: {exc}")
        logger.exception("Unexpected error")
        sys.exit(1)

    _divider()
    print(f"{Fore.GREEN}  ✨  Operation completed successfully!{Style.RESET_ALL}")
    _divider()
    print()


if __name__ == "__main__":
    main()
