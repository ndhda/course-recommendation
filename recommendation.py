import pandas as pd
from topsis import rank_courses

def get_recommendations(course_difficulty, course_time, course_type):
    # Load the dataset (if not loaded globally)
    df = pd.read_csv('data/coursera_courses.csv')
    
    # Rank courses based on user preferences
    recommendations = rank_courses(df, course_difficulty, course_time, course_type)
    
    return recommendations
