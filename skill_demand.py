import pandas as pd
import requests
import time
from sample import APP_ID, APP_KEY, url_base
job_titles = [
    "software engineer",
    "data engineer",
    "data scientist",
    "machine learning engineer",
    "backend developer"
]
locations = [
    "New York",
    "San Francisco",
    "Seattle",
    "Austin",
    "Boston"
]
skills = [
    "python", "sql", "aws", "docker", "kubernetes",
    "spark", "java", "pytorch", "tensorflow", "golang"
]
results = []
for title in job_titles:
    for skill in skills:
        total_count = 0

        for location in locations:
            params = {
                "app_id":           APP_ID,
                "app_key":          APP_KEY,
                "what":             f"{title} {skill}",
                "where":            location,
                "results_per_page": 1
            }
            response = requests.get(url_base, params=params)
            if response.status_code != 200:
                print(f"Error {response.status_code} — {title} + {skill} + {location}")
                time.sleep(5)
                continue
            data = response.json()
            count = data.get("count", 0)  #total matching jobs Adzuna has
            total_count += count
            print(f"  {title} + {skill} + {location}: {count} listings")
            time.sleep(0.5) 
        results.append({
            "role":        title,
            "skill":       skill,
            "total_count": total_count
        })
        print(f"→ {title} + {skill}: {total_count} total across all cities\n")
df = pd.DataFrame(results)
df.to_csv("skill_demand.csv", index=False)
pivot = df.pivot(index="skill", columns="role", values="total_count")
pivot = pivot.div(pivot.sum(axis=0), axis=1).round(3) * 100  # normalize to % per role
print("\n=== Skill demand by role (% of listings mentioning skill) ===")
print(pivot.to_string())
pivot.to_csv("skill_demand_pivot.csv")
print("\nSaved skill_demand.csv and skill_demand_pivot.csv")
