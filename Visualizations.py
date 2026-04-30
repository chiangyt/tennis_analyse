import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from IPython.display import display
from match_dataset import MatchDataset
from serve_analyzer import ServeAnalyzer
sns.set_theme(style="whitegrid",context="talk")
plt.rcParams["figure.figsize"]=(12,7)
plt.rcParams["axes.spines.top"]=False
plt.rcParams["axes.spines.right"]=False
DATA_PATH=Path("wta_matches_2024.csv")
VIS_PATH=Path("visualization")
VIS_PATH.mkdir(exist_ok=True)
df=MatchDataset(DATA_PATH).df
df["tourney_date"]=pd.to_datetime(df["tourney_date"].astype(str),format="%Y%m%d",errors="coerce")
print("Dataset shape:",df.shape)
##------------------------------------------------------------------------------------------------------
display(df.head())
display(df.sample(5,random_state=42))
overview=pd.DataFrame({"dtype":df.dtypes.astype(str),"missing":df.isna().sum(),"missing_pct":(df.isna().mean()*100).round(2),"unique_values":df.nunique(dropna=True)}).sort_values(["missing_pct","unique_values"],ascending=[False,False])
display(overview.head(20))
display(df[["minutes","winner_rank","loser_rank","w_svpt","l_svpt"]].describe().T)
print("Surface distribution:")
display(df["surface"].value_counts(dropna=False).rename_axis("surface").to_frame("matches"))
print("Tournament level distribution:")
display(df["tourney_level"].value_counts(dropna=False).rename_axis("tourney_level").to_frame("matches"))
print("Round distribution:")
display(df["round"].value_counts(dropna=False).rename_axis("round").to_frame("matches"))
analysis_df=df.join(ServeAnalyzer(DATA_PATH).metrics_df)
analysis_df["serve_gap"]=analysis_df["winner_serve_win_pct"]-analysis_df["loser_serve_win_pct"]
analysis_df["first_in_gap"]=analysis_df["winner_first_in_pct"]-analysis_df["loser_first_in_pct"]
analysis_df["rank_gap"]=analysis_df["loser_rank"]-analysis_df["winner_rank"]
analysis_df["is_upset"]=(analysis_df["winner_rank"]>analysis_df["loser_rank"]).fillna(False)
analysis_df["total_aces"]=analysis_df["w_ace"]+analysis_df["l_ace"]
analysis_df["total_double_faults"]=analysis_df["w_df"]+analysis_df["l_df"]
analysis_df["month"]=analysis_df["tourney_date"].dt.month

display(analysis_df[["winner_serve_win_pct","loser_serve_win_pct","winner_first_in_pct","loser_first_in_pct","serve_gap","rank_gap","is_upset"]].describe().T)
fig,axes=plt.subplots(2,2,figsize=(18,12))
##------------------------------------------------------------------------------------------------------
surface_counts=analysis_df["surface"].value_counts(dropna=False)
surface_counts.plot(kind="bar",color=["#2a9d8f","#e76f51","#264653","#8d99ae"],ax=axes[0,0])
axes[0,0].set_title("Match Counts by Surface")
axes[0,0].set_ylabel("Matches")
axes[0,0].tick_params(axis="x",rotation=0)
level_counts=analysis_df["tourney_level"].value_counts()
level_counts.plot(kind="bar",color="#457b9d",ax=axes[0,1])
axes[0,1].set_title("Match Counts by Tournament Level")
axes[0,1].set_ylabel("Matches")
axes[0,1].tick_params(axis="x",rotation=0)
round_order=["R128","R64","R32","R16","QF","SF","F","RR"]
round_counts=analysis_df["round"].value_counts().reindex(round_order).dropna()
round_counts.plot(kind="bar",color="#f4a261",ax=axes[1,0])
axes[1,0].set_title("Main Round Distribution")
axes[1,0].set_ylabel("Matches")
axes[1,0].tick_params(axis="x",rotation=0)
monthly_counts=analysis_df["month"].value_counts().sort_index()
monthly_counts.plot(marker="o",linewidth=3,color="#6a4c93",ax=axes[1,1])
axes[1,1].set_title("Matches by Month")
axes[1,1].set_xlabel("Month")
axes[1,1].set_ylabel("Matches")
plt.tight_layout()
plt.savefig(VIS_PATH/"figure_1.png",dpi=300,bbox_inches="tight")

plt.show()

