# Automated Job Market ETL Pipeline

An end-to-end data pipeline that collects, transforms, and analyzes US tech job market data 
using the Adzuna API, stores it in MySQL, and visualizes insights in Tableau.

🔗 [View Tableau Dashboard](https://public.tableau.com/app/profile/shravya.venkiteela/viz/TechJobMarketAnalysis_17732511769710/JobMarketDashboard)
<img width="1592" height="741" alt="Screenshot 2026-03-11 134401" src="https://github.com/user-attachments/assets/e0f162b4-e818-40a6-ae1a-41a8e9e9da12" />
<img width="1592" height="741" alt="Screenshot 2026-03-11 134401" src="https://github.com/user-attachments/assets/e0f162b4-e818-40a6-ae1a-41a8e9e9da12" />
[Dashboard Preview]



## Overview
This pipeline extracts 16,000+ job listings across 5 roles and 5 cities, classifies raw job 
titles using regex normalization, loads the cleaned data into a normalized MySQL database, and 
measures real skill demand via targeted API queries.

---

## ETL Pipeline

**Extract** — `sample.py`
- Collected 16,000+ listings via Adzuna API using Python
- Handled pagination across 20 pages per title × city combination
- Tagged each record with search context for downstream classification

**Transform** — `useful_field.py`
- Removed duplicate listings
- Cleaned and normalized salary fields
- Classified raw job titles into 5 role categories using regex
- Extracted 10 technical skills from job descriptions

**Load** — `sql_implement.py`
- Designed normalized MySQL schema across 3 tables
- Loaded 13,338 records using SQLAlchemy with foreign key constraints

**Orchestrate** — `pipeline_run.py`
- Master script that chains all pipeline steps
- Logs each run to `pipeline_log.txt` with timestamps

## Key Findings
- ML Engineer roles average **$190,070/year** — highest of all roles
- **AWS** is required in **61%** of ML Engineer listings
- **Python** is the top skill in 4 of 5 roles
- **Software Engineer** has the most listings (4,724) across all cities
- **Amazon** is the top hiring company for Data Engineer roles

---

## How to Run
1. Clone the repo
2. Install dependencies:
```bash
   pip install requests pandas sqlalchemy mysql-connector-python
```
3. Add your Adzuna API credentials to `sample.py`
4. Create MySQL database:
```sql
   CREATE DATABASE job_market;
```
5. Run the full pipeline:
```bash
   python pipeline_run.py
```
