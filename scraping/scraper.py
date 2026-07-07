import requests
import pandas as pd

# RemoteOK API
url = "https://remoteok.com/api"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)

# JSON data
data = response.json()

# Remove metadata (first record)
jobs = data[1:]

job_list = []

for job in jobs:
    job_list.append({
        "Job Title": job.get("position"),
        "Company": job.get("company"),
        "Location": job.get("location"),
        "Skills": ", ".join(job.get("tags", [])),
        "Salary Min": job.get("salary_min"),
        "Salary Max": job.get("salary_max"),
        "Posted Date": job.get("date"),
        "Apply URL": job.get("apply_url"),
        "Description": job.get("description")
    })

# Create DataFrame
df = pd.DataFrame(job_list)

# Save CSV
df.to_csv("data/raw_jobs.csv", index=False)

print("\nDataset Saved Successfully!")
print("Total Jobs:", len(df))

print("\nFirst 5 Records:")
print(df.head())