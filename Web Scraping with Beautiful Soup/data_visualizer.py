import matplotlib.pyplot as plt
import seaborn as sns

def visualize_insights(df, analysis_results):
    plt.figure(figsize=(15, 20))
    
    # Top 20 Most Demanded Skills
    plt.subplot(3, 2, 1)
    analysis_results['top_skills'].plot(kind='barh', color='skyblue')
    plt.title('Top 20 Most Demanded Skills')
    plt.xlabel('Number of Job Postings')
    plt.gca().invert_yaxis()
    
    # Top 10 Locations with Most Job Postings
    plt.subplot(3, 2, 2)
    analysis_results['top_locations'].plot(kind='bar', color='lightgreen')
    plt.title('Top 10 Locations with Most Job Postings')
    plt.xlabel('Location')
    plt.ylabel('Number of Jobs')
    plt.xticks(rotation=45)

    # Top 10 Companies Hiring
    plt.subplot(3, 2, 3)
    analysis_results['top_companies'].plot(kind='barh', color='gold')
    plt.title('Top 10 Companies Hiring')
    plt.xlabel('Number of Job Postings')
    plt.gca().invert_yaxis()

    # Job Titles Distribution (from raw df)
    plt.subplot(3, 2, 4)
    df['title'].value_counts().head(10).plot(kind='barh', color='purple')
    plt.title('Top 10 Job Titles Distribution')
    plt.xlabel('Number of Jobs')
    plt.gca().invert_yaxis()

    # Skill Salary Comparison (if available)
    if 'skill_salary' in analysis_results:
        plt.subplot(3, 2, 5)
        analysis_results['skill_salary'].sort_values().plot(kind='barh', color='coral')
        plt.title('Average Salary by Top 10 Skills')
        plt.xlabel('Average Yearly Salary')
        plt.gca().invert_yaxis()

    plt.tight_layout()
    plt.savefig('job_market_insights.png')
    plt.show()
