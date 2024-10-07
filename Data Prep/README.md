# Movie Dataset Cleaning

This stage of the project focuses on cleaning and preparing a raw movie dataset for analysis. The data includes various fields such as title, director, producer, budget, ratings, and more.

## Steps Involved:

### Data Import:
Imported the CSV with low_memory=False to handle large datasets.
Converted numeric fields (e.g., Year, Duration, Budget, etc.) to appropriate data types.

### Data Cleaning:
Removed movies with missing Director or Producer.
Removed movies with no Summary or Genres.
Fixed corrupted text using ftfy for all string columns.
Converted specific columns (e.g., Genres, Languages) to comma-separated lists.
Ensured languages and companies were in ASCII format, removing non-ASCII entries.

### Duplicate Removal:
Identified and removed duplicate movies based on Title and Year.

### Stand-up Comedy Filter:
Excluded movies classified solely as Comedy and Documentary, often indicating stand-up performances.

### Final Export:
The cleaned dataset was saved to cleaned_movie_data.csv.

## Output:

Cleaned movie data ready for further analysis or machine learning tasks.