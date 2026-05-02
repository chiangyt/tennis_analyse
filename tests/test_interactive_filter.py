import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from interactive_filter import filter_matches, prompt_choice, prompt_limit
from match_dataset import MatchDataset
from serve_analyzer import ServeAnalyzer


def test_load_dataset_removes_duplicate_and_all_null_rows(tmp_path: Path) -> None:
    path = tmp_path / "sample.csv"
    pd.DataFrame(
        [
            {"winner_name": "Iga Swiatek", "loser_name": "Coco Gauff", "surface": "Clay"},
            {"winner_name": "Iga Swiatek", "loser_name": "Coco Gauff", "surface": "Clay"},
            {"winner_name": None, "loser_name": None, "surface": None},
        ]
    ).to_csv(path, index=False)

    loaded = MatchDataset(path).df

    assert len(loaded) == 1


def test_filter_matches_ignores_missing_optional_columns() -> None:
    df = pd.DataFrame(
        [
            {"winner_name": "A", "loser_name": "B"},
            {"winner_name": "C", "loser_name": "D"},
        ]
    )

    filtered = filter_matches(df, surface="Hard", round_name="F", tourney_level="G")

    assert len(filtered) == 2


def test_prompt_choice_retries_after_invalid_input(monkeypatch, capsys) -> None:
    responses = iter(["9", "abc", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    selected = prompt_choice("Surface", ["Clay", "Hard"])
    output = capsys.readouterr().out

    assert selected == "Clay"
    assert output.count("Invalid selection. Enter a listed number.") == 2


def test_prompt_limit_retries_until_valid_positive_integer(monkeypatch, capsys) -> None:
    responses = iter(["-1", "0", "abc", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    limit = prompt_limit()
    output = capsys.readouterr().out

    assert limit == 3
    assert output.count("Invalid number. Enter a positive integer.") == 3


def test_serve_analyzer_handles_zero_division_as_nan(tmp_path: Path) -> None:
    path = tmp_path / "serve_zero_division.csv"
    pd.DataFrame(
        [
            {
                "winner_name": "Player G",
                "loser_name": "Player H",
                "surface": "Hard",
                "w_svpt": 8,
                "w_1stIn": 8,
                "w_1stWon": 5,
                "w_2ndWon": 0,
                "w_ace": 2,
                "w_df": 1,
                "l_svpt": 0,
                "l_1stIn": 0,
                "l_1stWon": 0,
                "l_2ndWon": 0,
                "l_ace": 0,
                "l_df": 0,
            }
        ]
    ).to_csv(path, index=False)

    row = ServeAnalyzer(path).metrics_df.iloc[0]

    assert row["winner_first_in_pct"] == 1.0
    assert pd.isna(row["winner_second_won_pct"])
    assert pd.isna(row["loser_first_in_pct"])


def test_match_dataset_raises_on_missing_columns(tmp_path: Path) -> None:
    path = tmp_path / "sample.csv"
    pd.DataFrame([{"winner_name": "A", "loser_name": "B"}]).to_csv(path, index=False)

    try:
        MatchDataset(path, cols=["winner_name", "nonexistent_col"])
        assert False, "Expected KeyError"
    except KeyError as e:
        assert "nonexistent_col" in str(e)

