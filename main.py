import asyncio
from pyscript import document
from pyweb import pydom
from pyscript import when
import js
from js import console, decodeURIComponent
import pandas as pd
import numpy as np

# Load dataset (simulate as the PyScript environment may have limited file I/O)
MOVIE_DATASET_PATH = "./datasets/Movie_Id_Titles_Enhanced.csv"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500/"
NO_IMAGE_URL = "https://via.placeholder.com/500x750?text=No+Image"

# Example movie data (will be expanded from CSV)
movie_data = {
    "Toy Story (1995)": {
        "predicted_rating": 4.36,
        "recommended_movies": [
            "Return of the Jedi (1983)",
            "Raiders of the Lost Ark (1981)",
            "The Empire Strikes Back (1980)",
            "Toy Story (1995)",
            "The Godfather (1972)",
        ],
        "top_users": [0, 268, 748, 864, 337, 419, 392, 85, 791, 862],
        "user_224_recommendations": [
            "The Killing Fields (1984)",
            "Dead Man Walking (1995)",
            "Waiting for Guffman (1996)",
            "Cool Hand Luke (1967)",
            "To Catch a Thief (1955)",
        ],
    }
}

# Load additional movie data
def load_movie_data():
    df = pd.read_csv(MOVIE_DATASET_PATH)
    for _, row in df.iterrows():
        movie_name = row["movie_name"]
        movie_data[movie_name] = {
            "poster_path": POSTER_BASE_URL + row["poster_path"]
            if row["poster_path"] != "Unknown"
            else NO_IMAGE_URL
        }

load_movie_data()

async def get_query_params():
    url_params = js.window.location.search
    params = dict(x.split('=') for x in url_params.lstrip('?').split('&') if '=' in x)
    movie_name = decodeURIComponent(params.get("movie", ""))
    if movie_name:
        display_results(movie_name)
    else:
        document.querySelector("#recommendation-list").innerHTML = "<li>No movie selected!</li>"

def get_predicted_rating(movie):
    if "predicted_rating" in movie_data[movie]:
        rating = movie_data[movie]["predicted_rating"]
    else:
        rating = "Rating not available."
    document.querySelector("#predicted_rating p").innerText = f"Predicted Rating: {rating}"

def get_recommendations(movie):
    recommendation_grid = document.querySelector("#recommendation-grid")
    recommendation_grid.innerHTML = ""

    if "recommended_movies" in movie_data[movie]:
        for recommended_movie in movie_data[movie]["recommended_movies"]:
            poster_path = (
                movie_data[recommended_movie]["poster_path"]
                if recommended_movie in movie_data
                else NO_IMAGE_URL
            )
            recommendation_grid.innerHTML += f"""
                <div class="movie">
                    <img src="{poster_path}" alt="{recommended_movie}" />
                    <p>{recommended_movie}</p>
                </div>
            """
    else:
        recommendation_grid.innerHTML = "<p>No recommendations available.</p>"

def get_top_users(movie):
    top_users_list = document.querySelector("#top-users-list")
    top_users_list.innerHTML = ""

    if "top_users" in movie_data[movie]:
        for user_id in movie_data[movie]["top_users"]:
            top_users_list.innerHTML += f"<li>User ID: {user_id}</li>"
    else:
        top_users_list.innerHTML = "<li>No top users available.</li>"

def add_recommendation(content):
    item_template = pydom.Element(document.querySelector("#list-item-template").content.querySelector("li"))
    item_html = item_template.clone()
    item_html.find("p")[0]._js.textContent = content
    recommendation_list.append(item_html)

def display_results(movie):
    get_predicted_rating(movie)
    get_recommendations(movie)
    get_top_users(movie)

recommendation_list = pydom["#recommendation-list"][0]
rating_p = pydom["#predicted_rating"]

async def main():
    _ = await asyncio.gather(get_query_params())

asyncio.ensure_future(main())
