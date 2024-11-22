"""
authors: Łukasz Reinke
emails: s15037@pjwstk.edu.pl

Żeby uruchomić program trzeba zainstalować

pip install bs4
pip install numpy
pip install scipy
pip install scikit-learn
pip install urllib3
"""

import json
import numpy as np

from compute_scores import cosing_score, euclidean_score

# Implementacja obu funkcji wygląda podobnie
# Finds users in the dataset that are similar to the input user
def find_similar_users(dataset, user, num_users):
    if user not in dataset:
        raise TypeError('Cannot find ' + user + ' in the dataset')

    # Compute Pearson score between input user
    # and all the users in the dataset
    scores = np.array([[x, euclidean_score(dataset, user,
            x)] for x in dataset if x != user])

    # Sort the scores in decreasing order
    scores_sorted_desc = np.argsort(scores[:, 1])[::-1]
    scores_sorted_asc = np.argsort(scores[:, 1])[::1]

    # Extract the top 'num_users' scores
    top_users = scores_sorted_desc[:num_users]
    bottom_users =  scores_sorted_asc[:num_users]
    scores_both = {}
    scores_both["top_users"] = scores[top_users]
    scores_both["bottom_users"] = scores[bottom_users]
    return scores_both



# Suggest 5 movies to watch and 5 movies to avoid for a specific user
def recommend_movies(dataset, user):
    if user not in dataset:
        raise ValueError(f"User '{user}' not found in the dataset")

    # Find similar users based on euclidean and cosine scores
    similar_users = find_similar_users(dataset, user, 5)
    top_similar_user = similar_users["top_users"][0][0]

    movies_of_similar_user = dataset[top_similar_user]
    movies_of_user = dataset[user]

    # Get movies not watched by the user
    movies_to_consider = {movie: rating for movie, rating in movies_of_similar_user.items()
                          if movie not in movies_of_user}

    # Sort movies by rating
    sorted_movies = sorted(movies_to_consider.items(), key=lambda x: x[1], reverse=True)

    # Get top 5 recommendations and bottom 5 anti-recommendations
    top_5_recommendations = sorted_movies[:5]
    bottom_5_anti_recommendations = sorted_movies[-5:][::-1]

    return top_5_recommendations, bottom_5_anti_recommendations

if __name__ == '__main__':
    ratings_file = 'dataset.json'
    with open(ratings_file, 'r') as f:
        data = json.loads(f.read())

    user = input("Enter the user name: ")

    try:
        recommendations, anti_recommendations = recommend_movies(data, user)

        print("\nTop 5 recommended movies for", user)
        print("-" * 40)
        for movie, rating in recommendations:
            print(f"{movie}: {rating}")

        print("\nTop 5 movies to avoid for", user)
        print("-" * 40)
        for movie, rating in anti_recommendations:
            print(f"{movie}: {rating}")

    except ValueError as e:
        print(e)
