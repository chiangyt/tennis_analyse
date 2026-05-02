import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from match_dataset import MatchDataset


class PairedMatchAnalyzer(MatchDataset):
    """Analyze serve performance differences between winner and loser within each match."""

    def __init__(self, filepath, cols=None, encoding="utf-8"):
        """Initialize the analyzer by loading data and computing paired differences.

        Args:
            filepath: Path to the CSV file.
            cols: List of column names to keep. Keeps all columns if None.
            encoding: File encoding. Defaults to "utf-8".
        """
        super().__init__(filepath, cols, encoding)
        self.diff_df = self.paired_differences()

    def paired_differences(self):
        """Compute per-match serve metric differences (winner minus loser).

        For each match, calculates the difference in each serve metric between
        the winner and the loser. A positive value means the winner outperformed
        the loser on that metric.

        Returns:
            DataFrame containing winner-minus-loser differences for all serve metrics.
        """
        df = self.df.copy()
        diff = pd.DataFrame()

        w_2nd = df["w_svpt"] - df["w_1stIn"]
        l_2nd = df["l_svpt"] - df["l_1stIn"]

        diff["1stIn_pct_diff"]    = df["w_1stIn"]  / df["w_svpt"] - df["l_1stIn"]  / df["l_svpt"]
        diff["1stWon_pct_diff"]   = df["w_1stWon"] / df["w_1stIn"] - df["l_1stWon"] / df["l_1stIn"]
        diff["2ndWon_pct_diff"]   = df["w_2ndWon"] / w_2nd - df["l_2ndWon"] / l_2nd
        diff["serve_won_pct_diff"] = (df["w_1stWon"] + df["w_2ndWon"]) / df["w_svpt"] - (df["l_1stWon"] + df["l_2ndWon"]) / df["l_svpt"]
        diff["ace_rate_diff"]     = df["w_ace"] / df["w_svpt"] - df["l_ace"] / df["l_svpt"]

        return diff.dropna(how="all")

    def summary(self):
        """Summarize paired differences: mean difference and winner advantage rate per metric.

        For each metric, reports the mean difference (winner minus loser) and
        the proportion of matches where the winner outperformed the loser.

        Returns:
            Dict mapping each metric name to a dict with mean_diff and winner_advantage_rate.
        """
        records = {}
        for col in self.diff_df.columns:
            series = self.diff_df[col].dropna()
            records[col] = {
                "mean_diff": round(series.mean(), 4),
                "winner_advantage_rate": round((series > 0).mean(), 4),
            }
        return pd.DataFrame(records).T