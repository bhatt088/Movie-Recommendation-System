import pandas as pd
import streamlit as st
import pickle
st.title('movie recommender system')

from dotenv import load_dotenv
import os

load_dotenv()  # loads .env file

TMDB_TOKEN = os.getenv("TMDB_TOKEN")
import requests
import os

TMDB_TOKEN = os.getenv("TMDB_TOKEN")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_TOKEN}"
}

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    response = requests.get(url, headers=headers)
    data = response.json()

    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    return None



def recommend (movie):
    recommended_movie = []
    recommended_movies_posters = []

    if movie not in movies['title'].values:
        st.error("Movie not found in dataset")
        return [], []

    movie_index = movies[movies['title']== movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted (list(enumerate(distances)), reverse = True , key = lambda x:x[1])[1:6]
    for i in movies_list:
        movie_id = movies.iloc[i[0]]['id']
        #fetch_poster_by api

        recommended_movie.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movie, recommended_movies_posters
movie_dict =  pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)

similarity =  pickle.load(open('similarity.pkl','rb'))
selected_movie_name = st.selectbox(
    "choose your movie ",
    movies['title'].values)


if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(posters[0],use_container_width=True)
        st.markdown(f"<div class='movie-title'>{names[0]}</div>", unsafe_allow_html=True)
    with col2:
        st.image(posters[1],use_container_width=True)
        st.markdown(f"<div class='movie-title'>{names[1]}</div>", unsafe_allow_html=True)
    with col3:
        st.image(posters[2],use_container_width=True)
        st.markdown(f"<div class='movie-title'>{names[2]}</div>", unsafe_allow_html=True)
    with col4:
        st.image(posters[3],use_container_width=True)
        st.markdown(f"<div class='movie-title'>{names[3]}</div>", unsafe_allow_html=True)
    with col5:
        st.image(posters[4],use_container_width=True)
        st.markdown(f"<div class='movie-title'>{names[4]}</div>", unsafe_allow_html=True)

