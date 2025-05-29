# healthyDB

## Important
The first column is the one that is processed

## Purpose and Scope

This document provides a high-level introduction to the **healthyDB** system, explaining its purpose as an Excel data cleaning and sanitization tool. It covers the system's architecture, core components, and processing modes to help users understand how healthyDB transforms messy Excel data into clean, standardized datasets.

- For detailed installation instructions, see **Installation**.
- For step-by-step usage examples, see **Basic Usage**.
- For technical implementation details, see **System Reference**.

## What is healthyDB?

**healthyDB** is a Python-based command-line tool designed to clean and sanitize Excel files by removing unwanted data, duplicates, and optionally filtering content based on configurable word blacklists. The system provides two cleaning profiles:

| Cleaning Mode | Operations Performed | Use Case |
|---------------|----------------------|----------|
| Basic         | Remove empty rows/columns, duplicates, strip whitespace | General data cleanup |
| Hard          | Basic operations + content filtering using word blacklist + text normalization | Content sanitization with specific filtering requirements |

The system processes Excel files and outputs cleaned versions with a standardized naming convention in a dedicated results directory.

## System Architecture

The following diagram shows the core system components and their relationships using actual code entities:

### Dependencies
- `pandas`
- `openpyxl`
- `numpy`

### Configuration & Data
- `palabras_a_eliminar.csv`
- `./result/` directory
- Output: `healthy_*.xlsx` files

### Core Processing Engine
- `main.py`
  - `sys.argv[1]` (file_path)
  - `sys.argv[2]` (profile)
- `cure.py`
  - `import_excel_file()`
  - `clean_excel_file()`
  - `hard_clean_excel_file()`
  - `save_excel_file()`
  - `eliminar_tildes()`
  - `load_words_to_remove()`

## Processing Pipeline

This diagram illustrates the data flow through the system using actual function names and file operations:

```text
Input Excel File
    ↓
cure.import_excel_file(file)
    ↓
pd.read_excel(file)
    ↓
pandas DataFrame
    ↓
profile == 'hard'?
    ↙                   ↘
Yes                    No
    ↓                     ↓
cure.hard_clean_excel_file(df)   cure.clean_excel_file(df)
    ↓                     ↓
- dropna(axis=1, how='all')  
- dropna(axis=0, how='all')  
- drop_duplicates()  
- str.strip()  

    ↓
Additional for Hard Mode:
- df['col_sin_tilde'] = eliminar_tildes(df[col])
- load_words_to_remove('palabras_a_eliminar.csv')
- df[~df['col_sin_tilde'].str.contains(patron, case=False)]
- df.drop(columns=['col_sin_tilde'])

    ↓
cure.save_excel_file(processed, file_path)
    ↓
./result/healthy_*.xlsx
```

## Core Components

### Entry Point and Orchestration

The `main.py` file serves as the system's entry point, handling command-line argument parsing and orchestrating the cleaning process:

- **Command-line interface**: Accepts file path and optional cleaning profile
- **Profile selection**: Routes to appropriate cleaning function based on `sys.argv[2]`
- **Error handling**: Manages `FileNotFoundError` and general exceptions
- **Timing**: Measures and reports processing duration

### Data Processing Engine

The `cure.py` module contains the core data processing functions:

| Function                | Purpose                                  | Input               | Output              |
|-------------------------|------------------------------------------|---------------------|---------------------|
| `import_excel_file()`   | Load Excel file into DataFrame           | File path           | `pd.DataFrame`      |
| `clean_excel_file()`    | Basic data cleaning operations           | `pd.DataFrame`      | Cleaned `pd.DataFrame` |
| `hard_clean_excel_file()` | Advanced cleaning with content filtering | `pd.DataFrame`      | Filtered `pd.DataFrame` |
| `save_excel_file()`     | Export cleaned data to result directory  | `pd.DataFrame`, file path | Status message  |
| `eliminar_tildes()`     | Remove accents from text                 | String              | Normalized string   |
| `load_words_to_remove()`| Load word blacklist from CSV             | File path           | `NumPy` array       |

## Configuration Management

The system uses `palabras_a_eliminar.csv` as a configuration file containing words to filter out during hard cleaning mode. This file is loaded by `load_words_to_remove()` and converted to a regex pattern for efficient text matching.

### Sources
- `cure.py` lines 17–99
- `main.py` lines 6–59

## Output Structure

**healthyDB** follows a consistent output pattern:

- **Output directory**: `./result/` (created automatically if it doesn't exist)
- **File naming**: `healthy_` prefix added to original filename
- **Format preservation**: Maintains Excel format using `openpyxl` backend
- **Index handling**: Saves without DataFrame index (`index=False`)

## Quick Start Example

```bash
# Basic cleaning mode
python main.py data.xlsx

# Hard cleaning mode with content filtering
python main.py data.xlsx hard
```

The system will process the input file and create `./result/healthy_data.xlsx` with the cleaned data.
```
