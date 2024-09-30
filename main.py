import os
import time

import ftfy  # Import FTFY library to clean text
import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key
API_KEY = os.getenv("API_KEY")

# Ensure the API key is not None
if not API_KEY:
    raise ValueError("API key not found. Make sure it is set in the .env file.")

# Use TMDb API
BASE_URL = "https://api.themoviedb.org/3"


# Function to handle rate limiting
def handle_rate_limiting(response):
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 1))
        print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
        time.sleep(retry_after)
        return True
    return False


# Function to get detailed information about a movie, including credits
def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits"
    while True:
        try:
            response = requests.get(url)
            if handle_rate_limiting(response):
                continue
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching movie details for ID {movie_id}: {e}")
            return {}


# Function to fetch a list of movies released in a specific year
def fetch_movies_by_year(year):
    movie_results = []
    page = 1
    while True:
        try:
            url = (
                f"{BASE_URL}/discover/movie?api_key={API_KEY}&primary_release_year={year}"
                f"&sort_by=popularity.desc&page={page}&certification_country=US&certification.lte=R"
            )
            response = requests.get(url)
            if handle_rate_limiting(response):
                continue
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])

            if not results:
                break  # If no more results, exit the loop

            movie_results.extend(results)

            if page >= data["total_pages"]:
                break  # Stop if there are no more pages

            page += 1  # Increment to the next page
        except requests.exceptions.RequestException as e:
            print(f"Error fetching movies for year {year}: {e}")
            break

    return movie_results


# Function to extract the director's name from the movie credits
def get_director(credits):
    if "crew" in credits:
        for crew_member in credits["crew"]:
            if crew_member["job"] == "Director":
                return crew_member["name"]
    return None


# Function to extract the producer's name from the movie credits
def get_producer(credits):
    if "crew" in credits:
        for crew_member in credits["crew"]:
            if crew_member["job"] == "Producer":
                return crew_member["name"]
    return None


# Function to fetch content ratings
def get_movie_content_rating(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/release_dates?api_key={API_KEY}"
    while True:
        try:
            response = requests.get(url)
            if handle_rate_limiting(response):
                continue
            response.raise_for_status()
            release_data = response.json()

            # Look for US certification (or change this to your preferred country)
            for entry in release_data.get("results", []):
                if entry["iso_3166_1"] in [
                    "US",
                    "GB",
                    "CA",
                ]:  # Adjust country codes as needed
                    for release in entry["release_dates"]:
                        if "certification" in release and release["certification"]:
                            return release[
                                "certification"
                            ]  # Return the first available rating
            return None  # Return None if no certification is found
        except requests.exceptions.RequestException as e:
            print(f"Error fetching content rating for movie ID {movie_id}: {e}")
            return None


# Function to clean text using FTFY
def clean_text(text):
    return ftfy.fix_text(text) if text else text


# Function to fetch movie data for a range of years
def fetch_movie_data(year_range):
    movie_data = []

    for year in year_range:
        print(f"Fetching movies from {year}...")
        movies = fetch_movies_by_year(year)

        for movie in movies:
            movie_details = get_movie_details(movie["id"])
            credits = movie_details.get("credits", {})

            # Check the runtime (skip movies under 60 minutes)
            runtime = movie_details.get("runtime")
            if runtime is not None and runtime < 60:
                print(
                    f"Skipping {movie_details.get('title')} - Duration: {runtime} minutes"
                )
                continue  # Skip this movie if runtime is less than 60 minutes

            # Fetch the content rating
            content_rating = get_movie_content_rating(movie["id"])

            print(f"Adding {movie_details.get('title')} - Duration: {runtime} minutes")

            # Collecting all important and interesting data points, and cleaning text fields
            movie_data.append(
                {
                    "Title": clean_text(movie_details.get("title")),
                    "Year": movie_details.get("release_date", "").split("-")[0],
                    "Director": clean_text(get_director(credits)),
                    "Producer": clean_text(get_producer(credits)),
                    "Genres": clean_text(
                        ", ".join(
                            [genre["name"] for genre in movie_details.get("genres", [])]
                        )
                    ),
                    "Summary": clean_text(movie_details.get("overview")),
                    "Duration": runtime,
                    "Budget": movie_details.get("budget"),
                    "Revenue": movie_details.get("revenue"),
                    "Ratings": movie_details.get("vote_average"),
                    "Vote Count": movie_details.get("vote_count"),
                    "Popularity": movie_details.get("popularity"),
                    "Content Rating": content_rating,
                    "Original Language": movie_details.get("original_language"),
                    "Production Companies": clean_text(
                        ", ".join(
                            [
                                company["name"]
                                for company in movie_details.get(
                                    "production_companies", []
                                )
                            ]
                        )
                    ),
                    "Production Countries": clean_text(
                        ", ".join(
                            [
                                country["name"]
                                for country in movie_details.get(
                                    "production_countries", []
                                )
                            ]
                        )
                    ),
                    "Spoken Languages": clean_text(
                        ", ".join(
                            [
                                language["name"]
                                for language in movie_details.get(
                                    "spoken_languages", []
                                )
                            ]
                        )
                    ),
                    "Tagline": clean_text(movie_details.get("tagline")),
                    "Adult": movie_details.get("adult"),
                    "Movie ID": movie["id"],
                }
            )

        time.sleep(1)  # To avoid rate-limiting

    return movie_data


# Define the range of years (you can adjust the range as needed)
year_range = range(1970, 2025)

# Fetch the movie data for the specified range of years
movies = fetch_movie_data(year_range)

# Convert the movie data list into a pandas DataFrame
df = pd.DataFrame(movies)

# Save the DataFrame to a CSV file
df.to_csv("movie_data.csv", index=False)
print("Data saved to movie_data.csv")
