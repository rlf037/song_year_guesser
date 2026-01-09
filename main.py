import base64
import io
import random
import re
import time
from datetime import datetime
from typing import Dict, List, Optional

import requests
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageFilter
from streamlit_autorefresh import st_autorefresh

# Page configuration
st.set_page_config(
    page_title="Song Year Game",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="expanded",
)
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
        color: #262730;
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
        color: #262730;
    }
    .game-over {
        text-align: center;
        font-size: 1.5em;
        padding: 2em;
        background: #f0f2f6;
        border-radius: 15px;
        margin: 1em 0;
    }
    .stSlider {
        padding-top: 0;
        margin-top: 0;
    }
    .stSlider > div {
        background: transparent !important;
    }
    .stSlider > div > div {
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)


COMPILATION_KEYWORDS = [
    'greatest hits', 'best of', 'collection', 'anthology',
    'compilation', 'essentials', 'hits', 'singles',
    'retrospective', 'very best', 'ultimate', 'deluxe', 'remastered',
    'live', 'remix', 'acoustic', 'version', 'edition', 'anniversary', 'remaster'
]

# Minimum Deezer rank to be considered a "popular" song
# Deezer rank is based on total plays - higher = more popular
# 200,000+ filters out very obscure songs while allowing popular tracks
MIN_POPULARITY_RANK = 200000


def is_compilation_or_remaster(text: str) -> bool:
    """Check if text suggests it's a compilation, remaster, or special edition"""
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in COMPILATION_KEYWORDS)


def strip_numbers_from_title(title: str) -> str:
    """Remove all numbers from song title to prevent year leaks"""
    return re.sub(r'\d+', '', title)


