import os
import pandas as pd
import streamlit as st
import pickle
import requests
from dotenv import load_dotenv

# Get the absolute path to the current directory
current_directory = os.path.abspath(os.getcwd())

# Construct the absolute path to the pickle file
file_path_movies = os.path.join(current_directory, 'movie_list.pkl')

# Use pandas to read the pickle file directly
movies_df = pd.read_pickle(file_path_movies)




# Load the similarity matrix
file_path_similarity = os.path.join(current_directory, 'similarity.pkl')

similarity = pd.read_pickle(file_path_similarity)

# similarity = pickle.load(open('data/pkl_data/similarity.pkl','rb'))

# Function:
def configure():
    load_dotenv()
    
def fetch_poster(movie_id):
    print(movie_id)
    try:
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=9879c485409304647f8b48d10982f910&language=en-US")
        data = response.json()
        # print(data)
        return "https://image.tmdb.org/t/p/original"+data['poster_path']
    except:
            return "image/no-poster.png"

def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_poster = []
    for movie in movies_list:
        id = movies_df.iloc[movie[0]].movie_id
        recommended_movies.append(movies_df.iloc[movie[0]].title)
        # Fetch poster from API
        recommended_movies_poster.append(fetch_poster(id))
    return recommended_movies,recommended_movies_poster



# def recommend(movie):
#     try:
#         # Get the index of the selected movie
#         movie_index = movies_df[movies_df['title'] == movie].index[0]

#         # Get the similarity scores for the selected movie
#         distances = similarity[movie_index]

#         # Sort movies based on similarity scores and get the top 15
#         movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:16]

#         recommended_movies = []
#         recommended_movies_poster = []

#         # Iterate over the recommended movies
#         for movie in movies_list:
#             # Get the movie ID
#             movie_id = movies_df.iloc[movie[0]].movie_id

#             # Fetch movie details from TMDB API
#             response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={os.getenv('API_KEY')}&language=en-US")
#             data = response.json()

#             # Append movie title to the list
#             recommended_movies.append(data['title'])

#             # Append movie poster URL to the list
#             recommended_movies_poster.append("https://image.tmdb.org/t/p/original" + data['poster_path'])

#         return recommended_movies, recommended_movies_poster

#     except IndexError:
#         # Handle the case where the selected movie is not found in the data
#         st.error("Currently we don't have any information about this movie.")
#         return [], []



# Web App
# def main():
#     # ENV Config
#     configure()
    
#     # Streamlit Config
#     st.set_page_config(page_title="Movie Recommender", page_icon=":camera:", layout="wide")
    
#     # Hide default styles
#     hide_st_style = """
#         <style>
#         #MainMenu {visibility: hidden;}
#         footer {visibility: hidden;}
#         button[title="View fullscreen"] {visibility: hidden;}
#         </style>
#     """
#     st.markdown(hide_st_style, unsafe_allow_html=True)
    
#     # Web Components
#     st.title('Movie Recommendation System')
#     selected_movie = st.selectbox(
#         label="Select a movie",
#         options=movies_df['title'],
#         placeholder = "Choose a movie",
#         index=None)

#     if st.button('Recommend'): 
#         # No movies selected 
#         if selected_movie == None:
#             st.error("No movies selected.")
#             exit()   
                     
#         try:    
#             names,posters = recommend(selected_movie)
#             col1, col2, col3, col4, col5 = st.columns(5)
            
#             with col1:
#                 st.text(names[0])
#                 st.image(posters[0])
                
#                 st.text(names[5])
#                 st.image(posters[5])
                
#                 st.text(names[10])
#                 st.image(posters[10])
                
#             with col2:
#                 st.text(names[1])
#                 st.image(posters[1])

#                 st.text(names[6])
#                 st.image(posters[6])
                
#                 st.text(names[11])
#                 st.image(posters[11])
                             
#             with col3:
#                 st.text(names[2])
#                 st.image(posters[2])
                
#                 st.text(names[7])
#                 st.image(posters[7])
                
#                 st.text(names[12])
#                 st.image(posters[12])
                
#             with col4:
#                 st.text(names[3])
#                 st.image(posters[3])
                
#                 st.text(names[8])
#                 st.image(posters[8])
                
#                 st.text(names[13])
#                 st.image(posters[13])
                
#             with col5:
#                 st.text(names[4])
#                 st.image(posters[4])
                
#                 st.text(names[9])
#                 st.image(posters[9])
                
#                 st.text(names[14])
#                 st.image(posters[14])
       
#         except IndexError:
#             st.error("Currently we don't have any information about this movie.")


def main():
    # ENV Config
    configure()
    
    # Streamlit Config
    st.set_page_config(page_title="Movie Recommender", page_icon=":camera:", layout="wide")
    
    # Hide default styles
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        button[title="View fullscreen"] {visibility: hidden;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    
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
            names, posters = recommend(selected_movie)
            col1, col2, col3, col4, col5 = st.columns(5)

            # Display only the top 5 recommended movies
            for i in range(5):
                with locals()[f"col{i+1}"]:
                    st.text(names[i])
                    st.image(posters[i])

        except IndexError:
            st.error("Currently we don't have any information about this movie.")

if __name__=="__main__": 
    main()