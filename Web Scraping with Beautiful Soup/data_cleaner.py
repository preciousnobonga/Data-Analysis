import pandas as pd
import matplotlib.pyplot as plt

def clean_job_data(jobs):
    """Clean and structure the scraped job data."""
    df = pd.DataFrame(jobs)

    # Remove duplicate jobs based on title and company
    df = df.drop_duplicates(subset=['title', 'company'])

    # Common skills to extract
    common_skills = [
        'python', 'java', 'sql', 'javascript', 'c++', 'c#', 'r', 'ruby', 'php', 'swift',
        'machine learning', 'ai', 'artificial intelligence', 'deep learning',
        'data analysis', 'data science', 'big data', 'hadoop', 'spark',
        'tableau', 'power bi', 'excel', 'aws', 'azure', 'google cloud', 'docker', 'kubernetes',
        'linux', 'git', 'agile', 'scrum', 'devops', 'ci/cd', 'rest api', 'graphql',
        'tensorflow', 'pytorch', 'keras', 'numpy', 'pandas', 'django', 'flask', 'react',
        'angular', 'vue', 'node.js', 'typescript', 'html', 'css', 'sass', 'nosql',
        'mongodb', 'postgresql', 'mysql', 'oracle', 'redis', 'elasticsearch'
    ]

    def extract_skills(text):
        if not text or pd.isna(text):
            return []
        text = text.lower()
        return list({skill for skill in common_skills if skill in text})

    # Combine skills from title and description
    df['skills'] = df.apply(
        lambda row: list(set(extract_skills(row.get('title', '')) + extract_skills(row.get('description', '')))),
        axis=1
    )

    def clean_location(loc):
        if not loc or pd.isna(loc):
            return None
        if 'remote in' in loc.lower():
            return loc.replace('Remote in', '').strip()
        return loc.strip()

    df['location'] = df['location'].apply(clean_location)

    return df


def analyze_job_data(df):
    """Analyze the cleaned job data and generate insights."""
    analysis_results = {}

    # Count top skills
    all_skills = [skill for sublist in df['skills'] for skill in sublist]
    skills_count = pd.Series(all_skills).value_counts().head(20)
    analysis_results['top_skills'] = skills_count

    # Top locations
    top_locations = df['location'].value_counts().head(10)
    analysis_results['top_locations'] = top_locations

    # Top companies
    top_companies = df['company'].value_counts().head(10)
    analysis_results['top_companies'] = top_companies

    return analysis_results


def save_to_csv(df, fileName='job_listings.csv'):
    """Save the cleaned job data to a CSV file."""
    df.to_csv(fileName, index=False)
    print(f"Data saved to {fileName}")
