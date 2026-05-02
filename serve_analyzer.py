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
            - Ace rate and double-fault rate

        Returns:
            DataFrame containing all computed serve metrics.
        """
        
        df = self.df.copy()
        metrics_df = pd.DataFrame()

        w_2nd_total = df["w_svpt"] - df["w_1stIn"]
        l_2nd_total = df["l_svpt"] - df["l_1stIn"]

        metrics_df["winner_first_in_pct"]    = df["w_1stIn"] / df["w_svpt"]
        metrics_df["loser_first_in_pct"]     = df["l_1stIn"] / df["l_svpt"]
        metrics_df["winner_first_won_pct"]   = df["w_1stWon"] / df["w_1stIn"]
        metrics_df["loser_first_won_pct"]    = df["l_1stWon"] / df["l_1stIn"]
        metrics_df["winner_second_won_pct"]  = df["w_2ndWon"] / w_2nd_total
        metrics_df["loser_second_won_pct"]   = df["l_2ndWon"] / l_2nd_total
        metrics_df["winner_serve_win_pct"]   = (df["w_1stWon"] + df["w_2ndWon"]) / df["w_svpt"]
        metrics_df["loser_serve_win_pct"]    = (df["l_1stWon"] + df["l_2ndWon"]) / df["l_svpt"]
        metrics_df["winner_ace_rate"]        = df["w_ace"] / df["w_svpt"]
        metrics_df["loser_ace_rate"]         = df["l_ace"] / df["l_svpt"]
        metrics_df["winner_df_rate"]         = df["w_df"] / df["w_svpt"]
        metrics_df["loser_df_rate"]          = df["l_df"] / df["l_svpt"]

        self.metrics_df = metrics_df
        return metrics_df

    def compute_group_state(self):
        """Compute mean and median for each serve metric, grouped by winner/loser.

        Returns:
            Dict mapping each metric name to a dict with winner_mean,
            loser_mean, winner_median, and loser_median values.
        """
        metrics = ["first_in_pct", "first_won_pct", "second_won_pct", "serve_win_pct", "ace_rate", "df_rate"]
        lines = []
        for metric in metrics:
            w_mean   = self.metrics_df[f"winner_{metric}"].mean()
            l_mean   = self.metrics_df[f"loser_{metric}"].mean()
            w_median = self.metrics_df[f"winner_{metric}"].median()
            l_median = self.metrics_df[f"loser_{metric}"].median()
            lines.append(
                f"{metric}:\n"
                f"  winner  mean={w_mean:.2f}  median={w_median:.2f}\n"
                f"  loser   mean={l_mean:.2f}  median={l_median:.2f}"
            )
        return "\n".join(lines)

    def plot_distributions(self):
        """KDE plots comparing winner vs loser distribution for each serve metric."""
        metrics = ["first_in_pct", "first_won_pct", "second_won_pct", "serve_win_pct", "ace_rate", "df_rate"]
        labels  = ["1st Serve In %", "1st Serve Won %", "2nd Serve Won %", "Serve Win %", "Ace Rate", "DF Rate"]

        fig, axes = plt.subplots(2, 3, figsize=(15, 8))
        fig.suptitle("Serve Metric Distributions: Winners vs Losers", fontsize=14)

        for ax, metric, label in zip(axes.flat, metrics, labels):
            w = self.metrics_df[f"winner_{metric}"].dropna()
            l = self.metrics_df[f"loser_{metric}"].dropna()
            w.plot(kind="kde", ax=ax, label="Winner", color="#2a9d8f")
            l.plot(kind="kde", ax=ax, label="Loser",  color="#e76f51")
            ax.set_title(label)
            ax.set_xlabel("Rate")
            ax.legend()

        plt.tight_layout()
        plt.show()
