import pandas as pd

movie_similarity_df = pd.read_csv("movie_similarity.csv", index_col=0)
user_similarity_df = pd.read_csv("user_similarity.csv", index_col=0)
ratings_summary = pd.read_csv("ratings_summary.csv", index_col=0)
ratings_with_movies = pd.read_csv('ratings_with_movies.csv')


def predict_rating(movie_name):
    if movie_name in ratings_summary['movie_name'].values:
        return ratings_summary.loc[ratings_summary['movie_name'] == movie_name, 'avg_rating'].values[0]
    return "Movie not found"

def recommend_similar_movies(movie_name, top_n=5):
    if movie_name in movie_similarity_df.index:
        similar_movies = movie_similarity_df[movie_name].sort_values(ascending=False).iloc[1:top_n + 1]
        return similar_movies.index.tolist()
    return "Movie not found"

def top_users_for_movie(movie_name, top_n=10):
    movie_ratings = ratings_with_movies[ratings_with_movies['title'] == movie_name]
    top_users = movie_ratings.sort_values(by='rating', ascending=False).head(top_n)
    return top_users['user_id'].tolist()

def recommend_movies_for_user(user_id, top_n=5):
    if user_id in user_similarity_df.index:
        similar_users = user_similarity_df.iloc[user_id].sort_values(ascending=False).iloc[1:top_n + 1]
        similar_user_ids = similar_users.index
        recommendations = ratings_with_movies[ratings_with_movies['user_id'].isin(list(map(int, similar_user_ids)))]
        top_recommendations = recommendations.groupby('title')['rating'].mean().sort_values(ascending=False).head(top_n)
        return top_recommendations.index.tolist()
    return "User not found"

# predicted_rating_star_wars = predict_rating("Star Wars (1977)")
# similar_movies_star_wars = recommend_similar_movies("Star Wars (1977)")
# top_users_star_wars = top_users_for_movie("Star Wars (1977)")
# user_224_recommendations = recommend_movies_for_user(224)

