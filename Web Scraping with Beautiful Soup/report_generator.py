# report_generator.py
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def generate_pdf_report(df, analysis_results, output_dir="reports"):
    """Generate a PDF report with visualizations."""
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "job_market_insights.pdf")

    required_keys = ["top_skills", "top_locations", "top_companies", "skill_salary"]
    if not all(key in analysis_results for key in required_keys):
        raise KeyError(f"Missing required keys in analysis_results: {required_keys}")

    with PdfPages(pdf_path) as pdf:
        # Plot 1: Top Skills
        plt.figure(figsize=(10, 6))
        analysis_results["top_skills"].plot(kind="barh", color="skyblue")
        plt.title("Top 20 Most Demanded Skills")
        plt.xlabel("Number of Job Postings")
        plt.gca().invert_yaxis()
        pdf.savefig()
        plt.close()

        # Plot 2: Top Locations
        plt.figure(figsize=(10, 6))
        analysis_results["top_locations"].plot(kind="bar", color="lightgreen")
        plt.title("Top 10 Locations with Most Job Postings")
        plt.xticks(rotation=45)
        pdf.savefig()
        plt.close()

        # Plot 3: Top Companies
        plt.figure(figsize=(10, 6))
        analysis_results["top_companies"].plot(kind="barh", color="orange")
        plt.title("Top 10 Companies Hiring")
        plt.xlabel("Number of Job Postings")
        plt.gca().invert_yaxis()
        pdf.savefig()
        plt.close()

        # Plot 4: Skill vs. Job Count
        plt.figure(figsize=(10, 6))
        analysis_results["skill_salary"].sort_values().plot(kind="bar", color="purple")
        plt.title("Average Job Count by Top Skills")
        plt.xlabel("Skill")
        plt.ylabel("Average Job Count")
        plt.xticks(rotation=45)
        pdf.savefig()
        plt.close()

    return pdf_path  # Return path for logging