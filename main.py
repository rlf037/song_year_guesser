import base64
import io
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

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
st.markdown(
    """
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
        background: transparent;
        border-radius: 15px;
        margin: 1em 0;
    }
    .status-line {
        text-align: center;
        padding: 0.5em 1em;
        background: linear-gradient(90deg, #667eea20 0%, #764ba220 100%);
        border-radius: 8px;
        margin: 0.5em 0;
        font-size: 0.9em;
        color: #667eea;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    .countdown-urgent {
        animation: shake 0.5s infinite;
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-2px); }
        75% { transform: translateX(2px); }
    }
</style>
""",
    unsafe_allow_html=True,
)


COMPILATION_KEYWORDS = [
    "greatest hits",
    "best of",
    "collection",
    "anthology",
    "compilation",
    "essentials",
    "hits",
    "singles",
    "retrospective",
    "very best",
    "ultimate",
    "deluxe",
    "remastered",
    "live",
    "remix",
    "acoustic",
    "version",
    "edition",
    "anniversary",
    "remaster",
    "expanded",
    "bonus",
    "special",
    "complete",
    "definitive",
    "gold",
    "platinum",
    "legend",
    "classic",
    "chronicles",
    "archive",
    "re-issue",
    "reissue",
    "re-release",
    "mono",
    "stereo",
    "digitally",
]

# Minimum Spotify popularity to be considered (0-100 scale)
MIN_SPOTIFY_POPULARITY = 85

# Maximum time allowed for guessing (seconds)
MAX_GUESS_TIME = 60

# List of major English-speaking music markets
ENGLISH_MARKETS = ["US", "GB", "AU", "CA"]


def is_compilation_or_remaster(text: str) -> bool:
    """Check if text suggests it's a compilation, remaster, or special edition"""
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in COMPILATION_KEYWORDS)


def strip_numbers_from_title(title: str) -> str:
    """Remove all numbers from song title to prevent year leaks"""
    return re.sub(r"\d+", "", title)


def get_spotify_token() -> str | None:
    """Get Spotify access token using client credentials flow"""
    try:
        client_id = st.secrets["spotify"]["client_id"]
        client_secret = st.secrets["spotify"]["client_secret"]
    except Exception:
        return None

    # Check if we have a cached valid token
    if (
        "spotify_token" in st.session_state
        and "spotify_token_expires" in st.session_state
        and time.time() < st.session_state.spotify_token_expires
    ):
        return st.session_state.spotify_token

    # Get new token
    try:
        auth_str = f"{client_id}:{client_secret}"
        auth_b64 = base64.b64encode(auth_str.encode()).decode()

        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={"Authorization": f"Basic {auth_b64}"},
            data={"grant_type": "client_credentials"},
            timeout=10,
        )

        if response.status_code == 200:
            data = response.json()
            st.session_state.spotify_token = data["access_token"]
            st.session_state.spotify_token_expires = time.time() + data["expires_in"] - 60
            return data["access_token"]
    except Exception:
        pass

    return None