fig,axes=plt.subplots(2,2,figsize=(18,12))
sns.histplot(analysis_df["minutes"].dropna(),bins=30,kde=True,color="#1d3557",ax=axes[0,0])
##------------------------------------------------------------------------------------------------------
axes[0,0].set_title("Distribution of Match Duration")
axes[0,0].set_xlabel("Minutes")
sns.boxplot(data=analysis_df,x="surface",y="minutes",palette="Set2",ax=axes[0,1])
axes[0,1].set_title("Match Duration by Surface")
axes[0,1].set_xlabel("Surface")
axes[0,1].set_ylabel("Minutes")
round_focus=analysis_df[analysis_df["round"].isin(["R128","R64","R32","R16","QF","SF","F"])].copy()
sns.boxplot(data=round_focus,x="round",y="minutes",order=["R128","R64","R32","R16","QF","SF","F"],palette="crest",ax=axes[1,0])
axes[1,0].set_title("Match Duration by Round")
axes[1,0].set_xlabel("Round")
axes[1,0].set_ylabel("Minutes")
scatter_df=analysis_df.dropna(subset=["winner_serve_win_pct","loser_serve_win_pct","surface"]).copy()
sns.scatterplot(data=scatter_df,x="loser_serve_win_pct",y="winner_serve_win_pct",hue="surface",alpha=0.65,s=55,ax=axes[1,1])
axes[1,1].axline((0.35,0.35),slope=1,linestyle="--",color="black",linewidth=1)
axes[1,1].set_title("Winner vs Loser Serve Win Rate")
axes[1,1].set_xlabel("Loser Serve Win Rate")
axes[1,1].set_ylabel("Winner Serve Win Rate")
plt.tight_layout()
plt.savefig(VIS_PATH/"figure_2.png",dpi=300,bbox_inches="tight")
plt.show()
metric_summary=pd.DataFrame({"winner_mean":analysis_df[["winner_serve_win_pct","winner_first_in_pct","winner_first_won_pct","winner_second_won_pct","winner_ace_rate","winner_df_rate"]].mean(),"loser_mean":analysis_df[["loser_serve_win_pct","loser_first_in_pct","loser_first_won_pct","loser_second_won_pct","loser_ace_rate","loser_df_rate"]].mean().values},index=["serve_win_pct","first_in_pct","first_won_pct","second_won_pct","ace_rate","df_rate"])
surface_summary=analysis_df.groupby("surface")[["winner_serve_win_pct","loser_serve_win_pct","minutes","total_aces"]].mean()
fig,axes=plt.subplots(2,2,figsize=(18,12))
metric_summary.plot(kind="bar",ax=axes[0,0],color=["#2a9d8f","#e76f51"])
axes[0,0].set_title("Average Winner vs Loser Performance")
axes[0,0].set_ylabel("Value")
axes[0,0].tick_params(axis="x",rotation=25)
sns.violinplot(data=analysis_df.dropna(subset=["surface","serve_gap"]),x="surface",y="serve_gap",palette="Set3",ax=axes[0,1])
axes[0,1].set_title("Serve Advantage Distribution by Surface")
axes[0,1].set_xlabel("Surface")
axes[0,1].set_ylabel("Winner - Loser Serve Win Rate")
surface_summary[["winner_serve_win_pct","loser_serve_win_pct"]].plot(kind="bar",ax=axes[1,0],color=["#264653","#f4a261"])
axes[1,0].set_title("Serve Win Rate by Surface")
axes[1,0].set_ylabel("Rate")
axes[1,0].tick_params(axis="x",rotation=0)
corr_cols=["minutes","winner_serve_win_pct","loser_serve_win_pct","winner_first_in_pct","loser_first_in_pct","serve_gap","rank_gap","total_aces","total_double_faults"]
corr=analysis_df[corr_cols].corr(numeric_only=True)
sns.heatmap(corr,cmap="coolwarm",center=0,annot=True,fmt=".2f",ax=axes[1,1])
axes[1,1].set_title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(VIS_PATH/"figure_3.png",dpi=300,bbox_inches="tight")
plt.show()
##------------------------------------------------------------------------------------------------------
player_results=pd.concat([analysis_df[["winner_name","surface"]].rename(columns={"winner_name":"player"}).assign(win=1),analysis_df[["loser_name","surface"]].rename(columns={"loser_name":"player"}).assign(win=0)],ignore_index=True)
player_summary=player_results.groupby("player").agg(matches=("win","size"),wins=("win","sum"))
player_summary["win_rate"]=player_summary["wins"]/player_summary["matches"]
top_win_totals=player_summary.sort_values("wins",ascending=False).head(15)
top_win_rate=player_summary.query("matches >= 15").sort_values(["win_rate","wins"],ascending=[False,False]).head(15)
surface_player=player_results.groupby(["player","surface"]).agg(matches=("win","size"),wins=("win","sum")).reset_index()
surface_player["win_rate"]=surface_player["wins"]/surface_player["matches"]
surface_pivot=surface_player.query("matches >= 5").pivot(index="player",columns="surface",values="win_rate").loc[top_win_rate.index[:10]]
fig,axes=plt.subplots(2,2,figsize=(18,13))
top_win_totals["wins"].sort_values().plot(kind="barh",color="#457b9d",ax=axes[0,0])
axes[0,0].set_title("Top 15 Players by Wins")
axes[0,0].set_xlabel("Wins")
axes[0,0].set_ylabel("")
top_win_rate["win_rate"].sort_values().plot(kind="barh",color="#2a9d8f",ax=axes[0,1])
axes[0,1].set_title("Top Win Rates (Min 15 Matches)")
axes[0,1].set_xlabel("Win Rate")
axes[0,1].set_ylabel("")
sns.heatmap(surface_pivot,cmap="YlGnBu",annot=True,fmt=".2f",ax=axes[1,0])
axes[1,0].set_title("Surface Win Rate for Leading Players")
axes[1,0].set_xlabel("Surface")
axes[1,0].set_ylabel("Player")
top_ranked_matches=analysis_df[analysis_df["winner_name"].isin(top_win_totals.index[:10])|analysis_df["loser_name"].isin(top_win_totals.index[:10])].copy()
elite_counts=pd.concat([top_ranked_matches[["winner_name"]].rename(columns={"winner_name":"player"}).assign(result="Win"),top_ranked_matches[["loser_name"]].rename(columns={"loser_name":"player"}).assign(result="Loss")],ignore_index=True)
elite_counts=elite_counts[elite_counts["player"].isin(top_win_totals.index[:10])]
sns.countplot(data=elite_counts,y="player",hue="result",order=top_win_totals.index,palette=["#2a9d8f","#e76f51"],ax=axes[1,1])
axes[1,1].set_title("Win/Loss Split for Top Winners")
axes[1,1].set_xlabel("Matches")
axes[1,1].set_ylabel("")
plt.tight_layout()
plt.savefig(VIS_PATH/"figure_4.png",dpi=300,bbox_inches="tight")
plt.show()
##------------------------------------------------------------------------------------------------------
upset_surface=analysis_df.groupby("surface")["is_upset"].mean().sort_values(ascending=False)
upset_level=analysis_df.groupby("tourney_level")["is_upset"].mean().sort_values(ascending=False)
fig,axes=plt.subplots(2,2,figsize=(18,12))
upset_surface.plot(kind="bar",color="#e76f51",ax=axes[0,0])
axes[0,0].set_title("Upset Rate by Surface")
axes[0,0].set_ylabel("Upset Rate")
axes[0,0].tick_params(axis="x",rotation=0)
upset_level.plot(kind="bar",color="#6d597a",ax=axes[0,1])
axes[0,1].set_title("Upset Rate by Tournament Level")
axes[0,1].set_ylabel("Upset Rate")
axes[0,1].tick_params(axis="x",rotation=0)
rank_view=analysis_df.dropna(subset=["rank_gap","minutes","serve_gap"]).copy()
sns.scatterplot(data=rank_view,x="rank_gap",y="serve_gap",hue="is_upset",alpha=0.65,palette={False:"#457b9d",True:"#e63946"},ax=axes[1,0])
axes[1,0].axvline(0,linestyle="--",color="black",linewidth=1)
axes[1,0].set_title("Ranking Gap vs Serve Advantage")
axes[1,0].set_xlabel("Loser Rank - Winner Rank")
axes[1,0].set_ylabel("Serve Gap")
sns.boxplot(data=rank_view,x="is_upset",y="minutes",palette=["#a8dadc","#ffb4a2"],ax=axes[1,1])
axes[1,1].set_title("Match Duration: Upset vs Non-Upset")
axes[1,1].set_xlabel("Is Upset")
axes[1,1].set_ylabel("Minutes")
plt.tight_layout()
plt.savefig(VIS_PATH/"figure_5.png",dpi=300,bbox_inches="tight")
plt.show()
##------------------------------------------------------------------------------------------------------
outlier_metrics=["minutes","serve_gap","rank_gap","total_aces","total_double_faults"]
outlier_df=analysis_df.dropna(subset=outlier_metrics+["winner_name","loser_name","tourney_name","score"]).copy()
for col in outlier_metrics:
    median=outlier_df[col].median()
    mad=(outlier_df[col]-median).abs().median()
    if mad==0:
        outlier_df[f"{col}_rz"]=0.0
    else:
        outlier_df[f"{col}_rz"]=0.6745*(outlier_df[col]-median)/mad
