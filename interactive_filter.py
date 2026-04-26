from __future__ import annotations

from pathlib import Path

import pandas as pd


DEFAULT_DATASET = Path("wta_matches_2024.csv")


def _normalize_text_series(series: pd.Series) -> pd.Series:
    return series.fillna("").astype(str).str.casefold().str.strip()


def load_dataset(filepath: str | Path) -> pd.DataFrame:
    """Load the dataset without depending on the existing analyzer modules."""
    df = pd.read_csv(filepath)
    df = df.drop_duplicates()
    df = df.dropna(how="all")
    return df


def _sorted_options(df: pd.DataFrame, column: str) -> list[str]:
    if column not in df.columns:
        return []
    values = (
        df[column]
        .dropna()
        .astype(str)
        .str.strip()
    )
    values = values[values != ""]
    return sorted(values.unique().tolist())


def filter_matches(
    df: pd.DataFrame,
    player: str | None = None,
    winner: str | None = None,
    loser: str | None = None,
    surface: str | None = None,
    round_name: str | None = None,
    tourney_level: str | None = None,
    limit: int | None = None,
) -> pd.DataFrame:
    """Filter matches using user-supplied parameters."""
    filtered = df.copy()

    if player:
        player_key = player.casefold().strip()
        winner_series = _normalize_text_series(filtered["winner_name"])
        loser_series = _normalize_text_series(filtered["loser_name"])
        filtered = filtered[(winner_series.str.contains(player_key)) | (loser_series.str.contains(player_key))]

    if winner:
        winner_key = winner.casefold().strip()
        filtered = filtered[_normalize_text_series(filtered["winner_name"]).str.contains(winner_key)]

    if loser:
        loser_key = loser.casefold().strip()
        filtered = filtered[_normalize_text_series(filtered["loser_name"]).str.contains(loser_key)]

    if surface and "surface" in filtered.columns:
        surface_key = surface.casefold().strip()
        filtered = filtered[_normalize_text_series(filtered["surface"]) == surface_key]

    if round_name and "round" in filtered.columns:
        round_key = round_name.casefold().strip()
        filtered = filtered[_normalize_text_series(filtered["round"]) == round_key]

    if tourney_level and "tourney_level" in filtered.columns:
        level_key = tourney_level.casefold().strip()
        filtered = filtered[_normalize_text_series(filtered["tourney_level"]) == level_key]

    if limit is not None and limit > 0:
        filtered = filtered.head(limit)

    return filtered.reset_index(drop=True)


def format_match_rows(df: pd.DataFrame) -> str:
    """Render filtered matches in a compact text format."""
    if df.empty:
        return "No matches found for the selected filters."

    lines = []
    for idx, row in df.iterrows():
        surface = row.get("surface", "Unknown")
        round_name = row.get("round", "Unknown")
        tourney_name = row.get("tourney_name", "Unknown tournament")
        score = row.get("score", "N/A")
        lines.append(
            f"{idx + 1}. {row['winner_name']} def. {row['loser_name']} | "
            f"{surface} | {round_name} | {tourney_name} | score: {score}"
        )
    return "\n".join(lines)


def prompt_choice(label: str, options: list[str]) -> str | None:
    """Ask the user to choose one option by number."""
    if not options:
        return None

    print()
    print(f"{label}:")
    print("0. Skip")
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")

    while True:
        raw = input("Select a number: ").strip()
        if raw == "":
            return None
        if raw.isdigit():
            choice = int(raw)
            if choice == 0:
                return None
            if 1 <= choice <= len(options):
                return options[choice - 1]
        print("Invalid selection. Enter a listed number.")


def prompt_limit(default: int = 10) -> int:
    print()
    while True:
        raw = input(f"Max number of matches to show [{default}]: ").strip()
        if raw == "":
            return default
        if raw.isdigit() and int(raw) > 0:
            return int(raw)
        print("Invalid number. Enter a positive integer.")


def prompt_filters(df: pd.DataFrame) -> dict[str, str | int | None]:
    """Prompt the user for step-by-step match filters."""
    print("Available filters")
    print("You can skip any step by choosing 0 or pressing Enter.")

    player = input("\nPlayer name keyword contains: ").strip() or None
    surface = prompt_choice("Surface", _sorted_options(df, "surface"))
    round_name = prompt_choice("Round", _sorted_options(df, "round"))
    tourney_level = prompt_choice("Tournament level", _sorted_options(df, "tourney_level"))
    winner = input("\nWinner name keyword contains: ").strip() or None
    loser = input("Loser name keyword contains: ").strip() or None
    limit = prompt_limit()

    return {
        "player": player,
        "winner": winner,
        "loser": loser,
        "surface": surface,
        "round_name": round_name,
        "tourney_level": tourney_level,
        "limit": limit,
    }


def main() -> None:
    df = load_dataset(DEFAULT_DATASET)
    filters = prompt_filters(df)
    filtered = filter_matches(df, **filters)

    print()
    print(f"Loaded {len(df)} matches from {DEFAULT_DATASET}")
    print(f"Filtered result count: {len(filtered)}")
    print(format_match_rows(filtered))


if __name__ == "__main__":
    main()
