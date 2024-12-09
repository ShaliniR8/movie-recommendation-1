import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from joblib import dump

def load_data(interaction_file, movies_file):
    """Load interaction and movie mapping data."""
    # Define column names for the TSV and CSV files
    interaction_columns = ["user_id", "item_id", "rating", "timestamp"]
    movie_columns = ["movie_id", "movie_name"]

    # Load the files with the defined column names
    interactions = pd.read_csv(interaction_file, sep="\t", names=interaction_columns)
    movies = pd.read_csv(movies_file, names=movie_columns)
    return interactions, movies

def preprocess_data(interactions, movies):
    """Preprocess data for training."""
    # Ensure consistent data types for merging
    interactions['item_id'] = interactions['item_id'].astype(str)
    movies['movie_id'] = movies['movie_id'].astype(str)

    # Merge interactions with movie names for interpretability
    interactions = interactions.merge(movies, left_on="item_id", right_on="movie_id", how="left")

    # Create a user-item matrix
    user_item_matrix = interactions.pivot_table(index="user_id", columns="item_id", values="rating", fill_value=0)
    return user_item_matrix


def train_model(user_item_matrix, n_components=50):
    """Train a recommendation model using SVD."""
    # Decompose the user-item matrix
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    svd.fit(user_item_matrix)
    return svd

def save_mappings(user_item_matrix, movies, model, model_path="model.pkl"):
    """Save model and mappings for later use."""
    # Save the model
    dump(model, model_path)

    import base64

    # Encode the model.pkl file to Base64
    with open("model.pkl", "rb") as file:
        encoded_model = base64.b64encode(file.read()).decode("utf-8")

    # Save the Base64 string to a text file
    with open("model_base64.txt", "w") as out_file:
        out_file.write(encoded_model)

    # Save mappings for reverse lookup
    user_mapping = pd.DataFrame({"user_id": user_item_matrix.index}).reset_index()
    movie_mapping = movies[["movie_id", "movie_name"]]
    user_mapping.to_csv("users_mapping.csv", index=False)
    movie_mapping.to_csv("movies_mapping.csv", index=False)

def main():
    interaction_file = "file.tsv"
    movies_file = "Movie_Id_Titles.csv"

    # Load and preprocess data
    interactions, movies = load_data(interaction_file, movies_file)
    user_item_matrix = preprocess_data(interactions, movies)

    # Train the model
    print("Training the model...")
    model = train_model(user_item_matrix)
    
    # Save the model and mappings
    print("Saving the model and mappings...")
    save_mappings(user_item_matrix, movies, model)
    print("All files saved successfully.")

if __name__ == "__main__":
    main()
