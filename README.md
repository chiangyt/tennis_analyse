# Tennis Match Analysis

## Team Members

| Name | Email | Stevens ID |
|------|-------|------------|
| Yuting Jiang | yjiang69@stevens.edu | 20030015 |
| Nazhi Guo | nguo2@stevens.edu | 20036725 |

## Project Overview

**Tennis Match Analysis** is a Python data analysis project that investigates the relationship between serve quality and match outcomes in the 2024 WTA season. Using match records from `wta_matches_2024.csv`, the project cleans raw data, computes per-match serve performance metrics for winners and losers, compares them statistically, and visualizes the findings. An interactive command-line filter allows users to query specific matches by player, surface, round, and tournament level.

## Main Features

- Load and clean WTA match data from CSV files, with validation for missing columns and file errors.
- Preview match-level serve statistics with a configurable row limit.
- Calculate serve performance metrics for winners and losers:
  - First-serve-in percentage
  - First-serve-points-won percentage
  - Second-serve-points-won percentage
  - Overall serve-points-won percentage
  - Ace rate and double-fault rate
- Compare winner-minus-loser serve differences per match and compute winner advantage rates.
- Visualize serve metric distributions (KDE) and advantage rates across all matches.
- Filter matches interactively by player keyword search, surface, round, tournament level, and result limit.
- Generate exploratory visualizations saved to the `visualization/` folder.
- Validate core behavior with pytest tests.

## Dependencies

```
pandas
numpy
matplotlib
seaborn
pytest
```

Install all dependencies with:

```bash
pip install -r requirements.txt
```

## Project Structure

```text
project/
├── README.md
├── requirements.txt
├── wta_matches_2024.csv
├── tennis_match_analyse.ipynb
├── match_dataset.py
├── serve_analyzer.py
├── paired_analyzer.py
├── interactive_filter.py
├── Visualizations.py
├── visualization/
│   ├── figure_1.png  –  figure_6.png
└── tests/
    └── test_interactive_filter.py
```

## File and Module Description

### `match_dataset.py`

Defines the `MatchDataset` base class. Loads a CSV file, removes duplicate rows, validates and selects requested columns, and drops fully-null rows. Provides `preview_matches(limit)` for a formatted text summary and `options(column)` for sorted unique values of any column. Raises `FileNotFoundError` for missing files and `KeyError` for missing columns.

### `serve_analyzer.py`

Defines `ServeAnalyzer`, which extends `MatchDataset`. Computes six serve-performance metrics (first-in %, first-won %, second-won %, serve-win %, ace rate, df rate) for both winners and losers. Provides `compute_group_state()` for grouped mean/median summary and `plot_distributions()` for KDE comparison plots.

### `paired_analyzer.py`

Defines `PairedMatchAnalyzer`, which extends `MatchDataset`. Calculates per-match winner-minus-loser serve differences and summarises the mean difference and winner advantage rate for each metric. Provides `plot_advantage()` for a grouped bar chart and advantage rate visualization.

### `interactive_filter.py`

Interactive command-line tool for filtering matches. Users search for players by keyword (results shown as a numbered list using set union across winner and loser names), then filter by surface, round, and tournament level. Skipping any step returns all matches for that criterion. Run directly with `python interactive_filter.py`.

### `Visualizations.py`

Runs exploratory data analysis and generates six figures covering match distribution, duration, serve performance comparisons, player win rates, upset patterns, and statistical outliers. Saves all figures to `visualization/`.

### `tennis_match_analyse.ipynb`

Main Jupyter notebook presenting the full analysis workflow: dataset overview, serve performance analysis, paired match comparison with visualizations, and an interactive match filter.

### `tests/test_interactive_filter.py`

Six pytest test cases covering dataset loading and deduplication, missing-column error handling, filter behaviour with absent columns, interactive prompt input validation, and serve metric division-by-zero edge cases.

## How to Run the Program

### 1. Clone the Repository

```bash
git clone <repository-url>
cd project
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Jupyter Notebook

Open `tennis_match_analyse.ipynb` in Jupyter and run all cells top to bottom. This is the main entry point — it covers the full analysis workflow, including serve performance analysis, paired match comparison, supporting visualizations, and an interactive match filter.

### 5. Run Standalone Scripts (Optional)

The following scripts can also be run independently:

```bash
# Interactive match filter (CLI)
python interactive_filter.py

# Exploratory visualization script — saves figures to visualization/
python Visualizations.py

# Use analyzer classes directly
python -c "
from serve_analyzer import ServeAnalyzer
from paired_analyzer import PairedMatchAnalyzer
serve = ServeAnalyzer('wta_matches_2024.csv')
print(serve.compute_group_state())
paired = PairedMatchAnalyzer('wta_matches_2024.csv')
print(paired.summary())
"
```

### 6. Run Tests

```bash
pytest
```

## Dataset

The project expects `wta_matches_2024.csv` in the project root. The file contains 2024 WTA match records including player names, surface, round, tournament information, score, ranking, match duration, and serve statistics for winners and losers.

## Testing

The test suite covers:

- Duplicate and all-null row removal during dataset loading
- `KeyError` raised when requested columns are missing from the dataset
- Filter behaviour when optional columns are absent from the DataFrame
- Interactive prompt retries on invalid input
- Serve metric NaN propagation on division-by-zero edge cases

```bash
pytest tests/ -v
```

## Main Contributions

**Yuting Jiang:** Designed and implemented the core class hierarchy (`MatchDataset`, `ServeAnalyzer`, `PairedMatchAnalyzer`),  and the Jupyter notebook structure. Responsible for serve metric calculations, paired comparison analysis, visualization methods in the analyzer classes, and overall project architecture.

**Nazhi Guo:** Responsible for the exploratory visualization script (`Visualizations.py`), pytest setup and test cases(`test_interactive_filter.py`), exception handling design, and integration testing of the interactive filter(`interactive_filter.py`).
