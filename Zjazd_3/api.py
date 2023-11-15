import requests

API_KEY = 'dd494be1'  # super secret


def get_movie_details(title):
    endpoint = f'http://www.omdbapi.com/?t={title}&apikey={API_KEY}'

    try:
        response = requests.get(endpoint)
        response.raise_for_status()

        # Parse the JSON response
        movie_details = response.json()

        # Check if the response contains an error and skip if any
        if 'Error' in movie_details:
            return None

        return movie_details
    except requests.exceptions.RequestException:
        return None
