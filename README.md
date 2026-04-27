# Job Market & Skill Demand Forecasting Engine

A data science system that identifies high-impact technical skills to learn by analyzing real-time job market demand, salary signals, and emerging role clusters.

🔗 [View Tableau Dashboard](https://public.tableau.com/app/profile/shravya.venkiteela/viz/TechJobMarketAnalysis_17732511769710/JobMarketDashboard)

<img width="1592" height="741" alt="Screenshot 2026-03-11 134401" src="https://github.com/user-attachments/assets/e0f162b4-e818-40a6-ae1a-41a8e9e9da12" />
[Dashboard Preview]



## Overview

This project transforms raw job postings into a decision-making system for skill prioritization.

Using 16,000+ real-world job listings across multiple roles and cities, it combines data engineering, machine learning, and analytics to uncover:

Which skills are most in demand
Which skills command higher salaries
How roles cluster based on real-world job descriptions
What skills are worth learning next
---

## System Capabilities
### 1. Data Collection:
Aggregates 16,000+ job listings across 5 roles and 5 US cities using the Adzuna API
### 2. Skill Demand Modeling:
Ranks skills using a Skill Importance Score based on:
demand frequency
salary weighting
(extendable to growth trends)
### 3. NLP-Based Job Segmentation
Uses TF-IDF and K-Means Clustering to identify hidden job market segments beyond rule-based classification
### 4. Recommendation Engine
Outputs ranked skill recommendations with confidence levels based on data coverage
### 5. Time-Series Tracking (in progress)
Captures periodic snapshots to enable trend analysis and forecasting of skill demand

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
