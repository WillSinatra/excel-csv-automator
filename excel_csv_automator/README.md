<div align="center">

# 📊 Excel & CSV Automator

### Professional Data Automation Toolkit

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-Portfolio-orange)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?logo=pandas)
![OpenPyXL](https://img.shields.io/badge/OpenPyXL-3.1%2B-217346)

> **Stop doing repetitive spreadsheet work manually.**  
> This tool automates your entire CSV/Excel data pipeline — clean, combine, convert, and report
> in a single command.

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧹 **Smart Cleaning** | Remove duplicates, fix nulls, normalize headers automatically |
| 🔗 **File Combiner** | Merge multiple CSV/XLSX files with automatic schema alignment |
| 🔄 **Format Converter** | Convert between CSV, Excel, and JSON in one command |
| 📈 **Excel Reporter** | Generate professional 3-sheet analysis reports with formatting |
| 🎨 **Beautiful CLI** | Color-coded terminal output with clear summaries |
| 📝 **Auto Logging** | Every operation logged to file with timestamp and detail |
| 🛡️ **Safe & Validated** | All inputs validated with helpful error messages |

---

## 📁 Project Structure

```
excel_csv_automator/
├── main.py                  # CLI entry point
├── config.py                # Global configuration
├── requirements.txt
├── demo_commands.txt        # Ready-to-run demo commands
├── sample_data/
│   └── sample_input.csv     # Realistic demo dataset (22 rows)
├── output/                  # Generated files land here
├── logs/
│   └── app.log              # Auto-generated operation log
└── modules/
    ├── cleaner.py           # Data cleaning pipeline
    ├── combiner.py          # Multi-file merger
    ├── converter.py         # Format conversion
    ├── reporter.py          # Excel report generator
    └── logger.py            # Centralized logging
```

---

## ⚙️ Installation

**Requirements:** Python 3.11+

```bash
# 1. Clone the repository
git clone https://github.com/your-username/excel_csv_automator.git
cd excel_csv_automator

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate      # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🚀 CLI Usage

### 🧹 Clean a file

Removes duplicates, strips whitespace, normalizes column names, and flags high-null columns.

```bash
python main.py clean --input sample_data/sample_input.csv
```

**Output:**
```
╔══════════════════════════════════════════════════════╗
║      Excel & CSV Automator  ·  v1.0.0                ║
╚══════════════════════════════════════════════════════╝

  ➜   Loading  →  sample_input.csv
  ➜   Cleaning  22 rows × 8 columns …

  ✅  Saved  →  output/cleaned_sample_input.csv

  📋  Cleaning Summary
     Rows before               22
     Rows after                18
     Duplicates removed         3
     Empty rows dropped         0
     Columns normalized         0

  ⚠   High-null columns:
      • department (27.3%)
```

---

### 🔗 Combine multiple files

```bash
python main.py combine --inputs file1.csv file2.xlsx file3.csv
```

Merges files vertically, adds a `source_file` column, handles different schemas.  
Output: `output/combined_output.csv`

---

### 🔄 Convert format

```bash
# CSV → JSON
python main.py convert --input sample_data/sample_input.csv --format json

# CSV → Excel
python main.py convert --input sample_data/sample_input.csv --format excel

# Excel → CSV
python main.py convert --input output/cleaned_sample_input.xlsx --format csv
```

Supported formats: `csv` · `excel` · `json`

---

### 📈 Generate Excel report

```bash
python main.py report --input sample_data/sample_input.csv
```

Creates `output/report_sample_input.xlsx` with three sheets:

| Sheet | Contents |
|---|---|
| **Data** | Full dataset with styled headers and zebra striping |
| **Summary** | Row/column counts, null rates, descriptive statistics |
| **Null Analysis** | Per-column null breakdown with OK / HIGH NULLS flags |

---

## 📥 Input / Output Examples

### Input CSV (raw)

| id | name | age | department | salary | status |
|---|---|---|---|---|---|
| 1 | `  John Smith  ` | 28 | Engineering | 75000 | Active |
| 11 | `  John Smith  ` | 28 | Engineering | 75000 | Active |  ← duplicate |
| 6 | Emily Chen | 26 | *(empty)* | 55000 | Active |

### Output CSV (cleaned)

| id | name | age | department | salary | status |
|---|---|---|---|---|---|
| 1 | John Smith | 28 | Engineering | 75000 | Active |
| 6 | Emily Chen | 26 | *(empty)* | 55000 | Active |

---

## 🛡️ Error Handling

The tool validates inputs and provides clear feedback:

```bash
# File not found
❌  Input file not found: data/missing.csv

# Unsupported format
❌  Unsupported output format 'pdf'. Choose from: csv, excel, json

# Empty dataset after combining
❌  No valid data found in the provided files.
```

All errors are also written to `logs/app.log` with full stack traces.

---

## 🎬 Demo Workflow

Run the full pipeline from raw data to polished report:

```bash
# Step 1 — Clean raw sample data
python main.py clean --input sample_data/sample_input.csv

# Step 2 — Convert cleaned data to JSON (API-ready format)
python main.py convert --input output/cleaned_sample_input.csv --format json

# Step 3 — Generate a full Excel analysis report
python main.py report --input output/cleaned_sample_input.csv
```

See `demo_commands.txt` for the full command reference.

---

## 📸 Screenshots

> *Add screenshots here after running the demo commands.*

| Clean Command | Excel Report |
|---|---|
| `screenshots/clean_command.png` | `screenshots/report_sheets.png` |

See `screenshots/demo_placeholder.txt` for guidance on what to capture.

---

## 🔮 Future Improvements

- [ ] Interactive TUI mode with `rich` or `textual`
- [ ] Email report delivery via SMTP
- [ ] Scheduled automation via `schedule` or cron
- [ ] Support for Google Sheets API integration
- [ ] Web dashboard with `streamlit`
- [ ] Config file support (`.toml` / `.yaml`)
- [ ] Data profiling with `ydata-profiling`

---

## 📄 License

Copyright © 2025 Santiago Sánchez.  
This project is for portfolio and demonstration purposes.  
See [LICENSE](LICENSE) for full terms.

---

<div align="center">

**Built with Python · pandas · openpyxl · colorama**

*If this project helped you, consider leaving a ⭐ on GitHub!*

</div>
