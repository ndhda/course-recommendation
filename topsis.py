import numpy as np
import pandas as pd

def topsis(data, weights, impacts):
    # Normalize the decision matrix
    norm_data = data / np.sqrt((data**2).sum(axis=0))

    # Multiply by weights
    weighted_data = norm_data * weights

    # Calculate ideal best and worst
    ideal_best = np.max(weighted_data, axis=0) * impacts
    ideal_worst = np.min(weighted_data, axis=0) * impacts

    # Calculate distances to ideal best and worst
    dist_best = np.sqrt(((weighted_data - ideal_best)**2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_data - ideal_worst)**2).sum(axis=1))

    # Calculate performance score
    scores = dist_worst / (dist_best + dist_worst)
    return scores

def rank_courses(courses, difficulty, time, type_):
    weights = np.array([1, 1, 1])  # Equal weights for simplicity
    impacts = np.array([1, 1, 1])  # All criteria are beneficial

    # Filter courses based on user selection
    filtered_courses = courses[
        (courses['course_difficulty'] == difficulty) &
        (courses['course_time'] == time) &
        (courses['course_type'] == type_)
    ]

    # If no courses match, return empty DataFrame
    if filtered_courses.empty:
        return pd.DataFrame()

    # Apply TOPSIS
    data = filtered_courses[['course_rating', 'course_students_enrolled', 'reviews']].astype(float).values
    scores = topsis(data, weights, impacts)

    # Add scores to the dataframe
    filtered_courses['score'] = scores
    ranked_courses = filtered_courses.sort_values(by='score', ascending=False)

    return ranked_courses
