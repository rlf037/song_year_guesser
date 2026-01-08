import random
import base64
import io
import time
from datetime import datetime
from typing import Optional, List, Dict
from urllib.parse import quote

import spotipy
import streamlit as st
import requests
from PIL import Image, ImageFilter
from spotipy.oauth2 import SpotifyClientCredentials


# Page configuration
st.set_page_config(
    page_title="Song Year Guesser",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="expanded",
)


# Custom CSS for a clean, modern look
st.markdown("""
<style>
    .main-header {
        text-align: center;
        font-size: 3em;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5em;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5em;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 1.3em;
        margin: 1em 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .hint-box {
        background: #f0f2f6;
        padding: 1em;
        border-radius: 10px;
        margin: 0.5em 0;
        border-left: 4px solid #667eea;
    }
    .timer {
        font-size: 2em;
        font-weight: bold;
        text-align: center;
        color: #667eea;
        margin: 0.5em 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-size: 1.1em;
        font-weight: bold;
        transition: all 0.3s;
    }
    .year-button {
        margin: 0.3em;
    }
    .leaderboard {
        background: white;
        padding: 1em;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .game-over {
        text-align: center;
        font-size: 1.5em;
        padding: 2em;
        background: #f0f2f6;
        border-radius: 15px;
        margin: 1em 0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Spotify client
@st.cache_resource
def get_spotify_client():
    return spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=st.secrets["spotify"]["client_id"],
            client_secret=st.secrets["spotify"]["client_secret"]
        )
    )


def blur_image(image_url: str, blur_amount: int) -> str:
    """Download image and apply blur effect, return as base64"""
    try:
        response = requests.get(image_url, timeout=5)
        img = Image.open(io.BytesIO(response.content))

        if blur_amount > 0:
            img = img.filter(ImageFilter.GaussianBlur(radius=blur_amount))

        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return ""


def get_deezer_preview(track_name: str, artist_name: str) -> Optional[str]:
    """Get Deezer preview URL for a song with multiple search strategies"""

    # Try multiple search strategies
    search_queries = [
        f"{artist_name} {track_name}",  # Artist first (often better results)
        f"{track_name} {artist_name}",  # Track first
        f"{track_name}",                 # Track name only
        f"{artist_name}",                # Artist only as last resort
    ]

    for query in search_queries:
        try:
            encoded_query = quote(query)
            deezer_search_url = f"https://api.deezer.com/search/track?q={encoded_query}"

            response = requests.get(deezer_search_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('data') and len(data['data']) > 0:
                    # Check first 10 results for a valid preview
                    for result in data['data'][:10]:
                        preview_url = result.get('preview')
                        if preview_url:
                            return preview_url
        except Exception:
            continue  # Try next search strategy

    return None


def get_random_song(sp, start_year: int, end_year: int) -> Optional[Dict]:
    """Get a random popular song from the specified year range"""
    year = random.randint(start_year, end_year)

    # Search for popular songs from that year
    query = f'year:{year}'
    results = sp.search(q=query, type='track', limit=50, market='US')

    if not results['tracks']['items']:
        return None

    # Sort by popularity and pick from top songs
    tracks = sorted(results['tracks']['items'], key=lambda x: x['popularity'], reverse=True)
    top_tracks = tracks[:20]  # Top 20 most popular

    if not top_tracks:
        return None

    track = random.choice(top_tracks)

    # Get album details for release year
    album = sp.album(track['album']['id'])
    release_date = album['release_date']

    # Parse year from release date (format: YYYY-MM-DD or YYYY)
    actual_year = int(release_date.split('-')[0])

    # Get Deezer preview URL (fallback to Spotify if not available)
    deezer_preview = get_deezer_preview(track['name'], track['artists'][0]['name'])
    preview_url = deezer_preview if deezer_preview else track['preview_url']

    return {
        'name': track['name'],
        'artist': track['artists'][0]['name'],
        'album': album['name'],
        'year': actual_year,
        'preview_url': preview_url,
        'image_url': album['images'][0]['url'] if album['images'] else None,
        'spotify_url': track['external_urls']['spotify']
    }


def calculate_score(guess: int, actual: int, time_taken: int, hints_used: int) -> int:
    """Calculate score based on accuracy, time, and hints used"""
    year_diff = abs(guess - actual)

    # Base score on accuracy (max 1000 points)
    if year_diff == 0:
        accuracy_score = 1000
    elif year_diff == 1:
        accuracy_score = 800
    elif year_diff == 2:
        accuracy_score = 600
    elif year_diff <= 3:
        accuracy_score = 400
    elif year_diff <= 5:
        accuracy_score = 200
    else:
        accuracy_score = max(0, 100 - (year_diff * 10))

    # Time bonus (max 300 points - faster is better)
    time_bonus = max(0, 300 - (time_taken * 10))

    # Hint penalty (each hint used reduces score)
    hint_penalty = hints_used * 100

    total_score = max(0, accuracy_score + time_bonus - hint_penalty)
    return int(total_score)


def generate_year_options(actual_year: int) -> List[int]:
    """Generate 4 year options including the correct one"""
    years = {actual_year}

    while len(years) < 4:
        offset = random.randint(-10, 10)
        year = actual_year + offset
        if 1950 <= year <= datetime.now().year:
            years.add(year)

    return sorted(list(years))


def initialize_game_state():
    """Initialize session state variables"""
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False
    if 'current_song' not in st.session_state:
        st.session_state.current_song = None
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'hints_revealed' not in st.session_state:
        st.session_state.hints_revealed = 0
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'player_scores' not in st.session_state:
        st.session_state.player_scores = []
    if 'current_player' not in st.session_state:
        st.session_state.current_player = "Player 1"
    if 'blur_level' not in st.session_state:
        st.session_state.blur_level = 25
    if 'year_options' not in st.session_state:
        st.session_state.year_options = []


def start_new_game(sp, start_year: int, end_year: int):
    """Start a new game round"""
    song = get_random_song(sp, start_year, end_year)

    if song is None:
        st.error("Could not find a song in that year range. Try a different range!")
        return

    st.session_state.current_song = song
    st.session_state.game_active = True
    st.session_state.start_time = time.time()
    st.session_state.hints_revealed = 0
    st.session_state.game_over = False
    st.session_state.blur_level = 25
    st.session_state.year_options = generate_year_options(song['year'])


def reveal_hint():
    """Reveal the next hint"""
    if st.session_state.hints_revealed < 3:
        st.session_state.hints_revealed += 1
        st.session_state.blur_level = max(0, st.session_state.blur_level - 8)


def make_guess(guess_year: int):
    """Process the player's guess"""
    song = st.session_state.current_song
    time_taken = int(time.time() - st.session_state.start_time)

    score = calculate_score(
        guess_year,
        song['year'],
        time_taken,
        st.session_state.hints_revealed
    )

    # Add to player scores
    st.session_state.player_scores.append({
        'player': st.session_state.current_player,
        'song': f"{song['name']} by {song['artist']}",
        'guess': guess_year,
        'actual': song['year'],
        'score': score,
        'time': time_taken
    })

    st.session_state.game_over = True
    st.session_state.blur_level = 0


def render_game_interface(sp):
    """Render the main game interface"""
    song = st.session_state.current_song

    if not song:
        return

    # Calculate elapsed time
    elapsed = int(time.time() - st.session_state.start_time)

    # Display timer
    st.markdown(f'<div class="timer">⏱️ {elapsed}s</div>', unsafe_allow_html=True)

    # Display album artwork with progressive reveal
    if song['image_url']:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            blurred_image = blur_image(song['image_url'], st.session_state.blur_level)
            if blurred_image:
                st.markdown(
                    f'<div style="text-align: center;"><img src="{blurred_image}" width="300" style="border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);"></div>',
                    unsafe_allow_html=True
                )

    st.write("")

    # Audio player
    if song['preview_url']:
        st.audio(song['preview_url'], format='audio/mp3', start_time=0)
    else:
        st.warning("No audio preview available for this song")
        st.markdown(f"[Listen on Spotify]({song['spotify_url']})")

    st.write("")

    # Progressive hints
    hints_container = st.container()
    with hints_container:
        if st.session_state.hints_revealed >= 1:
            st.markdown(f'<div class="hint-box">🎵 <strong>Album:</strong> {song["album"]}</div>', unsafe_allow_html=True)

        if st.session_state.hints_revealed >= 2:
            st.markdown(f'<div class="hint-box">🎤 <strong>Artist:</strong> {song["artist"]}</div>', unsafe_allow_html=True)

        if st.session_state.hints_revealed >= 3:
            st.markdown(f'<div class="hint-box">🎸 <strong>Song:</strong> {song["name"]}</div>', unsafe_allow_html=True)

    st.write("")

    # Hint button
    if not st.session_state.game_over:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.session_state.hints_revealed < 3:
                if st.button(f"💡 Reveal Hint ({st.session_state.hints_revealed}/3)", use_container_width=True):
                    reveal_hint()
                    st.rerun()
            else:
                st.info("All hints revealed!")

    st.write("")
    st.markdown("### 📅 What year was this song released?")

    # Year guessing interface
    if not st.session_state.game_over:
        # Multiple choice buttons
        cols = st.columns(4)
        for idx, year in enumerate(st.session_state.year_options):
            with cols[idx]:
                if st.button(str(year), key=f"year_{year}", use_container_width=True):
                    make_guess(year)
                    st.rerun()

        st.write("")
        st.markdown("##### Or enter a specific year:")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            custom_year = st.number_input(
                "Year",
                min_value=1950,
                max_value=datetime.now().year,
                value=2000,
                step=1,
                label_visibility="collapsed"
            )
            if st.button("Submit Guess", type="primary", use_container_width=True):
                make_guess(custom_year)
                st.rerun()

    # Game over display
    if st.session_state.game_over:
        last_score = st.session_state.player_scores[-1]
        year_diff = abs(last_score['guess'] - last_score['actual'])

        st.markdown('<div class="game-over">', unsafe_allow_html=True)

        if year_diff == 0:
            st.balloons()
            st.markdown("# 🎉 PERFECT!")
            st.markdown(f"## You got it exactly right!")
        elif year_diff <= 2:
            st.markdown("# 🎵 Excellent!")
            st.markdown(f"## Off by only {year_diff} year{'s' if year_diff > 1 else ''}!")
        elif year_diff <= 5:
            st.markdown("# 🎶 Good job!")
            st.markdown(f"## Close! Off by {year_diff} years.")
        else:
            st.markdown("# 🎸 Nice try!")
            st.markdown(f"## Off by {year_diff} years.")

        st.markdown(f"### The correct answer: **{song['year']}**")
        st.markdown('</div>', unsafe_allow_html=True)

        # Score display
        st.markdown(
            f'<div class="score-card">🏆 Score: {last_score["score"]} points</div>',
            unsafe_allow_html=True
        )

        # Reveal all info
        st.markdown("---")
        st.markdown("### 🎵 Song Details")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Song:** {song['name']}")
            st.markdown(f"**Artist:** {song['artist']}")
        with col2:
            st.markdown(f"**Album:** {song['album']}")
            st.markdown(f"**Year:** {song['year']}")

        st.markdown(f"[🎧 Listen on Spotify]({song['spotify_url']})")

        st.markdown("---")

        # Play again button
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎮 Play Again", type="primary", use_container_width=True):
                st.session_state.game_active = False
                st.session_state.game_over = False
                st.rerun()
        with col2:
            if st.button("📊 View Leaderboard", use_container_width=True):
                st.session_state.game_active = False
                st.session_state.game_over = False
                st.rerun()


def render_leaderboard():
    """Display the leaderboard"""
    if not st.session_state.player_scores:
        st.info("No scores yet! Play a game to see your scores here.")
        return

    st.markdown("### 🏆 Leaderboard")

    # Sort by score
    sorted_scores = sorted(
        st.session_state.player_scores,
        key=lambda x: x['score'],
        reverse=True
    )

    for idx, score in enumerate(sorted_scores[:10], 1):
        with st.container():
            st.markdown(
                f"""
                <div class="leaderboard" style="margin: 0.5em 0;">
                    <strong>#{idx} {score['player']}</strong> - {score['score']} points<br>
                    <small>{score['song']} | Guessed: {score['guess']} | Actual: {score['actual']} | Time: {score['time']}s</small>
                </div>
                """,
                unsafe_allow_html=True
            )


def main():
    """Main application"""
    initialize_game_state()

    try:
        sp = get_spotify_client()
    except Exception as e:
        st.error("Error connecting to Spotify. Please check your credentials.")
        st.error(f"Details: {e}")
        return

    # Header
    st.markdown('<h1 class="main-header">🎵 Song Year Guesser 🎵</h1>', unsafe_allow_html=True)

    # Sidebar for settings
    with st.sidebar:
        st.markdown("### ⚙️ Game Settings")

        # Player name
        player_name = st.text_input(
            "Player Name",
            value=st.session_state.current_player,
            max_chars=20
        )
        st.session_state.current_player = player_name

        st.markdown("---")
        st.markdown("### 📅 Year Range")

        start_year = st.slider(
            "Start Year",
            min_value=1950,
            max_value=datetime.now().year - 1,
            value=1980,
        )

        end_year = st.slider(
            "End Year",
            min_value=start_year,
            max_value=datetime.now().year,
            value=2020,
        )

        st.markdown("---")
        st.markdown("### 📊 Stats")

        if st.session_state.player_scores:
            player_games = [s for s in st.session_state.player_scores if s['player'] == player_name]
            if player_games:
                total_score = sum(s['score'] for s in player_games)
                avg_score = total_score // len(player_games)
                st.metric("Games Played", len(player_games))
                st.metric("Total Score", total_score)
                st.metric("Average Score", avg_score)

        st.markdown("---")

        if st.button("🗑️ Clear Leaderboard", use_container_width=True):
            st.session_state.player_scores = []
            st.rerun()

    # Main content
    if not st.session_state.game_active:
        st.markdown("""
        ### 🎮 How to Play

        1. **Listen** to a 30-second song preview
        2. **Watch** the album artwork gradually reveal
        3. **Guess** the year the song was released
        4. **Score** points based on accuracy and speed!

        💡 Use hints to reveal the album, artist, and song title (but you'll lose points!)
        """)

        st.write("")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎵 Start New Game", type="primary", use_container_width=True, key="start_game"):
                start_new_game(sp, start_year, end_year)
                st.rerun()

        st.markdown("---")

        # Show leaderboard
        render_leaderboard()

    else:
        # Game is active
        render_game_interface(sp)


if __name__ == "__main__":
    main()
