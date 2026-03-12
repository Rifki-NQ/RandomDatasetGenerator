# RandomDatasetGenerator

A CLI-based tool for generating random datasets as CSV files, with configurable column types, value ranges, and output paths.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [Running Tests](#running-tests)
- [Known Issues & TODO](#known-issues--todo)

---

## Features

**Generator**
- Generate a fully random dataset — column names, types, and values are all randomized automatically
- Generate a custom random dataset — define column names and data types (int, float, or string) per column, using values from your saved configuration

**Settings**
- View current file paths (config and dataset output)
- Change the output path for generated datasets
- View and update individual random value configuration options
- Bulk-update all random value configuration at once

---

## Project Structure

```
RandomDatasetGenerator/
├── main.py                          # Entry point; menu engine and app bootstrap
├── requirements.txt
├── core/
│   ├── exceptions.py                # Custom exception hierarchy
│   ├── utils.py                     # Helper, DataIO (CSV/YAML handlers), Randomizer
│   ├── generator/
│   │   ├── generator_cli.py         # CLI layer for dataset generation
│   │   ├── generator_logic.py       # Generation logic (dataset building, progress tracking)
│   │   ├── generator_setting_cli.py # CLI layer for settings
│   │   └── generator_setting_logic.py # Logic for reading/writing config
│   └── models/
│       ├── config_models.py         # Dataclasses: IntConfig, FloatConfig, StringConfig
│       └── progress_models.py       # GenerationProgress tracker
├── factories/
│   └── feature_factory.py           # Container (dependency wiring) + FeatureFactory
├── data/
│   ├── config.yaml                  # Persistent configuration file
│   └── *.csv                        # Generated dataset outputs
└── tests/
    ├── test_get_dict_depth_logic.py
    └── test_randomizer.py
```

---

## Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`:
  - `pandas`
  - `numpy`
  - `pyyaml`

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/Rifki-NQ/RandomDatasetGenerator

# 2. Navigate into the project directory
cd RandomDatasetGenerator

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py
```

You will be greeted with an interactive menu:

```
1. Generator
2. Setting
Enter by index (q to quit):
```

**Generating a random dataset**

Select `Generator → Generate random dataset`, then enter the number of columns and rows. The tool will generate a CSV with randomized column names and a mix of int, float, and string values.

**Generating a custom random dataset**

Select `Generator → Generate custom random dataset`. You can review your current configuration and output path before generating. For each column, choose a name (or skip to auto-generate) and a data type: `int`, `float`, or `string`. Type `s` at the type prompt to apply random types to all remaining columns.

**Changing settings**

Select `Setting` to view or update:
- The output filepath for generated datasets (must be inside the `data/` folder and end in `.csv`)
- Any individual random value configuration option (int range, float range, float precision, string length, string case)
- All configuration options at once

---

## Configuration

The app stores its configuration in `data/config.yaml`. The configurable values are:

| Key             | Description                                              |
|-----------------|----------------------------------------------------------|
| `column_length` | Number of columns to generate                            |
| `row_length`    | Number of rows to generate                               |
| `int_min`       | Minimum value for random integers (inclusive)            |
| `int_max`       | Maximum value for random integers (exclusive)            |
| `float_min`     | Minimum value for random floats (inclusive)              |
| `float_max`     | Maximum value for random floats (exclusive)              |
| `float_round`   | Decimal places for floats (1–8)                          |
| `string_length` | Character length of generated strings                    |
| `string_type`   | Case of generated strings: `uppercase`, `lowercase`, or `mixed` |
| `dataset_filepath` | Output path for generated CSV files                   |

---

## Architecture

The project is organized into three distinct layers:

- **CLI layer** (`generator_cli.py`, `generator_setting_cli.py`) — handles all user input and output. Never contains business logic.
- **Logic layer** (`generator_logic.py`, `generator_setting_logic.py`) — handles data processing, config reading/writing, and dataset generation.
- **Data/IO layer** (`utils.py`) — `CSVFileHandler` and `YAMLFileHandler` both extend the abstract `DataIO` class, keeping file-format details isolated. A static factory method (`DataIO.create_dataio`) is used to create the correct handler.

Dependencies are wired together in `factories/feature_factory.py` via a `Container` class, and feature dispatch is handled by `FeatureFactory`, which maps menu entries to class/method names at runtime.

The `Randomizer` class wraps `numpy`'s `np.random.default_rng` and supports an optional seed for reproducible output. Data types for generation are described by dataclasses (`IntConfig`, `FloatConfig`, `StringConfig`).

---

## Running Tests

```bash
pytest tests/
```

The test suite covers:

- `test_randomizer.py` — verifies that the `Randomizer` produces values of the correct type, size, and range; that float rounding is applied correctly; that string length matches configuration; and that seeded generation is fully reproducible across two independent instances.
- `test_get_dict_depth_logic.py` — verifies the recursive dict-depth utility used internally by the app.

---

## Known Issues & TODO

- **Bug in `_prompt_column_name`** — the `skip_custom_name` variable is set but not checked correctly on subsequent iterations, so the skip behaviour may not work as expected.
- Add a central validation layer for all config data before use.
- Replace positional list access in `change_random_config` / `update_random_configs` with dict-based lookup for safer config updates.
- Add `argparse` support for non-interactive usage (e.g., `python main.py --generate --columns 5 --rows 100`).