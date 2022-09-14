import pandas as pd
import json
import requests

MovieAPIKey='6461108259d95817ace0a23e57345c98'
TOP_RATED_MOVIES_API_URL = 'https://api.themoviedb.org/3/movie/top_rated'

for i in range(3,10):
    movie_list  = requests.get(f"{TOP_RATED_MOVIES_API_URL}?api_key={MovieAPIKey}&language=en-US&page={i}").json()
       
    # Parse the json string to a python dictionary
    # data = json.loads(movie_list)

    # The desired data is in the `Data` field, use pandas to construct the data frame
    df = pd.json_normalize(movie_list["results"])

    # Save to a csv file
    df.to_csv(f"result{i}.csv")