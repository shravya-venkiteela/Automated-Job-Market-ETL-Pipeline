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
MAX_RETRIES = 4
RETRYABLE = {429, 500, 502, 503, 504}


def get_with_retry(url, params):
    """GET with retries only for errors that can succeed later.

    429 and 5xx are retried with exponential backoff (honouring Retry-After).
    Other errors, such as 401 for a bad API key or 404, fail fast: retrying
    them can never succeed.
    """
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = requests.get(url, params=params, timeout=30)
        except requests.RequestException as e:
            print(f"Network error: {e}")
            response = None
        if response is not None and response.status_code == 200:
            return response
        if response is not None and response.status_code not in RETRYABLE:
            print(f"Status {response.status_code}, not retrying: {response.text[:200]}")
            return None
        if attempt == MAX_RETRIES:
            break
        retry_after = response.headers.get("Retry-After") if response is not None else None
        wait = int(retry_after) if retry_after and retry_after.isdigit() else 2 ** attempt
        print(f"Retrying in {wait}s (attempt {attempt + 1} of {MAX_RETRIES})...")
        time.sleep(wait)
    print(f"Giving up on {url} after {MAX_RETRIES} retries")
    return None


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
            response = get_with_retry(url, params)
            if response is None:
                break  # give up on this title/location, keep the rest of the run

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