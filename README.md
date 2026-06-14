# EPL Match Analytics — English Premier League 2020–2024

A data analytics project exploring four seasons of English Premier League match data. The goal was to uncover patterns in team performance, goal-scoring trends, and shot behaviour using Python — and turn raw numbers into visuals that actually tell a story.

---

## What This Project Covers

- Cleaning and preparing a real-world football dataset with mixed date formats, string-encoded numbers, and integer-encoded team IDs
- Engineering new features like total goals, goal difference, and per-team goal tallies
- Identifying the top-performing teams across four seasons
- Building four publication-ready visualisations with Matplotlib

---

## Visuals

### Distribution of Total Goals per Match
![Histogram](output/fig1_histogram.png)

### Top 10 Teams by Total Goals Scored
![Top 10 Teams](output/fig2_top10_teams.png)

### Goals Scored per Month Across All Seasons
![Monthly Goals](output/fig3_goals_monthly.png)

### Home vs Away Shots at Emirates Stadium
![Shots Emirates](output/fig4_shots_emirates.png)

---

## Key Findings

- The average EPL match produces **2.79 goals**, with 2–3 goal games being the most common outcome
- **Manchester City** led all teams with 276 goals over the four-season period, 38 clear of Liverpool in second
- Goal output peaks in **October–November** and again in **March–April**, aligned with fixture congestion and end-of-season pressure
- Arsenal consistently generated **more shots at home** than visiting sides at Emirates Stadium, with the gap widening against defensively-minded opponents

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3 | Core language |
| pandas | Data loading, cleaning, feature engineering |
| Matplotlib | All visualisations |
| NumPy | Numerical operations |
| re (regex) | Date parsing and team name extraction from URLs |

---

## How to Run It Yourself

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/epl-analytics.git
cd epl-analytics
```

**2. Install dependencies**
```bash
pip install pandas matplotlib numpy
```

**3. Add the dataset**

Place `epl_stats.csv` in the root folder (same level as `epl_analysis.py`).

**4. Run the script**
```bash
python epl_analysis.py
```

Charts are saved automatically to the `output/` folder.

---

## Project Structure

```
epl-analytics/
├── epl_analysis.py        # Main analysis script
├── epl_stats.csv          # Dataset (not tracked — add your own copy)
├── output/
│   ├── fig1_histogram.png
│   ├── fig2_top10_teams.png
│   ├── fig3_goals_monthly.png
│   └── fig4_shots_emirates.png
└── README.md
```

---

## Dataset

Match-level statistics from the 2020–2024 EPL seasons sourced via Sky Sports match URLs. Covers 1,140 fixtures across 25 clubs, including goals, shots, possession, passes, corners, fouls, cards, and attendance.

---

## Author

**Zwavhudi Mudogwa**  
Data Analytics | Cloud | IT Support  
📧 mudogwa.zwavhu@gmail.com  
🔗 [linkedin.com/in/zwavhudi-mudogwa5](https://www.linkedin.com/in/zwavhudi-mudogwa5)  
🗂️ [datascienceportfol.io/mudogwazwavhu](https://datascienceportfol.io/mudogwazwavhu)
