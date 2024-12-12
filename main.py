import asyncio
from pyscript import document
from pyweb import pydom
from pyscript import when
import js
from js import console, decodeURIComponent
import pandas as pd
from predictions import (
    predict_rating,
    recommend_similar_movies,
    top_users_for_movie,
    recommend_movies_for_user,
)

POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500/"
NO_IMAGE_URL = "https://via.placeholder.com/500x750?text=No+Image"

data = pd.read_csv('Movie_Id_Titles_Enhanced.csv')

predicted_rating_div = pydom["#predicted_rating"][0]
recommendation_list = document.querySelector("#recommendation-list")
user_recommendation_list = document.querySelector("#user-recommendation-list")
loading = document.querySelector("#loading")
item_template = document.querySelector("#list-item-template li")

def fetch_movie_data():
    url_params = js.window.location.search
    params = dict(x.split('=') for x in url_params.lstrip('?').split('&') if '=' in x)
    movie_id = decodeURIComponent(params.get("movie", ""))

    if not movie_id:
        console.error("No 'movie' parameter found in URL.")
        return {"error": "No movie selected!"}

    try:
        if 'item_id' not in data.columns or 'title' not in data.columns:
            console.error("'Movie_Id_Titles_Enhanced.csv' must contain 'item_id' and 'title' columns.")
            return {"error": "Invalid movie data file."}

        movie_row = data.loc[data['item_id'] == int(movie_id)]
        if movie_row.empty:
            console.error(f"No movie found with item_id: {movie_id}")
            return {"error": "Movie not found."}

        movie_title = movie_row['title'].values[0]
        console.log(f"Found movie: {movie_title}")
        return {"movie_id": movie_id, "title": movie_title}
    except Exception as e:
        console.error(f"Error fetching movie data: {e}")
        return {"error": "An error occurred while fetching movie data."}

def display_predicted_rating(rating):
    content = f"<strong>Predicted Rating According to your Liking:</strong> {rating:.2f} ⭐"
    new_div = pydom.create("div")
    new_div.create("p", html=content)
    predicted_rating_div.append(new_div)

def display_similar_movies(similar_movies):
    recommendation_list.innerHTML = ""
    if similar_movies:
        for movie in similar_movies:
            add_recommendation(movie)

def get_poster_url(movie_title):
    try:
        movie_row = data.loc[data['title'] == movie_title]
        if not movie_row.empty:
            poster_path = movie_row['poster_path'].values[0]
            if poster_path and poster_path != 'Unknown':
                return POSTER_BASE_URL + poster_path
    except Exception as e:
        console.error(f"Error fetching poster URL: {e}")

    return NO_IMAGE_URL

def add_recommendation(movie):
    cloned_li = item_template.cloneNode(True)
    poster_url = get_poster_url(movie)
    cloned_li.querySelector('img').setAttribute('src', poster_url)
    cloned_li.querySelector('p').innerHTML = movie
    recommendation_list.append(cloned_li)

def display_user_recommendations(user_recommendations):
    user_recommendation_list.innerHTML = ""
    if user_recommendations:
        for movie in user_recommendations:
            add_user_recommendation(movie)

def add_user_recommendation(movie):
    cloned_li = item_template.cloneNode(True)
    poster_url = get_poster_url(movie)
    cloned_li.querySelector('img').setAttribute('src', poster_url)
    cloned_li.querySelector('p').innerHTML = movie
    user_recommendation_list.append(cloned_li)

async def display_results():
    movie_data = fetch_movie_data()

    if "error" in movie_data:
        return

    movie_title = movie_data['title']
    console.log(f"Processing movie: {movie_title}")

    predicted_rating = predict_rating(movie_title)
    if isinstance(predicted_rating, (float, int)):
        display_predicted_rating(predicted_rating)
    else:
        error_content = f"<span style='color: red;'>{predicted_rating}</span>"
        error_div = pydom.create("div")
        error_div.create("p", html=error_content)
        predicted_rating_div.append(error_div)

    loading.innerHTML = ""
    similar_movies = recommend_similar_movies(movie_title)
    console.log(f"Similar Movies: {similar_movies}")
    if isinstance(similar_movies, list):
        display_similar_movies(similar_movies)

    user_id = 224 
    user_recommendations = recommend_movies_for_user(user_id)
    print(user_recommendations)
    if isinstance(user_recommendations, list):
        display_user_recommendations(user_recommendations)

async def main():
    await display_results()

asyncio.ensure_future(main())
