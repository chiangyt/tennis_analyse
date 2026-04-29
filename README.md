# Tennis Match Analysis


## Team Member:
Yuting Jiang, yjiang69@stevens.edu, Stevens ID:20030015
Nazhi Guo, nguo2@stevens.edu, Stevens ID: 20036725
## Project Overview
**Tennis Match Analysis** is a Python data analysis project for exploring the 2024 WTA match dataset. The project loads raw match records from `wta_matches_2024.csv`, mean function includes: data cleaning,  calculates serve-performance metrics, calculates serve-performance metrics, compares winner and loser, and generates visual, and can output the filter.

The project is designed for both script-based analysis and interactive exploration. It includes reusable analyzer classes, an interactive command-line filter, a visualization script, a Jupyter notebook, and automated tests.

## Main Features

- Load and clean WTA match data from CSV files.
- Preview match-level serve statistics.
- Calculate winner and loser serve metrics, including:
  - First-serve-in percentage
  - First-serve-points-won percentage
  - Second-serve-points-won percentage
  - Overall serve-points-won percentage
  - Serve aggressiveness based on aces and double faults
- Compare winner-minus-loser serve differences for each match.
- Filter matches interactively by player, winner, loser, surface, round, tournament level, and result limit.
- Generate exploratory visualizations and save figures to the `visualization/` folder.
- Validate core behavior with pytest tests.

## Dependencies

This project uses the following Python libraries:

| Library | Purpose |
| --- | --- |
| `pandas` | CSV loading, data cleaning, filtering, and tabular analysis |
| `numpy` | Numeric operations used during analysis |
| `matplotlib` | Plot creation and figure export |
| `seaborn` | Statistical visualizations |
| `ipython` | Rich display support for notebook-style output |
| `pytest` | Automated testing |

All dependencies are listed in [`requirements.txt`](requirements.txt).

## Project Structure

```text
tennis_analyse/
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
│   ├── figure_1.png
│   ├── figure_2.png
│   ├── figure_3.png
│   ├── figure_4.png
│   ├── figure_5.png
│   └── figure_6.png
└── tests/
    └── test_interactive_filter.py
```

## File and Module Description

### `match_dataset.py`

Defines the `MatchDataset` base class. It loads a CSV dataset, removes duplicate rows, drops fully empty rows, optionally keeps selected columns, and provides a text preview of match-level serve statistics.

### `serve_analyzer.py`

Defines `ServeAnalyzer`, which extends `MatchDataset`. It calculates serve-performance metrics for winners and losers, then provides grouped summary statistics such as mean and median values.

### `paired_analyzer.py`

Defines `PairedMatchAnalyzer`, which also extends `MatchDataset`. It calculates per-match differences between winner and loser serve metrics, making it easier to evaluate how serve performance relates to winning.

### `interactive_filter.py`

Provides an interactive command-line tool for filtering matches. Users can search by player name, winner, loser, surface, round, tournament level, and maximum number of displayed results.

### `Visualizations.py`

Runs exploratory data analysis and creates six visualization images. The charts include surface distribution, tournament levels, match duration, serve performance, player win rates, upset rates, ranking gaps, and outlier views.

### `tennis_match_analyse.ipynb`

A Jupyter notebook version of the analysis workflow. It is useful for step-by-step exploration and presentation.

### `tests/test_interactive_filter.py`

Contains pytest tests for dataset loading, match filtering, input validation, and serve metric edge cases.

## How to Run the Program

### 1. Clone or Open the Project

Open a terminal in the project root directory:

```bash
cd tennis_analyse
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Interactive Match Filter

```bash
python interactive_filter.py
```

The program will ask for filter options, then print matching WTA matches in a compact text format.

### 5. Run the Visualization Script

```bash
python Visualizations.py
```

This script reads `wta_matches_2024.csv`, performs exploratory analysis, and saves output charts into the `visualization/` directory.

### 6. Use the Analyzer Classes in Python

Example:

```python
from serve_analyzer import ServeAnalyzer
from paired_analyzer import PairedMatchAnalyzer

serve = ServeAnalyzer("wta_matches_2024.csv")
print(serve.compute_group_state())

paired = PairedMatchAnalyzer("wta_matches_2024.csv")
print(paired.summary())
```

### 7. Run Tests

```bash
pytest
```

## Dataset

The project expects the dataset file to be available at:

```text
wta_matches_2024.csv
```

The CSV should contain WTA match records with columns such as player names, surface, round, tournament information, score, ranking, match duration, and serve statistics for winners and losers.

## Output

Running the visualization script creates or updates the following files:

```text
visualization/figure_1.png
visualization/figure_2.png
visualization/figure_3.png
visualization/figure_4.png
visualization/figure_5.png
visualization/figure_6.png
```

These figures summarize match distribution, duration, serve performance, player results, upset patterns, and statistical outliers.

## Testing

The test suite checks important project behavior, including:

- Duplicate and empty-row removal during dataset loading
- Optional filter handling when columns are missing
- Interactive input validation
- Serve metric behavior when division-by-zero cases appear

Run all tests with:

```bash
pytest
```