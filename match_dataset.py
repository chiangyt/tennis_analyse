import pandas as pd
import matplotlib.pyplot as plt


class MatchDataset:
    """Tennis match dataset for loading, cleaning, and previewing match data."""

    def __init__(self, filepath, cols=None, encoding="utf-8"):
        """Load a CSV file and preprocess the data.

        Args:
            filepath: Path to the CSV file.
            cols: List of column names to keep. Keeps all columns if None.
            encoding: File encoding. Defaults to "utf-8".

        Raises:
            FileNotFoundError: If the specified file does not exist.
        """
        try:
            self.df = pd.read_csv(filepath, encoding=encoding)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filepath}")

        self.df = self._process(self.df, cols)

    def _process(self, df, cols=None):
        """Remove duplicates, select columns, and drop all-null rows.

        Args:
            df: Raw DataFrame.
            cols: List of column names to keep.

        Returns:
            Cleaned DataFrame.
        """
        df = df.drop_duplicates()
        if cols:
            missing = set(cols) - set(df.columns)
            if missing:
                raise KeyError(f"Columns not found in dataset: {sorted(missing)}")
            df = df[cols]
        df = df.dropna(how="all")
        return df

    def options(self, column: str) -> list:
        """Return sorted unique non-null values for a given column."""
        if column not in self.df.columns:
            return []
        values = self.df[column].dropna().astype(str).str.strip()
        return sorted(values[values != ""].unique().tolist())

    def __len__(self):
        """Return the number of matches in the dataset."""
        return len(self.df)

    def preview_matches(self, limit=None):
        """Format a line-by-line summary of serve statistics for every match.

        Args:
            limit: Maximum number of matches to preview. Shows all if None.

        Returns:
            A multi-line string with winner/loser serve stats per match.
        """
        rows = self.df.head(limit) if limit is not None else self.df
        lines = []
        for i, row in rows.iterrows():
            line = (f"Match {i+1}: Winner: {row['winner_name']}, Loser: {row['loser_name']}, surface:{row['surface']} | "
                    f"W(svpt:{row['w_svpt']:.0f} 1stIn:{row['w_1stIn']:.0f} 1stWon:{row['w_1stWon']:.0f} 2ndWon:{row['w_2ndWon']:.0f}) "
                    f"L(svpt:{row['l_svpt']:.0f} 1stIn:{row['l_1stIn']:.0f} 1stWon:{row['l_1stWon']:.0f} 2ndWon:{row['l_2ndWon']:.0f})")
            lines.append(line)
        return "\n".join(lines)
    
    def __str__(self):
        """Return a brief description of the dataset (match count and column count)."""
        return f"MatchDataset with {len(self.df)} matches and {len(self.df.columns)} columns."
