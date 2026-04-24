import sys,re
from pathlib import Path
import pandas as pd
import pytest

PROJECT_ROOT=Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT)not in sys.path:sys.path.insert(0,str(PROJECT_ROOT))

from match_dataset import MatchDataset
from paired_analyzer import PairedMatchAnalyzer
from serve_analyzer import ServeAnalyzer

@pytest.fixture
def sample_csv(tmp_path:Path)->Path:
    ##test case
    rows=[
        {"winner_name":"Player A","loser_name":"Player B","surface":"Hard","w_svpt":10,"w_1stIn":6,"w_1stWon":4,"w_2ndWon":2,"w_ace":1,"w_df":0,"l_svpt":8,"l_1stIn":4,"l_1stWon":2,"l_2ndWon":1,"l_ace":0,"l_df":1},
        {"winner_name":"Player C","loser_name":"Player D","surface":"Clay","w_svpt":12,"w_1stIn":9,"w_1stWon":7,"w_2ndWon":1,"w_ace":2,"w_df":1,"l_svpt":10,"l_1stIn":6,"l_1stWon":3,"l_2ndWon":2,"l_ace":1,"l_df":2},
        {"winner_name":"Player C","loser_name":"Player D","surface":"Clay","w_svpt":12,"w_1stIn":9,"w_1stWon":7,"w_2ndWon":1,"w_ace":2,"w_df":1,"l_svpt":10,"l_1stIn":6,"l_1stWon":3,"l_2ndWon":2,"l_ace":1,"l_df":2},
        dict.fromkeys(["winner_name","loser_name","surface","w_svpt","w_1stIn","w_1stWon","w_2ndWon","w_ace","w_df","l_svpt","l_1stIn","l_1stWon","l_2ndWon","l_ace","l_df"])
    ]
    path=tmp_path/"sample_matches.csv"
    pd.DataFrame(rows).to_csv(path,index=False)
    return path

def test_match_dataset_cleans_data_and_formats_preview(sample_csv:Path)->None:
    dataset=MatchDataset(sample_csv)
    assert len(dataset)==2
    assert str(dataset)=="MatchDataset with 2 matches and 15 columns."
    preview=dataset.preview_matches()
    assert "Match 1: Winner: Player A, Loser: Player B, surface:Hard" in preview
    assert "W(svpt:10 1stIn:6 1stWon:4 2ndWon:2)" in preview
    assert "Match 2: Winner: Player C, Loser: Player D, surface:Clay" in preview

def test_match_dataset_can_select_columns(sample_csv:Path)->None:
    dataset=MatchDataset(sample_csv,cols=["winner_name","loser_name"])
    assert list(dataset.df.columns)==["winner_name","loser_name"]
    assert len(dataset)==2

def test_match_dataset_raises_for_missing_file(tmp_path:Path)->None:
    missing_path=tmp_path/"missing.csv"
    with pytest.raises(FileNotFoundError,match=re.escape(f"File not found: {missing_path}")):MatchDataset(missing_path)

def test_serve_analyzer_computes_expected_metrics(sample_csv:Path)->None:
    first_row=ServeAnalyzer(sample_csv).metrics_df.iloc[0]
    assert first_row["w_1stIn_pct"]==pytest.approx(.6)
    assert first_row["l_1stIn_pct"]==pytest.approx(.5)
    assert first_row["w_1stWon_pct"]==pytest.approx(4/6)
    assert first_row["l_1stWon_pct"]==pytest.approx(.5)
    assert first_row["w_2ndWon_pct"]==pytest.approx(.5)
    assert first_row["l_2ndWon_pct"]==pytest.approx(.25)
    assert first_row["w_serve_won_pct"]==pytest.approx(.6)
    assert first_row["l_serve_won_pct"]==pytest.approx(.375)
    assert first_row["w_serve_aggresive"]==pytest.approx(.1)
    assert first_row["l_serve_aggresive"]==pytest.approx(-.125)

def test_serve_analyzer_group_state_summary(sample_csv:Path)->None:
    summary=ServeAnalyzer(sample_csv).compute_group_state()
    assert "1stIn_pct:" in summary
    assert "winner  mean=0.68  median=0.68" in summary
    assert "loser   mean=0.55  median=0.55" in summary
    assert "serve_aggresive:" in summary

def test_paired_analyzer_builds_difference_frame_and_summary(sample_csv:Path)->None:
    analyzer=PairedMatchAnalyzer(sample_csv)
    assert list(analyzer.diff_df.columns)==["1stIn_pct_diff","1stWon_pct_diff","2ndWon_pct_diff","serve_won_pct_diff","ace_rate_diff"]
    first_row=analyzer.diff_df.iloc[0]
    assert first_row["1stIn_pct_diff"]==pytest.approx(.1)
    assert first_row["1stWon_pct_diff"]==pytest.approx(4/6-.5)
    assert first_row["2ndWon_pct_diff"]==pytest.approx(.25)
    assert first_row["serve_won_pct_diff"]==pytest.approx(.225)
    assert first_row["ace_rate_diff"]==pytest.approx(.1)
    summary=analyzer.summary()
    assert summary.loc["1stIn_pct_diff","mean_diff"]==pytest.approx(.125)
    assert summary.loc["ace_rate_diff","winner_advantage_rate"]==pytest.approx(1)