import numpy as np
from flask import Flask, abort, jsonify, request
import pickle as pl
import pandas as pd

similarity = pl.load(open('model/similarity.pkl', 'rb'))
movies_dict = pl.load(open('model/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    recommended_movies = []
    # val = np.int64()
    for movie in movies_list:
        movieItem = {'movieId': int(movies.iloc[movie[0]].movie_id), 'movieName': movies.iloc[movie[0]].title}
        # recommended_movies.append({int(movies.iloc[movie[0]].movie_id), movies.iloc[movie[0]].title})
        recommended_movies.append(movieItem)
    return recommended_movies

app = Flask(__name__)

@app.route('/movie/predict', methods=[ 'POST' ])
def make_predict():
    # all kinds of error checking should go here
    data = request.get_json(force=True)
    print(data)
    # convert our json to a numpy array
    request_movie_name = data['name']
    # return our prediction
    output = recommend(request_movie_name)
    print(output)
    return jsonify(output)

@app.route('/movie/get', methods=[ 'GET' ])
def get_movies():
    # request_movie_name = data['name']
    response = movies['title'].values.tolist()
    return jsonify(response)

if __name__ == '__main__' :
    app.run(port = 7780, debug = True)