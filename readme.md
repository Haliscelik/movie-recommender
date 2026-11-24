# Movie Recommendation System

A content-based movie recommendation system with a Flask web interface.
Users select a movie and receive five recommendations based on content
similarity.

## Problem and Goal

Finding similar movies can be difficult when a catalogue contains
thousands of titles. This project helps users discover movies with
similar descriptions, genres, keywords, cast members, and directors.

## Recommendation Method

The project uses the TMDB 5000 movie dataset, containing 4,803 movies.

1. Merge movie information and credits using movie IDs.
2. Prepare the overview, genres, keywords, first three cast members,
   and director names.
3. Combine these features into a text representation called tags.
4. Convert tags into numerical vectors using CountVectorizer with
   a maximum of 500 features and English stop words removed.
5. Calculate cosine similarity between movie vectors.
6. Return the five most similar movies, excluding the selected movie.

The Flask application loads the saved movie table and similarity matrix
and displays recommendations through an HTML interface.

## Project Files

| File | Purpose |
|------|---------|
| `movie_recommendation2.ipynb` | Data checks, feature preparation, vectorization, similarity calculation, and recommendation testing |
| `app.py` | Flask application and recommendation logic |
| `templates/index.html` | Movie selection form and recommendation display |
| `requirements.txt` | Python package versions |
| `data/tmdb_5000_movies.csv` | Movie information |
| `data/2tmdb_5000_credits.csv` | Cast and crew information |
| `data/model.pkl` | Prepared movie table containing id, title, and tags |
| `data/similarity.pkl.gz` | Precomputed movie similarity matrix |

The saved movie table and similarity matrix must use the same movie order.
The application loads both files from the data folder.
The similarity matrix is stored using lossless gzip compression.
This reduced its file size from 176 MB to approximately 31.57 MB
without changing the similarity scores.

## How to Run Locally

1. Download the project and open a terminal in the project folder.

2. Install the required packages:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Make sure `data/model.pkl` and `data/similarity.pkl.gz` exist.
   If they are missing, open `data/movie_recommendation2.ipynb` in Jupyter
   and run all cells from top to bottom to.
   Run the notebook with `data` as its working folder.

4. Start the Flask application:

   ```bash
   python app.py
   ```

5. Open http://127.0.0.1:5000 in your browser.

6. Select a movie and click **Get Recommendations**.

Keep the terminal open while using the application.
To stop the server, press **Ctrl+C** in the terminal.

The application runs locally using Flask's development server.

## Data Quality and Sources

The original credits file contained unexpected columns and unreadable
cast records. Removing the extra columns did not resolve the parsing
problems, so I replaced the file with another copy of the TMDB 5000
credits dataset.

The replacement contains 4,803 rows and four columns. Before merging,
I checked for missing IDs, duplicate IDs, and unmatched movie IDs.
These checks found no issues.

Three movies had missing overviews. I kept these movies and replaced
the missing overviews with empty strings so their other features
could still contribute to recommendations.

Starter project:
https://github.com/furkhan67/movie_recommender

Replacement credits source:
https://github.com/masiod/TMDb_movie_data

The replacement credits file is saved locally as
`data/2tmdb_5000_credits.csv`.

## Validation and Limitations

Recommendations for Avatar and Pirates of the Caribbean: At World's End
matched between the notebook and the Flask application.

This confirms consistency for these two examples, rather than measuring
overall recommendation quality.

The current system uses content similarity and does not personalise
recommendations using user ratings. Titles shared by multiple movies
are rejected by the recommendation function; selection by movie ID
is a possible future improvement.