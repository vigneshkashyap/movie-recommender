import streamlit as st
import pickle as pl
import pandas as pd
import requests as req

similarity = pl.load(open('../model/similarity.pkl', 'rb'))
movies_dict = pl.load(open('../model/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
st.title("Recommender System")

def getPoster(movieId):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=f5458095cd4bd789e64d3734ba065d4a'.format(movieId)
    # auth = HTTPBasicAuth('api_key', 'f5458095cd4bd789e64d3734ba065d4a');
    response = req.get(url=url)
    data = response.json()
    # st.write(data)
    poster_url_base = 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
    return poster_url_base


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    # val = np.int64()
    for movie in movies_list:
        movieItem = {'movieId': int(movies.iloc[movie[0]].movie_id), 'movieName': movies.iloc[movie[0]].title}
        # recommended_movies.append({int(movies.iloc[movie[0]].movie_id), movies.iloc[movie[0]].title})
        recommended_movies.append(movieItem)
        recommended_movies_posters.append(getPoster(int(movies.iloc[movie[0]].movie_id)))
    return recommended_movies, recommended_movies_posters

response = movies['title'].values.tolist()
selectedMovieName = st.selectbox('Type the name of the Movie', response)

if st.button('Recommend'):
    movie_name, posters = recommend(selectedMovieName)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_name[0].get('movieName'))
        st.image(posters[0])
    with col2:
        st.text(movie_name[1].get('movieName'))
        st.image(posters[1])
    with col3:
        st.text(movie_name[2].get('movieName'))
        st.image(posters[2])
    with col4:
        st.text(movie_name[3].get('movieName'))
        st.image(posters[3])
    with col5:
        st.text(movie_name[4].get('movieName'))
        st.image(posters[4])
