"""
Movie Recommendation System, Wiktor Rostkowski Jan Szenborn, 2023

Overview:
This Python script provides movie recommendations based on user preferences using collaborative filtering and Pearson correlation.

How to Use:

1. Install required libraries:
   - Run the following command to install the necessary libraries:
     ```
     pip install numpy
     ```

2. Prepare your movie ratings dataset:
   - Our application currently has demo ratings from 1 to 13 users, but you can create your own dataset.
   - Create a JSON file, for example, 'anime_ratings.json', containing user movie ratings.
   - Each user should be represented with a unique key, and their ratings should be stored as a dictionary of movies and respective ratings.

   Example dataset structure:
   {
       "user1": {"movie1": 4, "movie2": 3, ...},
       "user2": {"movie1": 5, "movie3": 2, ...},
       ...
   }

   [optional]  if you have problem with json file because you used polish alphabet you should recodejson.py

4. Run the script:
   - Open a terminal and navigate to the script's directory.
   - Execute the following command to get movie recommendations for a specific user:
     ```
     python main.py
     ```
   - You will be prompted to choose your user profile by entering a number from 1 to 13 in the console.
   - For example, if you are user 3, enter '3' and press Enter.
   - The script will generate movie recommendations based on your selected user profile.

5. Explore your movie recommendations:
   - The script will display a list of movie recommendations for the specified user based on users' opinion.


Note:
- Make sure to customize the dataset and file names according to your data.

Enjoy discovering new movies!
"""

import json
import numpy as np


def calculate_pearson_score(dataset, user1, user2):
    '''Calculate the Pearson correlation score between two users'''

    if user1 not in dataset or user2 not in dataset:
        raise ValueError(f"User {user1} or {user2} not found in the dataset")

    # Find common movies
    common_movies = set(dataset[user1].keys()) & set(dataset[user2].keys())

    if not common_movies:
        return 0

    # Define lambda functions for summing user ratings and their squares
    sum_user_ratings = lambda user, movies: np.sum(np.fromiter((dataset[user][movie] for movie in movies), dtype=float))
    sum_user_ratings_squared = lambda user, movies: np.sum(
        np.fromiter((np.square(dataset[user][movie]) for movie in movies), dtype=float))

    # Calculate the necessary sums
    sum_user1_ratings = sum_user_ratings(user1, common_movies)
    sum_user2_ratings = sum_user_ratings(user2, common_movies)
    sum_user1_ratings_squared = sum_user_ratings_squared(user1, common_movies)
    sum_user2_ratings_squared = sum_user_ratings_squared(user2, common_movies)
    sum_of_products = np.sum(
        np.fromiter((dataset[user1][movie] * dataset[user2][movie] for movie in common_movies), dtype=float))

    # Calculate denominators for both users
    denominator_user1 = sum_user1_ratings_squared - np.square(sum_user1_ratings) / len(common_movies)
    denominator_user2 = sum_user2_ratings_squared - np.square(sum_user2_ratings) / len(common_movies)

    # Avoid division by zero
    if denominator_user1 * denominator_user2 == 0:
        return 0

    # Calculate and return the Pearson correlation score
    numerator = sum_of_products - (sum_user1_ratings * sum_user2_ratings / len(common_movies))

    return numerator / np.sqrt(denominator_user1 * denominator_user2)


def generate_movie_recommendations(dataset, input_user):
    '''Generate movie recommendations for the input user'''

    if input_user not in dataset:
        raise ValueError(f"User {input_user} not found in the dataset")

    overall_scores = {}
    similarity_scores = {}

    # Get movies already watched by the input user
    watched_movies = set(dataset[input_user])

    for user in [u for u in dataset if u != input_user]:
        # Calculate Pearson score for each user
        similarity_score = calculate_pearson_score(dataset, input_user, user)

        # Skip users with no similarity
        if similarity_score <= 0:
            continue

        # Find unseen movies for the input user
        unseen_movies = [m for m in dataset[user] if
                         m not in watched_movies and (m not in dataset[input_user] or dataset[input_user][m] == 0)]

        # Calculate overall scores and similarity scores for each unseen movie
        for item in unseen_movies:
            overall_scores[item] = dataset[user][item] * similarity_score
            similarity_scores[item] = similarity_score

    if not overall_scores:
        return ['No recommendations available']

    # Normalize and sort movie scores
    movie_scores = np.array([[score / similarity_scores[item], item] for item, score in overall_scores.items()])
    movie_scores = sorted(movie_scores, key=lambda x: x[0], reverse=True)
    movie_recommendations = [movie for _, movie in movie_scores]

    return movie_recommendations


if __name__ == '__main__':
    user = input("Enter the user: ")

    # Load movie ratings dataset from a file
    ratings_filename = 'output.json'

    with open(ratings_filename, 'r') as file:
        data = json.load(file)

    # Generate and display movie recommendations for the specified user
    print(f"\nMovie suggestions for {user}:")
    recommended_movies = generate_movie_recommendations(data, user)

    for i, movie in enumerate(recommended_movies):
        print(f"{i + 1}. {movie}")
