import pandas as pd
import streamlit as st
import pickle
import os
import requests

from huggingface_hub import hf_hub_download

@st.cache_resource
def load_similarity():
    file_path = hf_hub_download(
        repo_id="Bhattji-hug/movie-recommendation",
        filename="similarity.pkl",
        repo_type="space"
    )

    with open(file_path, "rb") as f:
        return pickle.load(f)

similarity = load_similarity()


st.title('movie recommender system')

from dotenv import load_dotenv


load_dotenv()  # loads .env file

TMDB_TOKEN = os.getenv("TMDB_TOKEN")


headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_TOKEN}"
}

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
    except:
        pass
    return None




def recommend (movie, similarity):
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


selected_movie_name = st.selectbox(
    "choose your movie ",
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name, similarity)

    cols = st.columns(5)

    for i in range(len(cols)):
        with cols[i]:
            if posters[i] is not None:
                st.image(posters[i], use_container_width=True)
            else:
                st.info("Poster not available")
            st.markdown(
                f"<div class='movie-title'>{names[i]}</div>",
                unsafe_allow_html=True
            )

##if st.button('Recommend'):
 #   names,posters = recommend(selected_movie_name,similarity)
#    col1, col2, col3, col4, col5 = st.columns(5)
 #   with col1:
  #      st.image(posters[0],use_container_width=True)
   #     st.markdown(f"<div class='movie-title'>{names[0]}</div>", unsafe_allow_html=True)
    #with col2:
     #   st.image(posters[1],use_container_width=True)
      #  st.markdown(f"<div class='movie-title'>{names[1]}</div>", unsafe_allow_html=True)
#    with col3:
#        st.image(posters[2],use_container_width=True)
#        st.markdown(f"<div class='movie-title'>{names[2]}</div>", unsafe_allow_html=True)
#    with col4:
 #       st.image(posters[3],use_container_width=True)
 #       st.markdown(f"<div class='movie-title'>{names[3]}</div>", unsafe_allow_html=True)
 #   with col5:
  #      st.image(posters[4],use_container_width=True)
 #       st.markdown(f"<div class='movie-title'>{names[4]}</div>", unsafe_allow_html=True)##