def get_deezer_preview(artist: str, track: str) -> str | None:
    """Find a Deezer preview URL for a song"""
    try:
        query = f"{artist} {track}"
        search_url = f"https://api.deezer.com/search?q={requests.utils.quote(query)}&limit=5"
        response = requests.get(search_url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            for result in data.get("data", []):
                if result.get("preview"):
                    return result["preview"]
    except Exception:
        pass

    return None


# Cache for playlist IDs (year -> playlist_id)
_playlist_cache: dict[int, str | None] = {}
# Cache for tracks by year
_tracks_cache: dict[int, list[dict]] = {}
# Cache for blurred images (url + blur_amount -> base64)
_image_cache: dict[str, str] = {}


def search_top_hits_playlist(year: int, token: str) -> str | None:
    """
    Search for Spotify's official "Top Hits of [Year]" playlist.
    Returns the playlist ID if found. Uses cache to avoid repeated API calls.
    """
    # Check cache first
    if year in _playlist_cache:
        return _playlist_cache[year]

    headers = {"Authorization": f"Bearer {token}"}

    # Single optimized search query
    try:
        query = f"Top Hits {year}"
        search_url = f"https://api.spotify.com/v1/search?q={requests.utils.quote(query)}&type=playlist&limit=20"
        response = requests.get(search_url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            playlists = data.get("playlists", {}).get("items", [])

            # First pass: look for Spotify official playlists
            for playlist in playlists:
                if not playlist:
                    continue
                name = playlist.get("name", "").lower()
                owner = playlist.get("owner", {}).get("display_name", "").lower()

                if "spotify" in owner and str(year) in name:
                    _playlist_cache[year] = playlist["id"]
                    return playlist["id"]

            # Second pass: accept good community playlists
            for playlist in playlists:
                if not playlist:
                    continue
                name = playlist.get("name", "").lower()
                if "top" in name and str(year) in name and ("hit" in name or "100" in name):
                    _playlist_cache[year] = playlist["id"]
                    return playlist["id"]
    except Exception:
        pass

    _playlist_cache[year] = None
    return None


def is_likely_english(track_name: str, artist_name: str) -> bool:
    """Check if track is likely English based on character analysis"""
    text = f"{track_name} {artist_name}"
    # Check for non-Latin characters (CJK, Cyrillic, Arabic, Hebrew, Thai, Korean, etc.)
    non_latin_pattern = re.compile(
        r"[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\u0400-\u04ff\u0600-\u06ff\u0e00-\u0e7f\uac00-\ud7af\u0590-\u05ff]"
    )
    if non_latin_pattern.search(text):
        return False
    # Check for excessive accented characters (might be Spanish, Portuguese, French, etc.)
    accented_count = len(re.findall(r"[àáâãäåèéêëìíîïòóôõöùúûüñçøæœßðþ]", text.lower()))
    if len(text) > 0 and accented_count > len(text) * 0.1:  # More than 10% accented chars
        return False
    # Check for common non-English title patterns
    non_english_patterns = [
        r"\b(el|la|los|las|del|de la)\b",  # Spanish
        r"\b(le|la|les|du|de la|des)\b",  # French
        r"\b(der|die|das|ein|eine)\b",  # German
        r"\b(il|lo|la|gli|le|del|della)\b",  # Italian
        r"\b(o|a|os|as|do|da|dos|das)\b",  # Portuguese
    ]
    text_lower = text.lower()
    for pattern in non_english_patterns:
        # Only flag if it looks like a title with multiple matches
        if re.search(pattern, text_lower) and len(re.findall(pattern, text_lower)) > 1:
            return False
    return True


def get_songs_from_spotify(year: int) -> list[dict]:
    """
    Get top 100 chart songs from a specific year using Spotify's Top Hits playlists.
    Returns songs that actually charted that year. Uses cache.
    """
    # Check cache first
    if year in _tracks_cache:
        return _tracks_cache[year]

    token = get_spotify_token()
    if not token:
        return []

    headers = {"Authorization": f"Bearer {token}"}
    tracks = []

    # First try to find the Top Hits playlist for this year
    playlist_id = search_top_hits_playlist(year, token)

    if playlist_id:
        # Get tracks from the playlist
        try:
            playlist_url = (
                f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=100&market=US"
            )
            response = requests.get(playlist_url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                for item in data.get("items", []):
                    track = item.get("track")
                    if not track:
                        continue

                    album = track.get("album", {})
                    track_name = track.get("name", "")
                    album_name = album.get("name", "")

                    # Skip compilations and remasters
                    if is_compilation_or_remaster(album_name) or is_compilation_or_remaster(
                        track_name
                    ):
                        continue

                    # Get artist name
                    artists = track.get("artists", [])
                    artist_name = artists[0]["name"] if artists else "Unknown"

                    # Skip non-English songs
                    if not is_likely_english(track_name, artist_name):
                        continue

                    # Filter by popularity (even from playlists)
                    popularity = track.get("popularity", 0)
                    if popularity < MIN_SPOTIFY_POPULARITY:
                        continue

                    # Get album artwork
                    images = album.get("images", [])
                    image_url = images[0]["url"] if images else None

                    # Get release year from album
                    release_date = album.get("release_date", "")
                    album_year = int(release_date[:4]) if len(release_date) >= 4 else year

                    tracks.append(
                        {
                            "id": track["id"],
                            "name": track_name,
                            "artist": artist_name,
                            "album": album_name,
                            "year": year,  # Use the chart year, not album year
                            "image_url": image_url,
                            "popularity": popularity,
                            "spotify_id": track["id"],
                        }
                    )
        except Exception:
            pass

    # Fallback: search for popular tracks from that year
    if not tracks:
        try:
            search_url = (
                f"https://api.spotify.com/v1/search?q=year:{year}&type=track&limit=50&market=US"
            )
            response = requests.get(search_url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                for item in data.get("tracks", {}).get("items", []):
                    album = item["album"]
                    release_date = album.get("release_date", "")

                    if len(release_date) >= 4:
                        album_year = int(release_date[:4])
                        if album_year != year:
                            continue

                    album_name = album.get("name", "")
                    track_name = item.get("name", "")
                    if is_compilation_or_remaster(album_name) or is_compilation_or_remaster(
                        track_name
                    ):
                        continue

                    popularity = item.get("popularity", 0)
                    if popularity < MIN_SPOTIFY_POPULARITY:
                        continue

                    artists = item.get("artists", [])
                    artist_name = artists[0]["name"] if artists else "Unknown"

                    # Skip non-English songs
                    if not is_likely_english(track_name, artist_name):
                        continue

                    images = album.get("images", [])
                    image_url = images[0]["url"] if images else None

                    tracks.append(
                        {
                            "id": item["id"],
                            "name": track_name,
                            "artist": artist_name,
                            "album": album_name,
                            "year": year,
                            "image_url": image_url,
                            "popularity": popularity,
                            "spotify_id": item["id"],
                        }
                    )
        except Exception:
            pass

    # Sort by popularity
    tracks.sort(key=lambda x: x.get("popularity", 0), reverse=True)

    result = tracks[:50]  # Return top 50 for variety
    _tracks_cache[year] = result
    return result


def _fetch_deezer_preview(track: dict) -> tuple[dict, str | None]:
    """Helper to fetch Deezer preview for a track (used in parallel)"""
    preview_url = get_deezer_preview(track["artist"], track["name"])
    return (track, preview_url)


def get_random_song(start_year: int, end_year: int) -> dict | None:
    """Get a random popular song from the specified year range using Spotify + Deezer"""
    years_to_try = list(range(start_year, end_year + 1))
    random.shuffle(years_to_try)

    for year in years_to_try[:3]:  # Try up to 3 years (reduced for speed)
        tracks = get_songs_from_spotify(year)

        if not tracks:
            continue

        # Shuffle and pick candidates
        random.shuffle(tracks)
        candidates = tracks[:8]  # Check 8 tracks in parallel

        # Fetch Deezer previews in parallel for speed
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(_fetch_deezer_preview, t): t for t in candidates}

            for future in as_completed(futures):
                try:
                    track, preview_url = future.result()
                    if preview_url:
                        # Cancel remaining futures
                        for f in futures:
                            f.cancel()
                        return {
                            "id": track["id"],
                            "name": strip_numbers_from_title(track["name"]),
                            "artist": track["artist"],
                            "album": track["album"],
                            "year": track["year"],
                            "preview_url": preview_url,
                            "image_url": track["image_url"],
                            "deezer_url": f"https://open.spotify.com/track/{track['spotify_id']}",
                        }
                except Exception:
                    continue

    return None


def blur_image(image_url: str, blur_amount: int) -> str:
    """Download image and apply blur effect, return as base64. Uses cache for performance."""
    cache_key = f"{image_url}_{blur_amount}"

    # Check cache first
    if cache_key in _image_cache:
        return _image_cache[cache_key]

    try:
        # Check if we have the original image cached
        original_key = f"{image_url}_original"
        if original_key in _image_cache:
            img_data = base64.b64decode(_image_cache[original_key])
            img = Image.open(io.BytesIO(img_data))
        else:
            response = requests.get(image_url, timeout=5)
            img = Image.open(io.BytesIO(response.content))
            # Cache original
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            _image_cache[original_key] = base64.b64encode(buffered.getvalue()).decode()

        if blur_amount > 0:
            img = img.filter(ImageFilter.GaussianBlur(radius=blur_amount))

        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        result = f"data:image/png;base64,{img_str}"

        # Cache the result
        _image_cache[cache_key] = result
        return result
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return ""


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


def generate_year_options(actual_year: int) -> list[int]:
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
    if "game_active" not in st.session_state:
        st.session_state.game_active = False
    if "current_song" not in st.session_state:
        st.session_state.current_song = None
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "hints_revealed" not in st.session_state:
        st.session_state.hints_revealed = 0
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "player_scores" not in st.session_state:
        st.session_state.player_scores = []
    if "current_player" not in st.session_state:
        st.session_state.current_player = "Player 1"
    if "blur_level" not in st.session_state:
        st.session_state.blur_level = 25
    if "year_options" not in st.session_state:
        st.session_state.year_options = []
    if "start_year" not in st.session_state:
        st.session_state.start_year = 1995
    if "end_year" not in st.session_state:
        st.session_state.end_year = 2010
    if "current_round" not in st.session_state:
        st.session_state.current_round = 0
    if "session_scores" not in st.session_state:
        st.session_state.session_scores = []
    if "audio_started" not in st.session_state:
        st.session_state.audio_started = False
    if "song_loaded_time" not in st.session_state:
        st.session_state.song_loaded_time = None
    if "timed_out" not in st.session_state:
        st.session_state.timed_out = False
    if "status_message" not in st.session_state:
        st.session_state.status_message = ""


def start_new_game(start_year: int, end_year: int):
    """Start a new game round"""
    # Show loading state
    st.session_state.status_message = "🔍 Searching for a song..."

    song = get_random_song(start_year, end_year)

    if song is None:
        st.error("Could not find a song in that year range. Try a different range!")
        st.session_state.status_message = ""
        return

    # Preload and cache the album image at max blur
    if song.get("image_url"):
        st.session_state.status_message = "🎨 Loading album artwork..."
        blur_image(song["image_url"], 25)  # Pre-cache blurred version
        blur_image(song["image_url"], 0)  # Pre-cache clear version

    # Increment round counter
    st.session_state.current_round += 1

    st.session_state.current_song = song
    st.session_state.game_active = True
    st.session_state.start_time = time.time()  # Timer starts immediately
    st.session_state.hints_revealed = 0
    st.session_state.game_over = False
    st.session_state.timed_out = False
    st.session_state.blur_level = 25
    st.session_state.year_options = generate_year_options(song["year"])
    st.session_state.audio_started = True  # Audio auto-plays
    st.session_state.song_loaded_time = time.time()
    st.session_state.status_message = "🎵 Listening... make your guess!"


def reveal_hint():
    """Reveal the next hint"""
    if st.session_state.hints_revealed < 3:
        st.session_state.hints_revealed += 1
        st.session_state.blur_level = max(0, st.session_state.blur_level - 8)


def make_guess(guess_year: int, timed_out: bool = False):
    """Process the player's guess"""
    song = st.session_state.current_song

    if st.session_state.start_time:
        time_taken = int(time.time() - st.session_state.start_time)
    else:
        time_taken = 0

    if timed_out:
        score = 0
        st.session_state.timed_out = True
    else:
        score = calculate_score(
            guess_year, song["year"], time_taken, st.session_state.hints_revealed
        )

    # Add to player scores
    st.session_state.player_scores.append(
        {
            "player": st.session_state.current_player,
            "song": f"{song['name']} by {song['artist']}",
            "guess": guess_year if not timed_out else "TIMEOUT",
            "actual": song["year"],
            "score": score,
            "time": time_taken,
        }
    )

    st.session_state.game_over = True
    st.session_state.blur_level = 0
    st.session_state.status_message = ""


def render_game_interface():
    """Render the main game interface"""
    song = st.session_state.current_song

    if not song:
        return

    # Auto-refresh every 1 second to update timer (100ms causes UI blocking)
    if not st.session_state.game_over and st.session_state.audio_started:
        st_autorefresh(interval=1000, key="game_timer")

    # Display round counter
    st.markdown(f"### 🎮 Round {st.session_state.current_round}")

    # Calculate elapsed time
    if st.session_state.start_time is not None:
        elapsed_float = time.time() - st.session_state.start_time
        elapsed_seconds = int(elapsed_float)
        elapsed = elapsed_seconds  # For blur calculation
    else:
        elapsed_float = 0
        elapsed_seconds = 0
        elapsed = 0

    # Check for timeout (60 seconds max)
    if (
        not st.session_state.game_over
        and st.session_state.audio_started
        and elapsed_seconds >= MAX_GUESS_TIME
    ):
        make_guess(0, timed_out=True)
        st.rerun()

    # Display timer counting UP
    if st.session_state.audio_started and not st.session_state.game_over:
        if elapsed_seconds >= 50:
            timer_class = "timer countdown-urgent"
            timer_color = "#ff4444"
        elif elapsed_seconds >= 40:
            timer_color = "#ff8844"
            timer_class = "timer"
        else:
            timer_color = "#667eea"
            timer_class = "timer"
        st.markdown(
            f'<div class="{timer_class}" style="color: {timer_color};">⏱️ {elapsed_seconds}s</div>',
            unsafe_allow_html=True,
        )
    elif not st.session_state.game_over:
        st.markdown(
            '<div class="timer" style="color: #667eea;">⏱️ 0s</div>',
            unsafe_allow_html=True,
        )

    # Status line with styled message
    if st.session_state.status_message and not st.session_state.game_over:
        st.markdown(
            f'<div class="status-line">{st.session_state.status_message}</div>',
            unsafe_allow_html=True,
        )

    # Calculate progressive blur based on time (starts at 25, decreases to 0 over 30 seconds)
    if not st.session_state.game_over:
        if st.session_state.audio_started:
            # Gradually reduce blur over 30 seconds
            time_based_blur = max(0, 25 - (elapsed * 25 / 30))
            current_blur = min(st.session_state.blur_level, time_based_blur)
        else:
            current_blur = st.session_state.blur_level
    else:
        current_blur = 0

    # Display album artwork with progressive reveal
    if song["image_url"]:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            blurred_image = blur_image(song["image_url"], int(current_blur))
            if blurred_image:
                st.markdown(
                    f'<div style="text-align: center;"><img src="{blurred_image}" width="300" style="border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);"></div>',
                    unsafe_allow_html=True,
                )

    st.write("")

    # Audio player with autoplay
    if song["preview_url"]:
        if not st.session_state.game_over:
            # During gameplay - autoplay
            audio_html = f'''
            <html>
            <body style="margin:0; padding:0; background: transparent;">
            <audio id="gameAudio" controls autoplay style="width: 100%; border-radius: 10px;">
                <source src="{song["preview_url"]}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
            <script>
                var audio = document.getElementById('gameAudio');
                audio.volume = 1.0;
                audio.play().catch(function(e) {{
                    console.log('Autoplay prevented:', e);
                }});
            </script>
            </body>
            </html>
            '''
            components.html(audio_html, height=60)
        else:
            # After guess - styled player without autoplay
            audio_html = f'''
            <html>
            <body style="margin:0; padding:10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px;">
            <audio id="gameAudio" controls style="width: 100%; border-radius: 8px;">
                <source src="{song["preview_url"]}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
            </body>
            </html>
            '''
            components.html(audio_html, height=70)
    else:
        st.warning("No audio preview available for this song")
        st.markdown(f"[Listen on Spotify]({song['deezer_url']})")

    st.write("")

    # Progressive hints
    if st.session_state.hints_revealed > 0:
        hints_container = st.container()
        with hints_container:
            if st.session_state.hints_revealed >= 1:
                st.markdown(
                    f'<div class="hint-box">🎵 <strong>Album:</strong> {song["album"]}</div>',
                    unsafe_allow_html=True,
                )

            if st.session_state.hints_revealed >= 2:
                st.markdown(
                    f'<div class="hint-box">🎤 <strong>Artist:</strong> {song["artist"]}</div>',
                    unsafe_allow_html=True,
                )

            if st.session_state.hints_revealed >= 3:
                st.markdown(
                    f'<div class="hint-box">🎸 <strong>Song:</strong> {song["name"]}</div>',
                    unsafe_allow_html=True,
                )

    # Hint button (show during active gameplay)
    if not st.session_state.game_over:
        st.write("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.session_state.hints_revealed < 3:
                hint_labels = ["Album", "Artist", "Song Title"]
                next_hint = hint_labels[st.session_state.hints_revealed]
                if st.button(
                    f"💡 Reveal {next_hint} ({st.session_state.hints_revealed}/3 hints used)",
                    use_container_width=True,
                    key=f"hint_btn_{st.session_state.hints_revealed}",
                ):
                    reveal_hint()
                    st.session_state.status_message = f"💡 {next_hint} revealed! (-100 points)"
                    st.rerun()
            else:
                st.markdown(
                    '<div class="status-line">All hints revealed!</div>', unsafe_allow_html=True
                )

    st.write("")

    # Year guessing interface with slider
    if not st.session_state.game_over:
        st.markdown("### 📅 What year was this song released?")

        guess_year = st.slider(
            "Year",
            min_value=st.session_state.start_year,
            max_value=st.session_state.end_year,
            value=st.session_state.start_year,
            step=1,
            key="guess_slider",
            label_visibility="collapsed",
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "🎯 Submit Guess", type="primary", use_container_width=True, key="submit_guess"
            ):
                make_guess(guess_year)
                st.rerun()

    # Game over display
    if st.session_state.game_over:
        last_score = st.session_state.player_scores[-1]

        st.markdown('<div class="game-over">', unsafe_allow_html=True)

        if st.session_state.timed_out:
            st.markdown("# ⏰ TIME'S UP!")
            st.markdown("## You ran out of time!")
        else:
            guess_val = last_score["guess"]
            if isinstance(guess_val, int):
                year_diff = abs(guess_val - last_score["actual"])

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
        st.markdown("</div>", unsafe_allow_html=True)

        # Score display
        st.markdown(
            f'<div class="score-card">Score: {last_score["score"]} points</div>',
            unsafe_allow_html=True,
        )

        # Reveal all info
        st.markdown("---")
        st.markdown("### Song Details")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Song:** {song['name']}")
            st.markdown(f"**Artist:** {song['artist']}")
        with col2:
            st.markdown(f"**Album:** {song['album']}")
            st.markdown(f"**Year:** {song['year']}")

        st.markdown(f"[Listen on Spotify]({song['deezer_url']})")

        st.markdown("---")

        # Next song and end game buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Next Song", type="primary", use_container_width=True, key="next_song"):
                start_new_game(st.session_state.start_year, st.session_state.end_year)
                st.rerun()
        with col2:
            if st.button("🏁 End Game", use_container_width=True, key="end_game"):
                st.session_state.game_active = False
                st.session_state.game_over = False
                st.session_state.current_round = 0
                st.rerun()


def render_leaderboard():
    """Display the leaderboard"""
    if not st.session_state.player_scores:
        st.info("No scores yet! Play a game to see your scores here.")
        return

    st.markdown("### 🏆 Leaderboard")

    # Sort by score
    sorted_scores = sorted(st.session_state.player_scores, key=lambda x: x["score"], reverse=True)

    for idx, score in enumerate(sorted_scores[:10], 1):
        guess_display = score["guess"] if isinstance(score["guess"], int) else "TIMEOUT"
        with st.container():
            st.markdown(
                f"""
                <div class="leaderboard" style="margin: 0.5em 0;">
                    <strong>#{idx} {score["player"]}</strong> - {score["score"]} points<br>
                    <small>{score["song"]} | Guessed: {guess_display} | Actual: {score["actual"]} | Time: {score["time"]}s</small>
                </div>
                """,
                unsafe_allow_html=True,
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
            "Player Name", value=st.session_state.current_player, max_chars=20
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
            player_games = [s for s in st.session_state.player_scores if s["player"] == player_name]
            if player_games:
                total_score = sum(s["score"] for s in player_games)
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
            if st.button(
                "🎵 Start New Game", type="primary", use_container_width=True, key="start_game"
            ):
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
