import streamlit as st
import pickle
import requests
import pandas as pd

def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=e41c6c7d8a32c1ab0cddf8215f135e24&language=en-US'.format(
            movie_id))
    data = response.json()
    if 'poster_path' in data:
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return None  # Return None if poster_path is not found

def recommend(movie):
    if movie in movies_list['title'].values:
        movie_index = movies_list[movies_list['title'] == movie].index[0]
        distances = similarity[movie_index]
        mo_li = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []
        for i in mo_li:
            movie_id = i[0]

            recommended_movies.append(movies_list.iloc[i[0]].title)
            # fetch poster from API
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters
    else:
        st.write(f"Movie '{movie}' not found in the dataset.")
        return []


movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select a movie', movies_list['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    for name, poster in zip(names, posters):
        st.header(name)
        if poster is not None and poster.startswith('http'):
            st.image(poster)
        else:
            st.write("No poster available for this movie")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])




