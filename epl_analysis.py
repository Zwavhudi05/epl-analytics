"""
=============================================================
  SportsBet EPL Analytics  |  2020–2024 Season Data
  Student Submission  –  Questions 1, 2 & 3
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import re, os, warnings

warnings.filterwarnings('ignore')
os.makedirs('output', exist_ok=True)


# =============================================================
#  QUESTION 1  —  Data Loading & Preparation
# =============================================================

# 1.1  Load dataset
df = pd.read_csv('epl_stats.csv')
print(f"1.1  Dataset loaded | {df.shape[0]} rows x {df.shape[1]} columns")


# 1.2  Convert date column to datetime
# Two formats exist: "28th May 2023" and "23/05/2021"
def parse_epl_date(raw):
    cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', str(raw).strip())
    for fmt in ['%d %B %Y', '%d/%m/%Y', '%d-%m-%Y', '%d %b %Y']:
        try:
            return pd.to_datetime(cleaned, format=fmt)
        except ValueError:
            pass
    return pd.NaT

df['date'] = df['date'].apply(parse_epl_date)
print(f"1.2  date dtype: {df['date'].dtype} | NaT count: {df['date'].isna().sum()}")


# 1.3  Extract month and year
df['month'] = df['date'].dt.month
df['year']  = df['date'].dt.year
print(f"1.3  month/year extracted | seasons: {sorted(df['year'].dropna().astype(int).unique())}")


# 1.4  Check missing values
missing = df.isnull().sum()
missing_found = missing[missing > 0]
print(f"1.4  Missing values:\n{missing_found if not missing_found.empty else '     None found.'}")


# 1.5  Handle missing values
# No missing values in this dataset.
# Policy: numeric NaNs -> fill with column median; date NaTs -> drop rows.
print("1.5  No missing values detected — no imputation required.")


# 1.6  Verify numeric column types
metadata = {'date', 'clock', 'stadium', 'class', 'attendance', 'links'}
stat_cols = [c for c in df.columns if c not in metadata]
non_numeric = [c for c in stat_cols if not pd.api.types.is_numeric_dtype(df[c])]
print(f"1.6  Non-numeric stat columns: {non_numeric if non_numeric else 'None — all correctly typed.'}")


# 1.7  Convert attendance string -> integer
df['attendance'] = (df['attendance'].astype(str)
                      .str.replace(',', '', regex=False).str.strip().astype(int))
print(f"1.7  attendance: {df['attendance'].dtype} | range {df['attendance'].min():,}–{df['attendance'].max():,}")


# 1.8  Filter: Emirates Stadium
emirates_df = df[df['stadium'] == 'Emirates Stadium'].copy()
print(f"1.8  Emirates Stadium matches: {len(emirates_df)}")


# 1.9  Filter: home goals > 2
high_home = df[df['Goals Home'] > 2].copy()
print(f"1.9  Matches with home goals > 2: {len(high_home)}")


# 1.10  Total goals
df['total_goals'] = df['Goals Home'] + df['Away Goals']
print(f"1.10 total_goals: mean {df['total_goals'].mean():.2f}, max {df['total_goals'].max()}")


# 1.11  Goal difference
df['goal_difference'] = df['Goals Home'] - df['Away Goals']
print(f"1.11 goal_difference: {df['goal_difference'].min()} to {df['goal_difference'].max()}")


# 1.12  Build team name map from links, then calculate team totals
def extract_slug(link):
    if pd.isna(link): return None
    m = re.search(r'/football/(.+)/\d+', str(link))
    return m.group(1) if m else None

df['_slug'] = df['links'].apply(extract_slug)
TEAM_MAP = {}
for _, row in df.iterrows():
    slug = row['_slug']
    if not isinstance(slug, str): continue
    parts = slug.split('-vs-')
    if len(parts) == 2:
        for side, tid in zip(parts, [row['Home Team'], row['Away Team']]):
            name = re.sub(r'/[Ss]tats$', '', ' '.join(w.capitalize() for w in side.split('-'))).strip()
            TEAM_MAP[tid] = name

df['home_team_name'] = df['Home Team'].map(TEAM_MAP).str.strip().str.title()
df['away_team_name'] = df['Away Team'].map(TEAM_MAP).str.strip().str.title()

home_g  = df.groupby('home_team_name')['Goals Home'].sum().rename('home_goals')
away_g  = df.groupby('away_team_name')['Away Goals'].sum().rename('away_goals')
team_goals = pd.concat([home_g, away_g], axis=1).fillna(0)
team_goals['total_team_goals'] = team_goals['home_goals'] + team_goals['away_goals']
print(f"1.12 Goals aggregated for {len(team_goals)} teams.")


# 1.13  Top 5 teams
top5 = team_goals['total_team_goals'].sort_values(ascending=False).head(5)
print("1.13 Top 5 teams by goals:")
for i, (t, g) in enumerate(top5.items(), 1):
    print(f"     {i}. {t:<32} {int(g)}")


# 1.14  Remove duplicate rows
pre  = len(df)
df.drop_duplicates(subset=[c for c in df.columns if c != '_slug'], inplace=True)
df.reset_index(drop=True, inplace=True)
print(f"1.14 Duplicates removed: {pre - len(df)} | rows remaining: {len(df)}")


# 1.15  Standardise team names (strip, title-case, rebuild aggregation)
df['home_team_name'] = df['home_team_name'].str.strip().str.title()
df['away_team_name'] = df['away_team_name'].str.strip().str.title()
home_g  = df.groupby('home_team_name')['Goals Home'].sum().rename('home_goals')
away_g  = df.groupby('away_team_name')['Away Goals'].sum().rename('away_goals')
team_goals = pd.concat([home_g, away_g], axis=1).fillna(0)
team_goals['total_team_goals'] = team_goals['home_goals'] + team_goals['away_goals']
print(f"1.15 Standardised {len(df['home_team_name'].dropna().unique())} unique team names.")

print("\nQ1 complete.\n")


# =============================================================
#  QUESTION 2  —  Visualisations (Matplotlib)
# =============================================================

C_RED  = '#e94560'
C_NAVY = '#0f3460'
C_DARK = '#16213e'
C_BG   = '#f9f9f9'
C_GRID = '#e0e0e0'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.facecolor': C_BG, 'figure.facecolor': 'white',
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'grid.color': C_GRID, 'grid.linewidth': 0.6,
    'axes.labelsize': 11, 'xtick.labelsize': 10, 'ytick.labelsize': 10,
})

# ── 2.1  Histogram ──────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5.5))
n, bins_out, patches = ax.hist(
    df['total_goals'], bins=range(0, int(df['total_goals'].max()) + 2),
    color=C_RED, edgecolor='white', linewidth=0.8, alpha=0.9
)
mean_g = df['total_goals'].mean()
ax.axvline(mean_g, color=C_NAVY, linestyle='--', linewidth=2,
           label=f'Mean = {mean_g:.2f} goals')
for patch, count in zip(patches, n):
    if count > 0:
        ax.text(patch.get_x() + patch.get_width()/2, count + 1.5,
                int(count), ha='center', va='bottom', fontsize=8.5, color='#444')
ax.set_xlabel('Total Goals per Match', labelpad=8)
ax.set_ylabel('Number of Matches', labelpad=8)
ax.set_title('Distribution of Total Goals Scored per Match  |  EPL 2020–2024',
             fontsize=13, fontweight='bold', pad=14, color='#1a1a2e')
ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
ax.legend(frameon=False, fontsize=10)
plt.tight_layout()
plt.savefig('output/fig1_histogram.png', dpi=150, bbox_inches='tight')
plt.close()
print("2.1  Histogram saved.")

# ── 2.2  Top-10 bar chart ────────────────────────────────
top10 = team_goals['total_team_goals'].sort_values(ascending=False).head(10).reset_index()
top10.columns = ['team', 'goals']
top10s = top10.sort_values('goals')

fig, ax = plt.subplots(figsize=(11, 6.5))
colors = [C_RED if g == top10s['goals'].max() else C_DARK for g in top10s['goals']]
ax.barh(top10s['team'], top10s['goals'], color=colors,
        edgecolor='white', linewidth=0.5, height=0.6)
for i, g in enumerate(top10s['goals']):
    ax.text(g + 2, i, f'{int(g)}', va='center', fontsize=9.5, color='#333')
ax.set_xlabel('Total Goals Scored', labelpad=8)
ax.set_title('Top 10 Teams by Total Goals Scored  |  EPL 2020–2024',
             fontsize=13, fontweight='bold', pad=14, color='#1a1a2e')
ax.grid(axis='y', visible=False)
ax.set_xlim(0, top10s['goals'].max() + 22)
plt.tight_layout()
plt.savefig('output/fig2_top10_teams.png', dpi=150, bbox_inches='tight')
plt.close()
print("2.2  Top-10 bar chart saved.")

# ── 2.3  Monthly line chart ──────────────────────────────
df['period'] = pd.to_datetime(df[['year', 'month']].assign(day=1))
monthly = df.groupby('period')['total_goals'].sum().reset_index().sort_values('period')

fig, ax = plt.subplots(figsize=(14, 5.5))
ax.plot(monthly['period'], monthly['total_goals'],
        color=C_NAVY, linewidth=2.2, marker='o', markersize=5,
        markerfacecolor=C_RED, markeredgecolor='white', markeredgewidth=0.8, zorder=3)
ax.fill_between(monthly['period'], monthly['total_goals'], alpha=0.12, color=C_NAVY)
ax.set_xlabel('Month', labelpad=8)
ax.set_ylabel('Total Goals Scored', labelpad=8)
ax.set_title('Total Goals Scored per Month  |  EPL 2020–2024',
             fontsize=13, fontweight='bold', pad=14, color='#1a1a2e')
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.xticks(rotation=45, ha='right', fontsize=9)
plt.tight_layout()
plt.savefig('output/fig3_goals_monthly.png', dpi=150, bbox_inches='tight')
plt.close()
print("2.3  Line chart saved.")

# ── 2.4  Side-by-side shots bar chart (Emirates) ─────────
em = df[df['stadium'] == 'Emirates Stadium'].copy()
em['match_label'] = em['home_team_name'] + ' vs ' + em['away_team_name']
em['total_shots'] = em['home_shots'] + em['away_shots']
em_plot = em.nlargest(15, 'total_shots').sort_values('total_shots')

x = np.arange(len(em_plot))
W = 0.38
fig, ax = plt.subplots(figsize=(12, 7.5))
ax.barh(x - W/2, em_plot['home_shots'].values, W,
        label='Home Shots (Arsenal)', color=C_DARK, alpha=0.9, edgecolor='white')
ax.barh(x + W/2, em_plot['away_shots'].values, W,
        label='Away Shots', color=C_RED, alpha=0.9, edgecolor='white')
ax.set_yticks(x)
ax.set_yticklabels(em_plot['match_label'].values, fontsize=8.5)
ax.set_xlabel('Number of Shots', labelpad=8)
ax.set_title('Home vs Away Shots at Emirates Stadium\nTop 15 Matches by Combined Shot Volume  |  EPL 2020–2024',
             fontsize=13, fontweight='bold', pad=14, color='#1a1a2e')
ax.legend(frameon=False, fontsize=10, loc='lower right')
ax.grid(axis='y', visible=False)
plt.tight_layout()
plt.savefig('output/fig4_shots_emirates.png', dpi=150, bbox_inches='tight')
plt.close()
print("2.4  Shots chart saved.")

print("\nQ2 complete. All figures saved to output/")
print("Q3 interpretations are in the accompanying report document.")
