import os
import pandas as pd
import streamlit as st
import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw
import numpy as np
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Define the configure function
def configure():
    load_dotenv()

# Create a requests session with retry logic
def create_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

# Define the fetch_poster function
def fetch_poster(movie_id):
    print(movie_id)
    session = create_session()
    try:
        response = session.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=9879c485409304647f8b48d10982f910&language=en-US")
        response.raise_for_status()
        data = response.json()
        print(data)
        return "https://image.tmdb.org/t/p/original" + data['poster_path']
    except requests.RequestException as e:
        st.error(f"Failed to fetch poster for movie_id {movie_id}: {e}")
        return "image/no-poster.png"

# Define the recommend function with movies_df as a parameter
def recommend(movie, movies_df, similarity):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for movie in movies_list:
        id = movies_df.iloc[movie[0]].movie_id
        recommended_movies.append(movies_df.iloc[movie[0]].title)
        # Fetch poster from API
        recommended_movies_poster.append(fetch_poster(id))
    return recommended_movies, recommended_movies_poster

# Define the main function
def main():
    # ENV Config
    configure()
    
    # Streamlit Config
    st.set_page_config(page_title="Movie Recommender", page_icon=":camera:", layout="wide")
    
    # Get the absolute path to the current directory
    current_directory = os.path.abspath(os.getcwd())

    # Construct the absolute path to the pickle file
    file_path_movies = os.path.join(current_directory, 'movie_list.pkl')
    print(file_path_movies)

    # Use pandas to read the pickle file directly
    movies_df = pd.read_pickle(file_path_movies)

    # Load the similarity matrix
    file_path_similarity = os.path.join(current_directory, 'similarity.pkl')
    similarity = pd.read_pickle(file_path_similarity)
 
    # Add custom CSS styles to set the background image
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('background_image.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Web Components
    st.title('Movie Recommendation System')
    selected_movie = st.selectbox(
        label="Select a movie",
        options=movies_df['title'],
        placeholder="Choose a movie",
        index=None)

    if st.button('Recommend'): 
        # No movies selected 
        if selected_movie is None:
            st.error("No movies selected.")
            exit()   
                     
        try:    
            # Pass movies_df and similarity as parameters to the recommend function
            names, posters = recommend(selected_movie, movies_df, similarity)
            col1, col2, col3, col4, col5 = st.columns(5)

            # Display only the top 5 recommended movies
            for i in range(5):
                with locals()[f"col{i+1}"]:
                    st.text(names[i])
                    st.image(posters[i])

        except IndexError:
            st.error("Currently, we don't have any information about this movie.")

if __name__ == "__main__": 
    main()
