# Movie Data Store and Analysis

## Table of Contents
1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Environment Variables](#environment-variables)
5. [How the Script Works](#how-the-script-works)
    - [API Requests](#api-requests)
    - [Handling Rate Limits](#handling-rate-limits)
    - [Data Points Extracted](#data-points-extracted)
    - [Skipping Short Movies](#skipping-short-movies)
    - [Data Cleaning with FTFY](#data-cleaning-with-ftfy)
6. [Usage](#usage)
7. [Output](#output)
8. [FTFY Library Overview](#ftfy-library-overview)

---

## Introduction

This script uses the [TMDb API](https://www.themoviedb.org/documentation/api) to fetch detailed movie data for a given range of years. The data is fetched, cleaned, and stored in a CSV file for further analysis. It includes important metadata such as movie titles, directors, genres, ratings, and more. The script also integrates the **FTFY (Fixes Text For You)** library to ensure all text data is properly encoded and readable.

## Requirements

Before running the script, ensure you have the following:
- Python 3.7 or higher
- A valid [TMDb API key](https://www.themoviedb.org/settings/api)

## Installation

Install required packages:

This project uses the following Python packages:
*pandas: for handling and saving data in CSV format.
*requests: for making HTTP requests to the TMDb API.
*python-dotenv: for loading environment variables.
*ftfy: for fixing text encoding issues.

## Environment Variables:

Create a .env file in the project directory and add your TMDb API key like this:

```API_KEY=your_tmdb_api_key```

## How the Script Works

The script fetches movie data from the TMDb API for a range of years, processes that data, and stores it in a CSV file.

### API Requests

The script uses the TMDb API to:

    Discover movies by release year.
    Retrieve movie details, including the director, producer, genres, and more.
    Fetch movie content ratings.

The script makes GET requests to different TMDb endpoints using the requests library.

### Handling Rate Limits

To prevent exceeding TMDb's API rate limits, the script checks for HTTP 429 responses and pauses the execution for the time specified in the Retry-After header. This ensures smooth data fetching without interruptions.

### Data Points Extracted

For each movie, the following details are extracted:

    - Title
    - Year of release
    - Director
    - Producer
    - Genres
    - Summary (Overview)
    - Duration (in minutes)
    - Budget
    - Revenue
    - Ratings (Average vote score)
    - Vote count
    - Popularity
    - Content Rating (MPAA or equivalent)
    - Original Language
    - Production Companies
    - Production Countries
    - Spoken Languages
    - Tagline
    - Adult content flag
    - Movie ID (from TMDb)

### Skipping Short Movies

The script excludes movies with a runtime of less than 60 minutes. This is useful for focusing on full-length films rather than short films or documentaries.

### Data Cleaning with FTFY

To ensure that the text data is properly readable and free from encoding issues (such as strange symbols or improper character encodings), the FTFY library is used. This library fixes common encoding problems in text and ensures that the data extracted is clean and human-readable.

For example, if a movie title contains unusual characters due to encoding issues, FTFY will correct it so that it displays properly in the final output.

## Usage

The script currently fetches movie data for the year range 2023–2024. If you wish to fetch data for a different year or range, you can adjust the year_range variable:

year_range = range(2010, 2020)  # Fetch movies from 2010 to 2019

## Output

The fetched movie data will be saved as a CSV file named movie_data.csv in the project directory. You can analyze this file using data analysis tools like Excel, Google Sheets, or any Python-based data analysis libraries like pandas or numpy.
Example CSV Output

The CSV file will contain columns like:

| Title         | Year | Director    | Producer     | Genres | Summary            | Duration | Budget  | Revenue  | Ratings | Content Rating |
|---------------|------|-------------|--------------|--------|--------------------|----------|---------|----------|---------|----------------|
| Example Movie | 2023 | Jane Doe    | John Smith   | Drama  | A great film.       | 120      | 1000000 | 5000000  | 7.5     | PG-13           |
| Another Movie | 2023 | Someone Else| Producer Name| Action | Exciting action.    | 90       | 500000  | 2000000  | 6.8     | R               |

## FTFY Library Overview

FTFY stands for "Fixes Text For You." It is a Python library that automatically fixes common encoding issues that occur when text data is mishandled. The main purpose of FTFY is to make sure that text data is readable and properly encoded, which is particularly useful when fetching data from external APIs where encoding inconsistencies might occur.
Why Use FTFY?

When dealing with text from multiple sources, you may encounter issues like:

    Incorrect characters (e.g., Ã© instead of é).
    Unicode replacement characters (�).
    Garbled text due to encoding mismatches.

FTFY solves these issues by converting the text into a human-readable format.
How It Is Used in the Script

In this script, FTFY is used to clean up text fields such as:

    Movie titles
    Overview (summary)
    Taglines
    Production company names
    Genre names
    Other text-based fields

The script passes each of these fields through the ftfy.fix_text() function, which ensures that any encoding errors are fixed before the data is saved to the CSV file.