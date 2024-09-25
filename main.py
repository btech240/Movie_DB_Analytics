import os
import time

import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key
API_KEY = os.getenv("API_KEY")

# Use TMDb API
BASE_URL = "https://api.themoviedb.org/3"


# Function to get detailed information about a movie, including credits
def get_movie_details(movie_id):
    # Construct the API URL to fetch movie details and append the 'credits' field
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits"
    # Send an HTTP GET request to the API
    response = requests.get(url)
    # Return the JSON response, which contains the movie details
    return response.json()


# Function to fetch a list of movies released in a specific year
def fetch_movies_by_year(year):
    movie_results = []
    page = 1  # Start with page 1
    while True:
        url = (
            f"{BASE_URL}/discover/movie?api_key={API_KEY}&primary_release_year={year}"
            f"&sort_by=popularity.desc&page={page}&certification_country=US&certification.lte=R"
        )
        response = requests.get(url)
        data = response.json()
        results = data.get("results", [])

        if not results:
            break  # If no more results, exit the loop

        movie_results.extend(results)

        if page >= data["total_pages"]:
            break  # Stop if there are no more pages

        page += 1  # Increment to the next page

    return movie_results


# Function to extract the director's name from the movie credits
def get_director(credits):
    # Loop through the 'crew' section of the credits to find the director
    for crew_member in credits["crew"]:
        if crew_member["job"] == "Director":
            return crew_member["name"]  # Return the director's name
    return None  # Return None if no director is found


# Function to extract the producer's name from the movie credits
def get_producer(credits):
    # Loop through the 'crew' section of the credits to find the producer
    for crew_member in credits["crew"]:
        if crew_member["job"] == "Producer":
            return crew_member["name"]  # Return the producer's name
    return None  # Return None if no producer is found


# Main function to fetch movie data for a range of years
def fetch_movie_data(year_range):
    movie_data = []  # List to store movie data

    # Loop over each year in the provided range
    for year in year_range:
        print(f"Fetching movies from {year}...")
        # Fetch movies released in the current year
        movies = fetch_movies_by_year(year)

        # Loop over each movie returned for that year
        for movie in movies:
            # Fetch detailed information about the movie, including credits
            movie_details = get_movie_details(movie["id"])
            credits = movie_details.get("credits", {})  # Get the credits information

            # Append the movie data to the list as a dictionary
            print(movie_details.get("title"))
            movie_data.append(
                {
                    "Title": movie_details.get("title"),  # Movie title
                    "Year": movie_details.get("release_date", "").split("-")[
                        0
                    ],  # Year of release
                    "Director": get_director(credits),  # Director's name
                    "Producer": get_producer(credits),  # Producer's name
                    "Genres": ", ".join(
                        [genre["name"] for genre in movie_details.get("genres", [])]
                    ),  # List of genres
                    "Summary": movie_details.get("overview"),  # Movie summary
                    "Duration": movie_details.get(
                        "runtime"
                    ),  # Movie duration in minutes
                    "Budget": movie_details.get("budget"),  # Movie budget
                    "Revenue": movie_details.get("revenue"),  # Movie revenue
                    "Ratings": movie_details.get(
                        "vote_average"
                    ),  # Average viewer rating
                    "Content Rating": movie_details.get(
                        "adult"
                    ),  # 'True' if adult content
                    "Movie ID": movie["id"],  # Movie ID
                }
            )

        # Add a delay of 1 second to avoid hitting the API rate limit
        time.sleep(1)

    # Return the list of movie data
    return movie_data


# Define the range of years (from 1964 to 2023) to fetch movie data for
year_range = range(2021, 2022)

# Fetch the movie data for the specified range of years
movies = fetch_movie_data(year_range)

# Convert the movie data list into a pandas DataFrame for easy data handling and storing to DB
df = pd.DataFrame(movies)

# Save the DataFrame to a CSV file
df.to_csv("movie_data.csv", index=False)
print("Data saved to movie_data.csv")
