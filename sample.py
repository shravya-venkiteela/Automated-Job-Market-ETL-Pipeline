import requests
import json
import time
APP_ID = "your_app_id_here"
APP_KEY = "your_app_key_here"
url_base = "https://api.adzuna.com/v1/api/jobs/us/search"

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
all_jobs = []
for title in job_titles:
    for location in locations:
        page = 1
        while page <= 20:
            params = {
                "app_id": APP_ID,
                "app_key": APP_KEY,
                "what": title,
                "where": location,
                "results_per_page": 100
            }

            url = f"{url_base}/{page}"
            response = requests.get(url, params=params)

            if response.status_code != 200:
                 print("Status:", response.status_code, "Retrying...")
                 time.sleep(5)
                 continue

            data = response.json()
            results = data["results"]

            if not results:
                break
            for job in results:
                job["_searched_title"] = title
                job["_searched_location"] = location
            all_jobs.extend(results)
            print(f"[{title} | {location}] Page {page} -> Total collected: {len(all_jobs)}")
            page += 1
            time.sleep(1)
with open("jobs_dataset_large.json", "w") as f:
    json.dump(all_jobs, f)