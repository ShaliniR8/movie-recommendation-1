import asyncio

from pyweb import pydom
from pyscript import when
from js import (
    console
)

import numpy as np
import pickle
from pyweb import pydom
from pyscript import when

# Load the recommendation model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

def get_recommendations(movie):
    """Generate recommendations based on a given movie."""
    try:
        recommendations = model.predict([movie])  # Assuming the model has a `predict` method
        return recommendations
    except Exception as e:
        return [f"Error: {str(e)}"]

form = pydom["#recommendation-form"][0]
button = pydom["button"][0]
console.log(button)

@when("click", button)
async def on_submit(event):
    event.preventDefault()
    movie_input = pydom["#movie-input"][0].value
    recommendations = get_recommendations(movie_input)
    
    recommendation_list = pydom["#recommendation-list"]
    recommendation_list.clear()
    for rec in recommendations:
        item = pydom.Element("li")
        item.textContent = rec
        recommendation_list.append(item)

async def main():
    _ = await asyncio.gather()

asyncio.ensure_future(main())
