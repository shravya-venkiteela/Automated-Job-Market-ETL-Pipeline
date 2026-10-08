# Automated Job Market ETL Pipeline

An ETL pipeline that turns 16,000+ job listings into a picture of which technical skills employers ask for, by role.

🔗 [View Tableau Dashboard](https://public.tableau.com/app/profile/shravya.venkiteela/viz/TechJobMarketAnalysis_17732511769710/JobMarketDashboard)

<img width="1592" height="741" alt="Screenshot 2026-03-11 134401" src="https://github.com/user-attachments/assets/e0f162b4-e818-40a6-ae1a-41a8e9e9da12" />
[Dashboard Preview]



## Overview

An ETL pipeline that collects 16,000+ real job listings from the Adzuna REST API, cleans them, and loads them into MySQL to answer one question: which technical skills do employers ask for, by role?

It covers 5 roles (software engineer, data engineer, data scientist, machine learning engineer, backend developer) across 5 US cities (New York, San Francisco, Seattle, Austin, Boston).

---

## What each script does

| Script | Step |
|---|---|
| `sample.py` | **Extract.** Pulls up to 20 pages of 100 listings per role and city from the Adzuna API and saves the raw JSON. Retries only errors that can succeed later (429 and 5xx) with exponential backoff and `Retry-After`; fails fast on others, such as 401 for a bad key. |
| `useful_field.py` | **Transform.** Flattens the nested JSON, removes duplicates and listings without salary, normalizes job titles into role categories with regex, and flags 10 skills (Python, SQL, AWS, Docker, Kubernetes, Spark, Java, PyTorch, TensorFlow, Go) mentioned in each description. |
| `sql_implement.py` | **Load.** Creates a normalized MySQL schema (`jobs`, `companies`, `locations`, with foreign keys) via SQLAlchemy and loads the cleaned data. |
| `skill_demand.py` | **Skill demand.** Queries Adzuna's total listing counts for each role, skill and city (250 queries) and writes the share of skill mentions per role to `skill_demand_pivot.csv`. |
| `pipeline_run.py` | **Runner.** Runs the transform and load steps as subprocesses, checks each exit code, and writes timestamped logs to `pipeline_log.txt`, so a failing step stops the run and points to the error. |

## Key finding

AWS accounts for 61% of the skill mentions in Machine Learning Engineer listings, the highest share of any skill for any role in the sample (see `skill_demand_pivot.csv`).

## How to Run

1. Clone the repo
2. Install dependencies:
```bash
   pip install requests pandas sqlalchemy mysql-connector-python
```
3. Add your Adzuna API credentials to `sample.py` (never commit real keys)
4. Add your MySQL connection details to `sql_implement.py`, and create the database:
```sql
   CREATE DATABASE job_market;
```
5. Collect the raw data:
```bash
   python sample.py
```
6. Run the transform and load steps:
```bash
   python pipeline_run.py
```
7. Optional, for the skill-demand table:
```bash
   python skill_demand.py
```

## Limitations

- Skills are detected by keyword match in the description Adzuna returns, which is often truncated, so counts understate real demand.
- Data is a single snapshot; there is no trend tracking over time yet.
- Credentials are set in source files; environment variables would be safer.
