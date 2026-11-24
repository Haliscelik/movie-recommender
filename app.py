# Import libraries
from flask import Flask, render_template, request
from pathlib import Path
import pickle
import gzip

# Create the Flask app
app = Flask(__name__)

# Locate the saved recommendation files
app_folder = Path(__file__).resolve().parent
data_folder = app_folder / "data"

# Load the prepared movie table
with open(data_folder / "model.pkl", "rb") as file:
    movies = pickle.load(file)

# Load the compressed similarity matrix
with gzip.open(data_folder / "similarity.pkl.gz", "rb") as file:
    similarity = pickle.load(file)

# Define a function to find movie positions by title
def recommend_movies(movie_title):
    title_matches = movies["title"] == movie_title
    movie_positions = []

    for position, matches in enumerate(title_matches):
        if matches:
            movie_positions.append(position)
    # Check whether the movie title exists
    if not movie_positions:
        raise ValueError("Movie title not found.")
        # Reject ambiguous movie titles
    if len(movie_positions) > 1:
        raise ValueError("Multiple movies share this title. Select by movie ID.")
    
    # Get similarity scores for the selected movie
    selected_position = movie_positions[0]
    selected_scores = similarity[selected_position]

        # Pair movie positions with similarity scores
    movie_scores = list(enumerate(selected_scores))

    # Rank movies by similarity score
    sorted_scores = sorted(
        movie_scores,
        key=lambda item: item[1],
        reverse=True
    )

        # Exclude the selected movie
    other_movies = []

    for movie_position, score in sorted_scores:
        if movie_position != selected_position:
            other_movies.append((movie_position, score))

       # Get titles and scores for the five recommendations
    recommendations = []

    for movie_position, score in other_movies[:5]:
        title = movies.iloc[movie_position]["title"]
        recommendations.append((title, float(score)))

    return recommendations
    
# Display the movie selection page
@app.route("/")
def home():
    movie_list = movies["title"].tolist()
    return render_template("index.html", movie_list=movie_list)

# Display recommendations for the selected movie
@app.route("/recommend", methods=["POST"])
def recommend():
    movie_title = request.form["selected_movie"]
    recommendations = recommend_movies(movie_title)

    recommended_titles = []
    for title, score in recommendations:
        recommended_titles.append(title)

    movie_list = movies["title"].tolist()

    return render_template(
        "index.html",
        movie_list=movie_list,
        recommended_movie_titles=recommended_titles,
        selected_movie=movie_title
    )

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
    