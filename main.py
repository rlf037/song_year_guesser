import random
from datetime import datetime

import spotipy
import streamlit as st
from spotipy.oauth2 import SpotifyClientCredentials


def render_app():
    st.title("Song Year Guesser")
    st.write("Welcome to the Song Year Guesser app!")
    st.write("---")
    
    st.write("Select year range for songs (inclusive)")
    
    start_year = st.slider("Start Year", min_value=1950, max_value=datetime.now().year-1, value=1995, width=140)
    end_year = st.slider("End Year", min_value=start_year, max_value=datetime.now().year, value=2005, width=140)

    if st.button("Play Song", type="primary"):
        load_song(start_year, end_year)

def load_song(start_year, end_year):
    year = random.randint(start_year, end_year)
    st.write(year)
    
    results = sp.search(q=f'year:{year}', type='track', limit=50)
    if results is not None:
        tracks = results['tracks']['items']

        if not tracks:
            st.write(f"No tracks found for the year {year}. Try a different year or search query.")
            return None
        random_track = random.choice(tracks)
        track_name = random_track['name']
        artist_name = random_track['artists'][0]['name']
        track_url = random_track['external_urls']['spotify']
        
        st.write(f"### {track_name} by {artist_name}")
        st.write(f"[Listen on Spotify]({track_url})")
    
if __name__ == "__main__":
    
    st.set_page_config(
        page_title="Song Game",
        page_icon="🎙️",
        layout="centered",
        initial_sidebar_state="expanded",
    )
    
    global sp
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=st.secrets["spotify"]["client_id"],
        client_secret=st.secrets["spotify"]["client_secret"]))

    
    render_app()
    
    