def get_popular_songs_by_year(year: int) -> List[Dict]:
    """
    Get popular songs from a specific year using Deezer API.
    Uses multiple search strategies to find 50-100+ genuinely popular tracks.
    """
    all_tracks = {}  # Use dict to dedupe by track ID
    
    # Strategy 1: Search by year with high limit
    try:
        search_url = f"https://api.deezer.com/search?q=year:{year}&limit=100"
        response = requests.get(search_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for track in data.get('data', []):
                if track['id'] not in all_tracks:
                    all_tracks[track['id']] = track
    except Exception:
        pass
    
    # Strategy 2: Search popular genre terms + year (expanded list)
    genres = ['pop', 'rock', 'hip hop', 'r&b', 'dance', 'electronic', 'indie', 
              'country', 'latin', 'soul', 'disco', 'funk', 'alternative', 'metal']
    for genre in genres:
        try:
            search_url = f"https://api.deezer.com/search?q={genre} {year}&limit=50"
            response = requests.get(search_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for track in data.get('data', []):
                    if track['id'] not in all_tracks:
                        all_tracks[track['id']] = track
        except Exception:
            pass
    
    # Strategy 3: Search by "hits" + year and "best" + year
    for term in ['hits', 'best', 'top', 'chart']:
        try:
            search_url = f"https://api.deezer.com/search?q={term} {year}&limit=50"
            response = requests.get(search_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for track in data.get('data', []):
                    if track['id'] not in all_tracks:
                        all_tracks[track['id']] = track
        except Exception:
            pass
    
    # Filter tracks: must have preview, high popularity rank, not a compilation
    valid_tracks = []
    for track in all_tracks.values():
        album_title = track['album']['title']
        song_title = track['title']
        rank = track.get('rank', 0)
        
        # Only include songs with high popularity rank
        if (track.get('preview') and 
            rank >= MIN_POPULARITY_RANK and
            not is_compilation_or_remaster(album_title) and 
            not is_compilation_or_remaster(song_title)):
            valid_tracks.append({
                'id': track['id'],
                'name': strip_numbers_from_title(track['title']),
                'artist': track['artist']['name'],
                'album': album_title,
                'preview_url': track['preview'],
                'image_url': track['album'].get('cover_xl') or track['album'].get('cover_big'),
                'release_date': track.get('release_date', str(year)),
                'rank': rank
            })
    
    return valid_tracks


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


def get_random_song(start_year: int, end_year: int) -> Optional[Dict]:
    """Get a random popular song from the specified year range using Deezer"""
    # Shuffle all years in range to try them randomly
    years_to_try = list(range(start_year, end_year + 1))
    random.shuffle(years_to_try)
    
    # Try each year until we find songs
    for year in years_to_try[:10]:  # Limit to 10 attempts for performance
        # Get popular songs from Deezer
        tracks = get_popular_songs_by_year(year)

        if not tracks:
            continue

        # Sort by rank (popularity) and pick from top 30 most popular for variety
        tracks_sorted = sorted(tracks, key=lambda x: x.get('rank', 0), reverse=True)
        top_tracks = tracks_sorted[:30]

        if not top_tracks:
            continue

        track = random.choice(top_tracks)

        # Parse year from release date
        release_date = track['release_date']
        try:
            if '-' in release_date:
                actual_year = int(release_date.split('-')[0])
            else:
                actual_year = int(release_date) if release_date.isdigit() else year
        except:  # noqa: E722
            actual_year = year

        return {
            'id': track['id'],
            'name': track['name'],
            'artist': track['artist'],
            'album': track['album'],
            'year': actual_year,
            'preview_url': track['preview_url'],
            'image_url': track['image_url'],
            'spotify_url': f"https://www.deezer.com/track/{track['id']}"
        }
    
    # Fallback: if no popular songs found, get ANY song with a preview from the year range
    for year in years_to_try[:5]:
        try:
            search_url = f"https://api.deezer.com/search?q=year:{year}&limit=50"
            response = requests.get(search_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Filter: must have preview and not be a compilation/remaster
                tracks = [t for t in data.get('data', []) 
                         if t.get('preview') 
                         and not is_compilation_or_remaster(t['album']['title'])
                         and not is_compilation_or_remaster(t['title'])]
                if tracks:
                    # Sort by rank and pick from top
                    tracks_sorted = sorted(tracks, key=lambda x: x.get('rank', 0), reverse=True)
                    track = tracks_sorted[0]  # Get most popular available
                    
                    album_title = track['album']['title']
                    return {
                        'id': track['id'],
                        'name': strip_numbers_from_title(track['title']),
                        'artist': track['artist']['name'],
                        'album': album_title,
                        'year': year,
                        'preview_url': track['preview'],
                        'image_url': track['album'].get('cover_xl') or track['album'].get('cover_big'),
                        'spotify_url': f"https://www.deezer.com/track/{track['id']}"
                    }
        except Exception:
            pass
    
    return None


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
    if 'start_year' not in st.session_state:
        st.session_state.start_year = 1995
    if 'end_year' not in st.session_state:
        st.session_state.end_year = 2010
    if 'current_round' not in st.session_state:
        st.session_state.current_round = 0
    if 'session_scores' not in st.session_state:
        st.session_state.session_scores = []
    if 'audio_started' not in st.session_state:
        st.session_state.audio_started = False
    if 'song_loaded_time' not in st.session_state:
        st.session_state.song_loaded_time = None


def start_new_game(start_year: int, end_year: int):
    """Start a new game round"""
    song = get_random_song(start_year, end_year)

    if song is None:
        st.error("Could not find a song in that year range. Try a different range!")
        return

    # Increment round counter
    st.session_state.current_round += 1

    st.session_state.current_song = song
    st.session_state.game_active = True
    st.session_state.start_time = None  # Don't start timer yet
    st.session_state.hints_revealed = 0
    st.session_state.game_over = False
    st.session_state.blur_level = 25
    st.session_state.year_options = generate_year_options(song['year'])
    st.session_state.audio_started = False
    st.session_state.song_loaded_time = time.time()  # Track when song loaded


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


def render_game_interface():
    """Render the main game interface"""
    song = st.session_state.current_song

    if not song:
        return

    # Auto-refresh every second to update timer (only when game is active)
    if not st.session_state.game_over:
        st_autorefresh(interval=1000, key="game_timer")

    # Initialize timer immediately when song loads
    if st.session_state.start_time is None and st.session_state.song_loaded_time is not None:
        st.session_state.start_time = time.time()

    # Display round counter
    st.markdown(f"### 🎮 Round {st.session_state.current_round}")

    # Calculate elapsed time and display timer
    if st.session_state.start_time is not None:
        elapsed = int(time.time() - st.session_state.start_time)
    else:
        elapsed = 0  # Show 0 during the 2-second delay

    # Display timer
    st.markdown(f'<div class="timer">⏱️ {elapsed}s</div>', unsafe_allow_html=True)

    # Calculate progressive blur based on time (starts at 25, decreases to 0 over 30 seconds)
    if not st.session_state.game_over:
        # Gradually reduce blur over 30 seconds
        time_based_blur = max(0, 25 - (elapsed * 25 / 30))
        current_blur = min(st.session_state.blur_level, time_based_blur)
    else:
        current_blur = 0

    # Display album artwork with progressive reveal
    if song['image_url']:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            blurred_image = blur_image(song['image_url'], int(current_blur))
            if blurred_image:
                st.markdown(
                    f'<div style="text-align: center;"><img src="{blurred_image}" width="300" style="border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);"></div>',
                    unsafe_allow_html=True
                )

    st.write("")

    # Audio player - only show and autoplay when game is active (not after guess)
    if song['preview_url'] and not st.session_state.game_over:
        audio_html = f'''
        <html>
        <body style="margin:0; padding:0;">
        <audio id="gameAudio" controls autoplay style="width: 100%;">
            <source src="{song['preview_url']}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        <script>
            var audio = document.getElementById('gameAudio');
            audio.volume = 1.0;
            audio.play();
        </script>
        </body>
        </html>
        '''
        components.html(audio_html, height=60)
    elif not song['preview_url']:
        st.warning("No audio preview available for this song")
        st.markdown(f"[Listen on Deezer]({song['spotify_url']})")

    st.write("")

    # Progressive hints (only show during active gameplay, hide after guess)
    if not st.session_state.game_over and st.session_state.hints_revealed > 0:
        hints_container = st.container()
        with hints_container:
            if st.session_state.hints_revealed >= 1:
                st.markdown(f'<div class="hint-box">🎵 <strong>Album:</strong> {song["album"]}</div>', unsafe_allow_html=True)

            if st.session_state.hints_revealed >= 2:
                st.markdown(f'<div class="hint-box">🎤 <strong>Artist:</strong> {song["artist"]}</div>', unsafe_allow_html=True)

            if st.session_state.hints_revealed >= 3:
                st.markdown(f'<div class="hint-box">🎸 <strong>Song:</strong> {song["name"]}</div>', unsafe_allow_html=True)

    # Hint button (only show during active gameplay)
    if not st.session_state.game_over:
        st.write("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.session_state.hints_revealed < 3:
                if st.button(f"💡 Reveal Hint ({st.session_state.hints_revealed}/3)", use_container_width=True):
                    reveal_hint()
                    st.rerun()
            else:
                st.info("All hints revealed!")

    st.write("")

    # Year guessing interface with slider (constrained to sidebar year range)
    if not st.session_state.game_over:
        st.markdown("### 📅 What year was this song released?")

        guess_year = st.slider(
            "Year",
            min_value=st.session_state.start_year,
            max_value=st.session_state.end_year,
            value=st.session_state.start_year,
            step=1,
            key="guess_slider",
            label_visibility="collapsed"
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎯 Submit Guess", type="primary", use_container_width=True, key="submit_guess"):
                make_guess(guess_year)
                st.rerun()

    # Game over display
    if st.session_state.game_over:
        last_score = st.session_state.player_scores[-1]
        year_diff = abs(last_score['guess'] - last_score['actual'])

        st.markdown('<div class="game-over">', unsafe_allow_html=True)

        if year_diff == 0:
            st.balloons()
            st.markdown("# 🎉 PERFECT!")
            st.markdown("## You got it exactly right!")
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

        st.markdown(f"[🎧 Listen on Deezer]({song['spotify_url']})")

        st.markdown("---")

        # Next song and end game buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Next Song", type="primary", use_container_width=True, key="next_song"):
                # Load a new song in the same game session
                start_new_game(st.session_state.start_year, st.session_state.end_year)
                st.rerun()
        with col2:
            if st.button("🏁 End Game", use_container_width=True, key="end_game"):
                st.session_state.game_active = False
                st.session_state.game_over = False
                st.session_state.current_round = 0  # Reset round counter
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
            value=st.session_state.start_year,
        )

        end_year = st.slider(
            "End Year",
            min_value=start_year,
            max_value=datetime.now().year,
            value=st.session_state.end_year,
        )

        # Update session state when sliders change
        st.session_state.start_year = start_year
        st.session_state.end_year = end_year

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
                st.session_state.current_round = 0  # Reset for new game
                start_new_game(start_year, end_year)
                st.rerun()

        st.markdown("---")

        # Show leaderboard
        render_leaderboard()

    else:
        # Game is active
        render_game_interface()


if __name__ == "__main__":
    main()
