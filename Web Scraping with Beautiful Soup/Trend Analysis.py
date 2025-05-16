import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load environments from .env file
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST,
    "Content-Type": "application/json"
}

def fetch_linkedin_jobs(search_term, location, num_pages=1):
 # Fetch job listings from LinkedIn Jobs via RapidAPI

    base_url = f"https://{RAPIDAPI_HOST}/search"
    jobs = []

    for page in range(num_pages):
        querystring = {
            "query": search_term,
            "location": location,
            "page": str(page + 1)
        }

        try:
            response = requests.get(base_url, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()

            for job in data.get('jobs', []):
                job_info = {
                    'title': job.get('title'),
                    'company': job.get('companyName'),
                    'location': job.get('location'),
                    'locationType': job.get('locationType'),
                    'employmentType': job.get('employmentType'),
                    'description': job.get('description'),
                    'skills': job.get('skills'),
                    'link': job.get('jobUrl'),
                }
                jobs.append(job_info)
        except requests.exceptions.RequestException as e:
            print(f"API request error: (e)")
            break

    return jobs

def main():
    search_term = input("Enter job title to search (e.g., 'Data Scientist): ")
    location = input("Enter location (e.g., 'Johannesburg' or 'Remote'): ")
    num_pages = int(input("Enter number of pages to fetch: "))

    print("\nFetching LinkedIn job listings...")
    jobs = fetch_linkedin_jobs(search_term, location, num_pages)

    if not jobs:
        print("No jobs found or an error occured.")
        return
    
    df = pd.DataFrame(jobs)
    print(df.head())

    
            

 