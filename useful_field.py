import json
import pandas as pd
import re
with open("jobs_dataset_large.json") as f:
    jobs = json.load(f)
rows = []
for job in jobs:
    rows.append({
        "title": job.get("title"),
        "searched_title": job.get("_searched_title"),
        "searched_location": job.get("_searched_location"),
        "company": job.get("company", {}).get("display_name"),
        "location": job.get("location", {}).get("display_name"),
        "latitude": job.get("latitude"),
        "salary_min": job.get("salary_min"),
        "salary_max": job.get("salary_max"),
        "salary_predicted": job.get("salary_is_predicted"),
        "contract_time": job.get("contract_time"),
        "description": job.get("description"),
        "created": job.get("created")
    })

df = pd.DataFrame(rows)
df = df.drop_duplicates(subset=["title","company","location","created"])
df = df.dropna(subset=["salary_min","salary_max"])
df["avg_salary"] = (df["salary_min"] + df["salary_max"]) / 2
df["created"] = pd.to_datetime(df["created"])
role_patterns = {
    "Software Engineer":         r"software engineer|software developer|swe\b|full.?stack|platform engineer|senior engineer|staff engineer|principal engineer|systems engineer",
    "Data Engineer":             r"data engineer|etl engineer|analytics engineer|data infrastructure|data platform",
    "Data Scientist":            r"data scientist|data analyst|research scientist|quantitative analyst|quant\b",
    "Machine Learning Engineer": r"machine learning|ml engineer|ai engineer|deep learning|mlops|research engineer",
    "Backend Developer":         r"backend developer|back.end developer|backend engineer|api engineer|server.side",
}
def normalize_title(raw_title):
    if pd.isna(raw_title):
        return "Other"
    t = raw_title.lower()
    for role, pattern in role_patterns.items():
        if re.search(pattern, t):
            return role
    return "Other"
df["role_category"] = df["title"].apply(normalize_title)
mask = df["role_category"] != "Other"
df.loc[mask, 'role_category'] = df.loc[mask, 'searched_title'].str.title().fillna("Other")
skills = {
    "python": r"\bpython\b",
    "sql": r"\bsql\b",
    "aws": r"\baws\b",
    "docker": r"\bdocker\b|\bdockerized\b|\bcontainers?\b",
    "kubernetes": r"\bkubernetes\b",
    "spark": r"\bspark\b",
    "java": r"\bjava\b",
    "pytorch": r"\bpytorch\b",
    "tensorflow": r"\btensorflow\b",
    "go": r"\bgolang\b|\bgo language\b"
}
desc = df["description"].str.lower().fillna("")
print(df["description"].str.len().describe())
for skill, pattern in skills.items():
    df[skill] = desc.str.contains(pattern, regex=True)

print("\n=== Job counts per role ===")
print(df["role_category"].value_counts())

print("\n=== Average salary by role ===")
print(df.groupby("role_category")["avg_salary"].mean().sort_values(ascending=False).round(0))

print("\n=== Top skills per role ===")
skills_cols = list(skills.keys())
print(df.groupby("role_category")[skills_cols].mean().round(2).T)

print("\n=== Top hiring companies per role ===")
for role in df["role_category"].unique():
    subset = df[df["role_category"] == role]
    print(f"\n{role}:")
    print(subset["company"].value_counts().head(5))
df.to_csv("clean_jobs.csv", index=False)
print("\nSaved to clean_jobs.csv")