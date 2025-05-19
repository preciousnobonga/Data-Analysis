import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
from time import sleep
from random import randint
from dotenv import load_dotenv
from matplotlib.backends.backend_pdf import PdfPages
from data_cleaner import clean_job_data, analyze_job_data, save_to_csv
from data_visualizer import visualize_insights
from report_generator import generate_pdf_report

# Load environments from .env file
load_dotenv()


RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST,
    "Content-Type": "application/json"
}

def create_launch_json():
    """
    Create a launch.json file in the .vscode directory to configure VS Code debugging.
    """
    vscode_dir = os.path.join(os.getcwd(), ".vscode")
    if not os.path.exists(vscode_dir):
        os.makedirs(vscode_dir)
    
    launch_json_path = os.path.join(vscode_dir, "launch.json")
    config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Run Job Scraper",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/main.py",
                "console": "integratedTerminal",
                "envFile": "${workspaceFolder}/.env"
            }
        ]
    }
    with open(launch_json_path, "w") as f:
        json.dump(config, f, indent=4)
    print(f"launch.json created at {launch_json_path}")


def fetch_linkedin_jobs(search_term, location, num_pages=1):
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
            sleep(randint(1, 3))   # Avoid API rate limiting

        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page + 1}: {e}")

    return jobs

def filter_jobs(df, employment_type, location_type):
    if employment_type:
        df = df[df['employmentType'].str.lower() == employment_type.lower()]
    if location_type:
        df = df[df['locationType'].str.lower() == location_type.lower()]
    return df

def generate_pdf_report(df, analysis_results, pdf_path="job_market_insights.pdf"):
    with PdfPages(pdf_path) as pdf:
        plt.figure(figsize=(10, 6))
        analysis_results['top_skills'].plot(kind='barh', color='skyblue')
        plt.title("Top 20 Most Demanded Skills")
        plt.xlabel("Number of Job Postings")
        plt.gca().invert_yaxis()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(10, 6))
        analysis_results['top_locations'].plot(kind='bar', color='lightgreen')
        plt.title("Top 10 Locations with Most Job Postings")
        plt.xticks(rotation=45)
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(10, 6))
        analysis_results['top_companies'].plot(kind='barh', color='orange')
        plt.title("Top 10 Companies Hiring")
        plt.xlabel("Number of Job Postings")
        plt.gca().invert_yaxis()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(10, 6))
        analysis_results['skill_salary'].sort_values().plot(kind='bar', color='purple')
        plt.title("Average Job Count by Top Skills")
        plt.xlabel("Skill")
        plt.ylabel("Average Job Count")
        plt.xticks(rotation=45)
        pdf.savefig()
        plt.close()

def main():

    # Create the launch.json file (if needed)
    create_launch_json()

    search_term = input("Enter job title to search (e.g., 'Data Scientist'): ")
    location = input("Enter location (e.g., 'Johannesburg' or 'Cape Town'): ")
    num_pages = int(input("Enter number of pages to fetch: "))
    employment_type = input("Filter by Employment Type (optional, e.g., 'Full-time'): ")
    location_type = input("Filter by Location Type (optional: Remote, On-site, Hybrid): ")

    print("\nFetching LinkedIn job listings...")
    jobs = fetch_linkedin_jobs(search_term, location, num_pages)

    if not jobs:
        print("No jobs found or an error occurred.")
        return

    print("\nCleaning and structuring data...")
    df = clean_job_data(jobs)

    if employment_type or location_type:
        df = filter_jobs(df, employment_type, location_type)

    print("\nAnalyzing data...")
    analysis_results = analyze_job_data(df)

    print("\nGenerating Visualizations...")
    visualize_insights(df, analysis_results)

    print("\nSaving data to CSV and PDF...")
    save_to_csv(df)
    generate_pdf_report(df, analysis_results)

    print("\nAnalysis complete! Check 'job_market_insights.png', 'job_market_insights.pdf', and 'job_listings.csv'.")
    print("\nSamples of collected data: ")
    print(df.head())

if __name__ == "__main__":
    main()
