import pandas as pd
import matplotlib.pyplot as plt

from match_dataset import MatchDataset


class ServeAnalyzer(MatchDataset):
    """Analyze serve performance metrics for winners and losers across matches."""

    def __init__(self, filepath, cols=None, encoding="utf-8"):
        """Initialize the analyzer by loading data and computing serve metrics.

        Args:
            filepath: Path to the CSV file.
            cols: List of column names to keep. Keeps all columns if None.
            encoding: File encoding. Defaults to "utf-8".
        """
        super().__init__(filepath, cols, encoding)
        self.metrics_df = self.cal_serve_metrics()

    def cal_serve_metrics(self):
        """Calculate serve performance metrics for both winners and losers.

        Computes the following metrics:
            - 1st serve in percentage
            - 1st serve points won percentage
            - 2nd serve points won percentage
            - Overall serve points won percentage
            - Serve aggressiveness (ace - double fault ratio)

        Returns:
            DataFrame containing all computed serve metrics.
        """
        
        df = self.df.copy()
        metrics_df = pd.DataFrame()

        # First serve in %
        metrics_df["w_1stIn_pct"] = self.df["w_1stIn"] / self.df["w_svpt"]
        metrics_df["l_1stIn_pct"] = self.df["l_1stIn"] / self.df["l_svpt"]

        # First serve points won %
        metrics_df["w_1stWon_pct"] = self.df["w_1stWon"] / self.df["w_1stIn"]
        metrics_df["l_1stWon_pct"] = self.df["l_1stWon"] / self.df["l_1stIn"]

        # Second serve total
        w_2nd_total = self.df["w_svpt"] - self.df["w_1stIn"]
        l_2nd_total = self.df["l_svpt"] - self.df["l_1stIn"]

        # Second serve points won %
        metrics_df["w_2ndWon_pct"] = self.df["w_2ndWon"] / w_2nd_total
        metrics_df["l_2ndWon_pct"] = self.df["l_2ndWon"] / l_2nd_total

        # Serve points won %
        metrics_df["w_serve_won_pct"] = (self.df["w_1stWon"] + self.df["w_2ndWon"]) / self.df["w_svpt"]
        metrics_df["l_serve_won_pct"] = (self.df["l_1stWon"] + self.df["l_2ndWon"]) / self.df["l_svpt"]

        # Serve aggresive
        metrics_df["w_serve_aggresive"] = (self.df["w_ace"] - self.df["w_df"]) / self.df["w_svpt"]
        metrics_df["l_serve_aggresive"] = (self.df["l_ace"] - self.df["l_df"]) / self.df["l_svpt"]

        self.metrics_df = metrics_df
        return metrics_df

    def compute_group_state(self):
        """Compute mean and median for each serve metric, grouped by winner/loser.

        Returns:
            Dict mapping each metric name to a dict with winner_mean,
            loser_mean, winner_median, and loser_median values.
        """
        stats = {}
        metrics = ["1stIn_pct", "1stWon_pct", "2ndWon_pct", "serve_won_pct", "serve_aggresive"]
        for metric in metrics:
            stats[metric] = {
                "winner_mean": self.metrics_df[f"w_{metric}"].mean(),
                "loser_mean": self.metrics_df[f"l_{metric}"].mean(),
                "winner_median": self.metrics_df[f"w_{metric}"].median(),
                "loser_median": self.metrics_df[f"l_{metric}"].median()
            }
        return stats