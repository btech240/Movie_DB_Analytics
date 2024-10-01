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

Set up environment variables:

Create a .env file in the project directory and add your TMDb API key like this:

```API_KEY=your_tmdb_api_key```