rz_cols=[f"{col}_rz" for col in outlier_metrics]
outlier_df["outlier_score"]=outlier_df[rz_cols].abs().sum(axis=1)
top_outliers=outlier_df.sort_values("outlier_score",ascending=False).head(12).copy()
fig,axes=plt.subplots(1,2,figsize=(18,7))
sns.scatterplot(data=outlier_df,x="minutes",y="serve_gap",hue="surface",size="outlier_score",sizes=(20,350),alpha=0.55,ax=axes[0])
axes[0].set_title("Outlier Detection View: Minutes vs Serve Gap")
axes[0].set_xlabel("Minutes")
axes[0].set_ylabel("Serve Gap")
for _,row in top_outliers.head(8).iterrows():
    axes[0].annotate(row["winner_name"].split()[0],(row["minutes"],row["serve_gap"]),fontsize=9,alpha=0.9)
sns.barplot(data=top_outliers,y="winner_name",x="outlier_score",color="#d62828",ax=axes[1])
axes[1].set_title("Top Anomalous Matches by Winner")
axes[1].set_xlabel("Composite Outlier Score")
axes[1].set_ylabel("Winner")
plt.tight_layout()
plt.savefig(VIS_PATH/"figure_6.png",dpi=300,bbox_inches="tight")
plt.show()
display(top_outliers[["tourney_name","surface","round","winner_name","loser_name","score","minutes","serve_gap","rank_gap","total_aces","total_double_faults","outlier_score"]])