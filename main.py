import base64
import io
import json
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta

import requests
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageFilter
from streamlit_autorefresh import st_autorefresh

# Supabase for persistent leaderboard
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

# Import UI components
from ui_components import (
    MAIN_CSS,
    album_image,
    audio_player,
    audio_visualizer,
    correct_answer_with_diff,
    elapsed_time_receiver,
    empty_leaderboard,
    game_header,
    get_elapsed_time_js,
    how_to_play,
    leaderboard_entry,
    leaderboard_header,
    main_title,
    result_display,
    score_card,
    scroll_wheel_year_picker,
    song_history_item,
    song_info_card,
    spotify_button,
    static_timer,
    timer_html,
)

# Page configuration - centered layout for cleaner look
st.set_page_config(
    page_title="Song Year Guesser",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.markdown(MAIN_CSS, unsafe_allow_html=True)


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

MIN_SPOTIFY_POPULARITY = 50  # Lower threshold for more song variety
MAX_GUESS_TIME = 30
HINT_REVEAL_TIME = 25

# Genre configuration with golden age years for each genre
GENRE_CONFIG = {
    "All Genres": {
        "query": "",  # Empty means no genre filter
        "best_years": (1995, 2020),
        "icon": "🎵",
    },
    "Pop": {
        "query": "pop",
        "best_years": (1985, 2000),
        "icon": "🎤",
    },
    "Rock": {
        "query": "rock",
        "best_years": (1968, 1985),
        "icon": "🎸",
    },
    "Hip-Hop": {
        "query": "hip hop rap",
        "best_years": (1994, 2009),
        "icon": "🎧",
    },
    "R&B": {
        "query": "r&b soul",
        "best_years": (1990, 2005),
        "icon": "💜",
    },
    "Electronic": {
        "query": "electronic dance edm",
        "best_years": (1998, 2013),
        "icon": "🎹",
    },
    "Country": {
        "query": "country",
        "best_years": (1990, 2005),
        "icon": "🤠",
    },
    "Alternative": {
        "query": "alternative indie",
        "best_years": (1991, 2006),
        "icon": "🎪",
    },
    "Metal": {
        "query": "metal heavy",
        "best_years": (1983, 1998),
        "icon": "🤘",
    },
    "Disco/Funk": {
        "query": "disco funk",
        "best_years": (1975, 1985),
        "icon": "🕺",
    },
    "80s": {
        "query": "80s hits",
        "best_years": (1980, 1989),
        "icon": "📼",
    },
}

GENRE_LIST = list(GENRE_CONFIG.keys())


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

    if (
        "spotify_token" in st.session_state
        and "spotify_token_expires" in st.session_state
        and time.time() < st.session_state.spotify_token_expires
    ):
        return st.session_state.spotify_token

    try:
        auth_str = f"{client_id}:{client_secret}"
        auth_b64 = base64.b64encode(auth_str.encode()).decode()

        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={"Authorization": f"Basic {auth_b64}"},
            data={"grant_type": "client_credentials"},
            timeout=5,
        )

        if response.status_code == 200:
            data = response.json()
            st.session_state.spotify_token = data["access_token"]
            st.session_state.spotify_token_expires = time.time() + data["expires_in"] - 60
            return data["access_token"]
    except Exception:
        pass

    return None


_deezer_preview_cache: dict[str, str | None] = {}


def get_deezer_preview(artist: str, track: str) -> str | None:
    """Find a Deezer preview URL for a song."""
    cache_key = f"{artist}|{track}".lower()
    if cache_key in _deezer_preview_cache:
        return _deezer_preview_cache[cache_key]

    try:
        query = f"{artist} {track}"
        search_url = f"https://api.deezer.com/search?q={requests.utils.quote(query)}&limit=3"
        response = requests.get(search_url, timeout=2)  # Faster timeout

        if response.status_code == 200:
            data = response.json()
            for result in data.get("data", []):
                if result.get("preview"):
                    _deezer_preview_cache[cache_key] = result["preview"]
                    return result["preview"]
    except Exception:
        pass

    _deezer_preview_cache[cache_key] = None
    return None


_playlist_cache: dict[int, str | None] = {}
_tracks_cache: dict[int, tuple[float, list[dict]]] = {}
_image_cache: dict[str, str] = {}
CACHE_EXPIRY_SECONDS = 60  # 1 minute - short cache for more song variety

# Leaderboard storage - uses Supabase if configured, falls back to session state
MAX_LEADERBOARD_ENTRIES = 20


def get_supabase_client() -> "Client | None":
    """Get Supabase client if configured"""
    if not SUPABASE_AVAILABLE:
        return None
    try:
        url = st.secrets.get("SUPABASE_URL", "")
        key = st.secrets.get("SUPABASE_KEY", "")
        if url and key:
            return create_client(url, key)
    except Exception:
        pass
    return None


def clear_song_cache():
    """Clear all cached songs to get fresh selections"""
    global _tracks_cache, _playlist_cache
    _tracks_cache.clear()
    _playlist_cache.clear()


def load_leaderboard() -> list[dict]:
    """Load leaderboard from Supabase or session state"""
    # Try Supabase first
    client = get_supabase_client()
    if client:
        try:
            response = client.table("leaderboard").select("*").order(
                "total_score", desc=True
            ).limit(MAX_LEADERBOARD_ENTRIES).execute()
            return response.data if response.data else []
        except Exception:
            pass

    # Fall back to session state
    if "leaderboard" not in st.session_state:
        st.session_state.leaderboard = []
    return st.session_state.leaderboard


def save_leaderboard(leaderboard: list[dict]):
    """Save leaderboard to session state (Supabase saves directly in add_to_leaderboard)"""
    sorted_lb = sorted(leaderboard, key=lambda x: x["total_score"], reverse=True)
    sorted_lb = sorted_lb[:MAX_LEADERBOARD_ENTRIES]
    st.session_state.leaderboard = sorted_lb


def add_to_leaderboard(player: str, total_score: int, songs_played: int, genre: str):
    """Add a game session to the leaderboard"""
    # Use AEDT timezone (UTC+11)
    aedt = timezone(timedelta(hours=11))
    now_aedt = datetime.now(aedt)
    entry = {
        "player": player,
        "total_score": total_score,
        "songs_played": songs_played,
        "avg_score": round(total_score / songs_played) if songs_played > 0 else 0,
        "genre": genre,
        "date": now_aedt.strftime("%b %d"),
    }

    # Try to save to Supabase
    client = get_supabase_client()
    if client:
        try:
            client.table("leaderboard").insert(entry).execute()
            return  # Success - Supabase handles storage
        except Exception:
            pass  # Fall back to session state

    # Fall back to session state
    leaderboard = load_leaderboard()
    leaderboard.append(entry)
    save_leaderboard(leaderboard)


def search_top_hits_playlist(year: int, token: str) -> str | None:
    """Search for Spotify's official Top Hits playlist for a year."""
    if year in _playlist_cache:
        return _playlist_cache[year]

    headers = {"Authorization": f"Bearer {token}"}

    try:
        query = f"Top Hits {year}"
        search_url = f"https://api.spotify.com/v1/search?q={requests.utils.quote(query)}&type=playlist&limit=20"
        response = requests.get(search_url, headers=headers, timeout=5)

        if response.status_code == 200:
            data = response.json()
            playlists = data.get("playlists", {}).get("items", [])

            for playlist in playlists:
                if not playlist:
                    continue
                name = playlist.get("name", "").lower()
                owner = playlist.get("owner", {}).get("display_name", "").lower()

                if "spotify" in owner and str(year) in name:
                    _playlist_cache[year] = playlist["id"]
                    return playlist["id"]

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
    non_latin_pattern = re.compile(
        r"[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\u0400-\u04ff\u0600-\u06ff\u0e00-\u0e7f\uac00-\ud7af\u0590-\u05ff]"
    )
    if non_latin_pattern.search(text):
        return False
    accented_count = len(re.findall(r"[àáâãäåèéêëìíîïòóôõöùúûüñçøæœßðþ]", text.lower()))
    return not (len(text) > 0 and accented_count > len(text) * 0.1)


def get_songs_from_spotify(year: int, genre_query: str = "") -> list[dict]:
    """Get top chart songs from a specific year using Spotify.

    Args:
        year: The year to search for songs
        genre_query: Optional genre search terms (e.g., "rock", "pop")
    """
    cache_key = f"{year}_{genre_query}"
    if cache_key in _tracks_cache:
        cache_time, cached_tracks = _tracks_cache[cache_key]
        if time.time() - cache_time < CACHE_EXPIRY_SECONDS:
            # IMPORTANT: Shuffle on every retrieval to avoid repeating songs
            shuffled = cached_tracks.copy()
            random.shuffle(shuffled)
            return shuffled

    token = get_spotify_token()
    if not token:
        return []

    headers = {"Authorization": f"Bearer {token}"}
    tracks = []

    # Only use playlist for "All Genres" - otherwise go straight to genre search
    playlist_id = None
    if not genre_query:
        playlist_id = search_top_hits_playlist(year, token)

    if playlist_id:
        try:
            playlist_url = (
                f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=100&market=US"
            )
            response = requests.get(playlist_url, headers=headers, timeout=5)

            if response.status_code == 200:
                data = response.json()
                for item in data.get("items", []):
                    track = item.get("track")
                    if not track:
                        continue

                    album = track.get("album", {})
                    track_name = track.get("name", "")
                    album_name = album.get("name", "")

                    if is_compilation_or_remaster(album_name) or is_compilation_or_remaster(
                        track_name
                    ):
                        continue

                    artists = track.get("artists", [])
                    artist_name = artists[0]["name"] if artists else "Unknown"

                    if not is_likely_english(track_name, artist_name):
                        continue

                    popularity = track.get("popularity", 0)
                    if popularity < MIN_SPOTIFY_POPULARITY:
                        continue

                    images = album.get("images", [])
                    image_url = images[0]["url"] if images else None

                    release_date = album.get("release_date", "")
                    album_year = int(release_date[:4]) if len(release_date) >= 4 else year

                    song_key = f"{artist_name.lower()}|{track_name.lower()}"

                    tracks.append(
                        {
                            "id": track["id"],
                            "name": track_name,
                            "artist": artist_name,
                            "album": album_name,
                            "year": album_year,
                            "image_url": image_url,
                            "popularity": popularity,
                            "spotify_id": track["id"],
                            "song_key": song_key,
                        }
                    )
        except Exception:
            pass

    if not tracks:
        try:
            # Include genre in search if specified
            if genre_query:
                search_url = f"https://api.spotify.com/v1/search?q={requests.utils.quote(genre_query)}+year:{year}&type=track&limit=50&market=US"
            else:
                search_url = (
                    f"https://api.spotify.com/v1/search?q=year:{year}&type=track&limit=50&market=US"
                )
            response = requests.get(search_url, headers=headers, timeout=5)

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

                    if not is_likely_english(track_name, artist_name):
                        continue

                    images = album.get("images", [])
                    image_url = images[0]["url"] if images else None

                    song_key = f"{artist_name.lower()}|{track_name.lower()}"

                    tracks.append(
                        {
                            "id": item["id"],
                            "name": track_name,
                            "artist": artist_name,
                            "album": album_name,
                            "year": album_year,
                            "image_url": image_url,
                            "popularity": popularity,
                            "spotify_id": item["id"],
                            "song_key": song_key,
                        }
                    )
        except Exception:
            pass

    # Deduplicate
    seen_keys = set()
    unique_tracks = []
    for track in tracks:
        if track.get("song_key") not in seen_keys:
            seen_keys.add(track.get("song_key"))
            unique_tracks.append(track)
    tracks = unique_tracks

    # Shuffle before caching for better randomness
    random.shuffle(tracks)

    result = tracks[:100]
    cache_key = f"{year}_{genre_query}"
    _tracks_cache[cache_key] = (time.time(), result)
    return result


def _fetch_deezer_preview(track: dict) -> tuple[dict, str | None]:
    """Helper to fetch Deezer preview for a track"""
    preview_url = get_deezer_preview(track["artist"], track["name"])
    return (track, preview_url)


def get_random_song(
    start_year: int,
    end_year: int,
    played_ids: set | None = None,
    played_keys: set | None = None,
    genre_query: str = "",
) -> dict | None:
    """Get a random popular song from the specified year range."""
    if played_ids is None:
        played_ids = set()
    if played_keys is None:
        played_keys = set()

    years_to_try = list(range(start_year, end_year + 1))
    random.shuffle(years_to_try)

    for year in years_to_try:
        tracks = get_songs_from_spotify(year, genre_query)

        if not tracks:
            continue

        available_tracks = [
            t
            for t in tracks
            if t["id"] not in played_ids
            and t.get("song_key") not in played_keys
            and start_year <= t.get("year", year) <= end_year
        ]

        if not available_tracks:
            continue

        # Shuffle and take candidates - more for better variety
        random.shuffle(available_tracks)
        candidates = available_tracks[:20]  # Try more candidates for better variety

        with ThreadPoolExecutor(max_workers=8) as executor:  # Increased parallelism
            futures = {executor.submit(_fetch_deezer_preview, t): t for t in candidates}

            for future in as_completed(futures):
                try:
                    track, preview_url = future.result()
                    if preview_url:
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
                            "song_key": track.get(
                                "song_key", f"{track['artist'].lower()}|{track['name'].lower()}"
                            ),
                        }
                except Exception:
                    continue

    return None


def blur_image(image_url: str, blur_amount: int) -> str:
    """Download image and apply blur effect, return as base64."""
    cache_key = f"{image_url}_{blur_amount}"

    if cache_key in _image_cache:
        return _image_cache[cache_key]

    try:
        original_key = f"{image_url}_original"
        if original_key in _image_cache:
            img_data = base64.b64decode(_image_cache[original_key])
            img = Image.open(io.BytesIO(img_data))
        else:
            response = requests.get(image_url, timeout=3)
            img = Image.open(io.BytesIO(response.content))
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            _image_cache[original_key] = base64.b64encode(buffered.getvalue()).decode()

        if blur_amount > 0:
            img = img.filter(ImageFilter.GaussianBlur(radius=blur_amount))

        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        result = f"data:image/png;base64,{img_str}"

        _image_cache[cache_key] = result
        return result
    except Exception:
        return ""


def calculate_score(guess: int, actual: int, time_taken: int, hints_used: int = 0) -> int:
    """Calculate score based on accuracy and time"""
    year_diff = abs(guess - actual)

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

    time_bonus = max(0, 300 - (time_taken * 10))
    total_score = max(0, accuracy_score + time_bonus)
    return int(total_score)


def initialize_game_state():
    """Initialize session state variables"""
    defaults = {
        "game_active": False,
        "current_song": None,
        "start_time": None,
        "game_over": False,
        "player_scores": [],
        "current_player": "Player 1",
        "blur_level": 25,
        "start_year": 1995,
        "end_year": 2020,
        "selected_genre": "All Genres",
        "current_round": 0,
        "played_song_ids": set(),
        "played_song_keys": set(),
        "next_song_cache": None,
        "audio_started": False,
        "song_loaded_time": None,
        "timed_out": False,
        "status_message": "",
        "current_guess": 2000,
        "time_locked": False,
        "elapsed_playing_time": 0,
        "loading_game": False,
        "submitting_guess": False,
        "guess_timed_out": False,
        "saving_to_leaderboard": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def prefetch_next_song(start_year: int, end_year: int, genre_query: str = ""):
    """Prefetch the next song in background"""
    played_ids = st.session_state.get("played_song_ids", set())
    played_keys = st.session_state.get("played_song_keys", set())
    next_song = get_random_song(start_year, end_year, played_ids, played_keys, genre_query)
    if next_song:
        if next_song.get("image_url"):
            blur_image(next_song["image_url"], 25)
            blur_image(next_song["image_url"], 0)
        st.session_state.next_song_cache = next_song


def start_new_game(start_year: int, end_year: int, genre_query: str = ""):
    """Start a new game round"""
    song = st.session_state.get("next_song_cache")

    played_ids = st.session_state.get("played_song_ids", set())
    played_keys = st.session_state.get("played_song_keys", set())
    if song and (song["id"] in played_ids or song.get("song_key") in played_keys):
        song = None

    if song is None:
        st.session_state.status_message = "🔍 Searching for a song..."
        song = get_random_song(start_year, end_year, played_ids, played_keys, genre_query)

    st.session_state.next_song_cache = None

    if song is None:
        played_count = len(st.session_state.get("played_song_ids", set()))
        if played_count > 0:
            st.warning(f"You've played {played_count} songs! Try expanding the year range.")
        else:
            st.error("Could not find a song. Try a different range or genre!")
        st.session_state.status_message = ""
        return

    st.session_state.played_song_ids.add(song["id"])
    if song.get("song_key"):
        st.session_state.played_song_keys.add(song["song_key"])

    if song.get("image_url"):
        blur_image(song["image_url"], 25)
        blur_image(song["image_url"], 0)

    st.session_state.current_round += 1
    st.session_state.current_song = song
    st.session_state.game_active = True
    st.session_state.start_time = None
    st.session_state.game_over = False
    st.session_state.timed_out = False
    st.session_state.time_locked = False
    st.session_state.blur_level = 25
    st.session_state.audio_started = False
    st.session_state.song_loaded_time = time.time()
    st.session_state.status_message = "🎵 Press play to start!"
    st.session_state.current_guess = (start_year + end_year) // 2
    st.session_state.elapsed_playing_time = 0
    st.session_state.submitting_guess = False
    st.session_state.guess_timed_out = False

    prefetch_next_song(start_year, end_year, genre_query)


def make_guess(guess_year: int, timed_out: bool = False):
    """Process the player's guess"""
    song = st.session_state.current_song

    # Use actual playing time (excludes paused time) if available
    if st.session_state.elapsed_playing_time > 0:
        time_taken = int(st.session_state.elapsed_playing_time)
    elif st.session_state.start_time:
        time_taken = int(time.time() - st.session_state.start_time)
    else:
        time_taken = 0

    if timed_out:
        score = calculate_score(guess_year, song["year"], MAX_GUESS_TIME)
        st.session_state.timed_out = True
    else:
        score = calculate_score(guess_year, song["year"], time_taken)

    st.session_state.player_scores.append(
        {
            "player": st.session_state.current_player,
            "song": f"{song['name']} by {song['artist']}",
            "guess": guess_year,
            "actual": song["year"],
            "score": score,
            "time": time_taken,
        }
    )

    st.session_state.game_over = True
    st.session_state.blur_level = 0
    st.session_state.status_message = ""


def get_total_score() -> int:
    """Get total score for current player"""
    player = st.session_state.current_player
    return sum(s["score"] for s in st.session_state.player_scores if s["player"] == player)


def render_game_interface():
    """Render the main game interface"""
    song = st.session_state.current_song
    if not song:
        return

    # Header with game info
    total_score = get_total_score()
    current_genre = st.session_state.selected_genre
    genre_icon = GENRE_CONFIG[current_genre]["icon"]
    st.markdown(
        game_header(
            st.session_state.current_player,
            st.session_state.current_round,
            st.session_state.start_year,
            st.session_state.end_year,
            total_score,
            current_genre,
            genre_icon,
        ),
        unsafe_allow_html=True,
    )

    # Auto-refresh for game state updates (optimized frequency)
    if not st.session_state.game_over:
        st_autorefresh(interval=1000, key="game_timer")

    # Add elapsed time receiver component (hidden) - consolidated
    if st.session_state.audio_started and not st.session_state.game_over:
        components.html(elapsed_time_receiver() + get_elapsed_time_js(), height=0)

    # Calculate elapsed time
    if st.session_state.start_time is not None:
        # Use actual playing time (excludes paused time) if available
        if st.session_state.elapsed_playing_time > 0:
            elapsed_float = st.session_state.elapsed_playing_time
        else:
            elapsed_float = time.time() - st.session_state.start_time
        elapsed_seconds = int(elapsed_float)
        start_timestamp = st.session_state.start_time * 1000
    else:
        elapsed_float = 0
        elapsed_seconds = 0
        start_timestamp = 0

    # Check for timeout - lock input but don't auto-submit
    time_expired = (
        not st.session_state.game_over
        and st.session_state.audio_started
        and elapsed_seconds >= MAX_GUESS_TIME
    )
    if time_expired and not st.session_state.time_locked:
        st.session_state.time_locked = True
        st.rerun()

    # Calculate blur amount - always start fully blurred
    if not st.session_state.game_over:
        if not st.session_state.audio_started:
            # Before audio starts, keep everything fully blurred
            current_blur = 25
            hint_blur = 8
        elif st.session_state.elapsed_playing_time > 0 and elapsed_float >= 1.0:
            # Audio has been playing for at least 1 second, gradually reduce blur
            time_based_blur = max(0, 25 - (elapsed_float * 25 / HINT_REVEAL_TIME))
            current_blur = min(st.session_state.blur_level, time_based_blur)
            hint_blur = max(0, 8 - (elapsed_float * 8 / HINT_REVEAL_TIME))
        else:
            # Audio just started - keep fully blurred
            current_blur = 25
            hint_blur = 8
    else:
        current_blur = 0
        hint_blur = 0

    # === MAIN GAME LAYOUT - CENTERED ===

    # === TWO COLUMN: Album+Audio LEFT, Year Picker RIGHT ===
    if not st.session_state.game_over:
        col1, main_left, main_right, col4 = st.columns([0.1, 1.2, 0.8, 0.1])

        with main_left:
            # Album artwork (much larger - 450px)
            if song["image_url"]:
                blurred_image = blur_image(song["image_url"], int(current_blur))
                if blurred_image:
                    st.markdown(album_image(blurred_image, 450), unsafe_allow_html=True)

            # Audio visualizer bars - stop when time is up
            is_playing = st.session_state.audio_started and not st.session_state.time_locked
            st.markdown(audio_visualizer(is_playing=is_playing), unsafe_allow_html=True)

            # Audio player directly under album (wider)
            if song["preview_url"]:
                components.html(
                    audio_player(song["preview_url"], song["id"], autoplay=True), height=70
                )
                if not st.session_state.audio_started:
                    if (
                        st.session_state.song_loaded_time
                        and (time.time() - st.session_state.song_loaded_time) > 1.0
                    ):
                        st.session_state.audio_started = True
                        st.session_state.start_time = time.time()
                        st.rerun()

            # Song info card below audio
            st.markdown(
                song_info_card(song, hint_blur if st.session_state.audio_started else 8),
                unsafe_allow_html=True,
            )

        with main_right:
            start_year = st.session_state.start_year
            end_year = st.session_state.end_year
            is_locked = st.session_state.time_locked

            # Read year from query params FIRST (set by scroll wheel JS)
            year_from_url = st.query_params.get("yr")
            if year_from_url:
                try:
                    url_year = int(year_from_url)
                    if start_year <= url_year <= end_year:
                        st.session_state.current_guess = url_year
                except (ValueError, TypeError):
                    pass

            # Read elapsed time from query params (set by timer JS)
            elapsed_from_url = st.query_params.get("et")
            if elapsed_from_url:
                try:
                    st.session_state.elapsed_playing_time = float(elapsed_from_url)
                except (ValueError, TypeError):
                    pass

            # Scroll wheel year picker - include round number to force re-render with new lock state
            scroll_wheel_html = scroll_wheel_year_picker(
                st.session_state.current_guess, start_year, end_year, is_locked
            )
            # Add hidden round marker to force component refresh (content change forces re-render)
            scroll_wheel_html += f"<!-- round:{st.session_state.current_round} locked:{is_locked} -->"
            # Note: components.html doesn't support key parameter, but content changes force re-render
            components.html(scroll_wheel_html, height=220)

            # Submit button with selected year
            button_text = f"Submit {st.session_state.current_guess}"

            # Check if currently submitting to show status
            if st.session_state.get("submitting_guess", False):
                # Show submitting status with visual feedback
                st.markdown(f'''
                        <div style="
                            text-align: center;
                            padding: 1.1em 2em;
                            background: linear-gradient(135deg, #22d3ee 0%, #0ea5e9 100%);
                            border-radius: 16px;
                            box-shadow: 0 8px 24px rgba(34, 211, 238, 0.4);
                            animation: submitPulse 0.8s ease-in-out infinite;
                            border: 2px solid rgba(34, 211, 238, 0.3);
                        ">
                            <div style="font-size: 1.3em; font-weight: 700; color: white; display: flex; align-items: center; justify-content: center; gap: 0.5em;">
                                <span style="animation: spin 1s linear infinite;">⏳</span>
                                <span>Submitting {st.session_state.current_guess}...</span>
                            </div>
                        </div>
                        <style>
                            @keyframes submitPulse {{
                                0%, 100% {{ 
                                    opacity: 1;
                                    transform: scale(1);
                                }}
                                50% {{ 
                                    opacity: 0.9;
                                    transform: scale(1.02);
                                }}
                            }}
                            @keyframes spin {{
                                from {{ transform: rotate(0deg); }}
                                to {{ transform: rotate(360deg); }}
                            }}
                        </style>
                    ''', unsafe_allow_html=True)
            elif is_locked:
                # Time's up - urgent button
                button_text_urgent = f"⏰ Submit {st.session_state.current_guess}"

                if st.button(button_text_urgent, type="primary", use_container_width=True, key="submit_guess_urgent"):
                    st.session_state.submitting_guess = True
                    st.session_state.guess_timed_out = True
                    st.rerun()

                # Add moderate pulsing animation
                st.markdown(f'''
                        <style>
                            button[key="submit_guess_urgent"] {{
                                animation: urgentPulse 1s ease-in-out infinite !important;
                                background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
                                font-size: 1.35em !important;
                                font-weight: 800 !important;
                                box-shadow: 0 8px 24px rgba(239, 68, 68, 0.4) !important;
                            }}
                            @keyframes urgentPulse {{
                                0%, 100% {{
                                    transform: scale(1);
                                    box-shadow: 0 8px 24px rgba(239, 68, 68, 0.4);
                                }}
                                50% {{
                                    transform: scale(1.03);
                                    box-shadow: 0 12px 32px rgba(239, 68, 68, 0.6);
                                }}
                            }}
                        </style>
                    ''', unsafe_allow_html=True)
            else:
                # Normal button with improved styling
                if st.button(button_text, type="primary", use_container_width=True, key="submit_guess"):
                    st.session_state.submitting_guess = True
                    st.session_state.guess_timed_out = is_locked
                    st.rerun()
                
                # Enhanced button styling - happy medium between bland and flashy
                st.markdown(f'''
                        <style>
                            button[key="submit_guess"] {{
                                background: linear-gradient(135deg, #22d3ee 0%, #0ea5e9 100%) !important;
                                color: white !important;
                                font-size: 1.25em !important;
                                font-weight: 700 !important;
                                padding: 0.95em 2em !important;
                                border-radius: 16px !important;
                                border: none !important;
                                box-shadow: 
                                    0 6px 20px rgba(34, 211, 238, 0.35),
                                    0 2px 8px rgba(0, 0, 0, 0.2),
                                    inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
                                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
                                transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
                            }}
                            button[key="submit_guess"]:hover:not(:disabled) {{
                                background: linear-gradient(135deg, #06b6d4 0%, #0284c7 100%) !important;
                                box-shadow: 
                                    0 10px 28px rgba(34, 211, 238, 0.45),
                                    0 4px 12px rgba(0, 0, 0, 0.25),
                                    inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
                                transform: translateY(-2px) scale(1.02) !important;
                            }}
                            button[key="submit_guess"]:active:not(:disabled) {{
                                transform: translateY(0) scale(0.98) !important;
                                box-shadow: 
                                    0 4px 12px rgba(34, 211, 238, 0.3),
                                    0 1px 4px rgba(0, 0, 0, 0.2) !important;
                            }}
                        </style>
                    ''', unsafe_allow_html=True)

            # Timer in right column - compact
            st.markdown('<div style="margin-top: 1em;"></div>', unsafe_allow_html=True)
            if st.session_state.audio_started:
                # Only delay on the first song of the round
                delay = 2 if st.session_state.current_round == 1 else 0
                components.html(timer_html(start_timestamp, MAX_GUESS_TIME, delay_seconds=delay), height=220)
            else:
                st.markdown(static_timer(30), unsafe_allow_html=True)

    # === GAME OVER DISPLAY ===
    if st.session_state.game_over:
        last_score = st.session_state.player_scores[-1]
        guess_val = last_score["guess"]
        year_diff = abs(guess_val - last_score["actual"])

        # Result message based on accuracy
        if st.session_state.timed_out:
            emoji, message, subtitle, color = (
                "⏰",
                "TIME'S UP!",
                f"Your guess of {guess_val} was submitted.",
                "#f59e0b",
            )
        elif year_diff == 0:
            st.balloons()
            emoji, message, subtitle, color = (
                "🎉",
                "PERFECT!",
                "You got it exactly right!",
                "#00ff88",
            )
        elif year_diff <= 2:
            emoji, message, subtitle, color = (
                "🎵",
                "Excellent!",
                f"Off by only {year_diff} year{'s' if year_diff > 1 else ''}!",
                "#22d3ee",
            )
        elif year_diff <= 5:
            emoji, message, subtitle, color = (
                "🎶",
                "Good job!",
                f"Close! Off by {year_diff} years.",
                "#a78bfa",
            )
        else:
            emoji, message, subtitle, color = (
                "🎸",
                "Nice try!",
                f"Off by {year_diff} years.",
                "#8b5cf6",
            )

        st.markdown(result_display(emoji, message, subtitle, color), unsafe_allow_html=True)

        # Show revealed album and song info centered
        result_col1, result_spacer, result_col2 = st.columns([1.2, 0.1, 0.8])
        with result_col1:
            if song["image_url"]:
                blurred_image = blur_image(song["image_url"], 0)  # Fully revealed
                if blurred_image:
                    st.markdown(album_image(blurred_image, 450), unsafe_allow_html=True)

            # Audio player under album in results too
            if song["preview_url"]:
                components.html(
                    audio_player(song["preview_url"], song["id"], autoplay=False), height=70
                )

            st.markdown(song_info_card(song, 0), unsafe_allow_html=True)

        with result_col2:
            st.markdown(correct_answer_with_diff(song["year"], guess_val), unsafe_allow_html=True)
            st.markdown(score_card(last_score["score"]), unsafe_allow_html=True)

            # Listen on Deezer button
            st.markdown(spotify_button(song["deezer_url"]), unsafe_allow_html=True)

            st.write("")

            # Action buttons - horizontally aligned
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("▶️ Next Song", type="primary", use_container_width=True, key="next_song"):
                    # Reset time lock immediately before loading new song
                    st.session_state.time_locked = False
                    st.session_state.submitting_guess = False
                    st.session_state.guess_timed_out = False
                    st.session_state.loading_game = True
                    st.rerun()

            with btn_col2:
                if st.button("🏁 End Game", use_container_width=True, key="end_game"):
                    st.session_state.saving_to_leaderboard = True
                    st.rerun()


def render_leaderboard():
    """Display the persistent leaderboard (round-based)"""
    leaderboard = load_leaderboard()

    if not leaderboard:
        st.markdown(empty_leaderboard(), unsafe_allow_html=True)
        return

    st.markdown(leaderboard_header(), unsafe_allow_html=True)
    sorted_lb = sorted(leaderboard, key=lambda x: x["total_score"], reverse=True)
    for idx, entry in enumerate(sorted_lb[:10], 1):
        st.markdown(leaderboard_entry(idx, entry), unsafe_allow_html=True)


def render_song_history():
    """Display recent song history"""
    if not st.session_state.player_scores:
        return

    st.markdown('<div class="history-container">', unsafe_allow_html=True)
    st.markdown('<div class="history-header">📜 Recent Songs</div>', unsafe_allow_html=True)

    # Show last 5 songs in reverse order (most recent first)
    recent_scores = list(reversed(st.session_state.player_scores[-5:]))
    for score in recent_scores:
        history_data = {
            "song_name": score["song"].split(" by ")[0]
            if " by " in score["song"]
            else score["song"],
            "artist": score["song"].split(" by ")[1] if " by " in score["song"] else "Unknown",
            "guess": score["guess"],
            "actual": score["actual"],
            "score": score["score"],
        }
        st.markdown(song_history_item(history_data), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_settings_panel():
    """Render a compact settings panel with genre, year range, and player name"""
    st.markdown(
        '<div style="text-align: center; margin-bottom: 1em;">',
        unsafe_allow_html=True,
    )

    # Row 1: Genre and Player Name
    col_genre, col_name = st.columns([2, 1.5])

    with col_genre:
        # Genre selection with icons
        genre_options = [f"{GENRE_CONFIG[g]['icon']} {g}" for g in GENRE_LIST]
        current_idx = GENRE_LIST.index(st.session_state.selected_genre)

        selected_display = st.selectbox(
            "Genre",
            options=genre_options,
            index=current_idx,
        )

        # Extract genre name (remove icon)
        selected_genre = (
            selected_display.split(" ", 1)[1] if " " in selected_display else selected_display
        )

        # If genre changed, update year range to genre's best years
        if selected_genre != st.session_state.selected_genre:
            st.session_state.selected_genre = selected_genre
            best_years = GENRE_CONFIG[selected_genre]["best_years"]
            st.session_state.start_year = best_years[0]
            st.session_state.end_year = best_years[1]
            # Clear song cache when genre changes
            clear_song_cache()
            st.session_state.played_song_ids = set()
            st.session_state.played_song_keys = set()
            st.session_state.next_song_cache = None
            st.rerun()

    with col_name:
        player_name = st.text_input(
            "Player Name",
            value=st.session_state.current_player,
            max_chars=15,
            placeholder="Enter your name",
        )
        st.session_state.current_player = player_name

    # Row 2: Year range slider (full width)
    year_range = st.slider(
        "Year Range",
        min_value=1960,
        max_value=datetime.now().year,
        value=(st.session_state.start_year, st.session_state.end_year),
        label_visibility="collapsed",
    )
    st.session_state.start_year = year_range[0]
    st.session_state.end_year = year_range[1]

    # Show selected genre and range
    genre_icon = GENRE_CONFIG[st.session_state.selected_genre]["icon"]
    st.markdown(
        f'<div style="text-align: center; color: #22d3ee; font-size: 0.9em; margin-top: -0.5em;">'
        f"{genre_icon} {st.session_state.selected_genre} • {year_range[0]} — {year_range[1]}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)


def main():
    """Main application"""
    initialize_game_state()

    # Handle loading state - show spinner while fetching song
    if st.session_state.loading_game:
        st.markdown(main_title(), unsafe_allow_html=True)
        with st.spinner("🎵 Finding a song for you..."):
            genre_query = GENRE_CONFIG[st.session_state.selected_genre]["query"]
            start_new_game(st.session_state.start_year, st.session_state.end_year, genre_query)
            st.session_state.loading_game = False
            st.rerun()
        return

    # Handle guess submission (quick operation, no spinner needed)
    if st.session_state.submitting_guess:
        make_guess(st.session_state.current_guess, timed_out=st.session_state.guess_timed_out)
        st.session_state.submitting_guess = False
        st.rerun()

    # Handle saving to leaderboard
    if st.session_state.saving_to_leaderboard:
        st.markdown(main_title(), unsafe_allow_html=True)
        with st.spinner("💾 Saving your score to the leaderboard..."):
            total_score = get_total_score()
            songs_played = len(
                [
                    s
                    for s in st.session_state.player_scores
                    if s["player"] == st.session_state.current_player
                ]
            )
            if songs_played > 0:
                add_to_leaderboard(
                    st.session_state.current_player,
                    total_score,
                    songs_played,
                    st.session_state.selected_genre,
                )
            # Reset game state
            st.session_state.game_active = False
            st.session_state.game_over = False
            st.session_state.current_round = 0
            st.session_state.player_scores = []
            st.session_state.played_song_ids = set()
            st.session_state.played_song_keys = set()
            st.session_state.next_song_cache = None
            st.session_state.saving_to_leaderboard = False
            st.rerun()
        return

    if not st.session_state.game_active:
        # Welcome screen
        st.markdown(main_title(), unsafe_allow_html=True)

        # Settings panel
        render_settings_panel()

        # How to play
        st.markdown(how_to_play(), unsafe_allow_html=True)

        st.write("")

        # Start button - centered
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "🎵 Start New Game", type="primary", use_container_width=True, key="start_game"
            ):
                st.session_state.current_round = 0
                st.session_state.played_song_ids = set()
                st.session_state.played_song_keys = set()
                st.session_state.next_song_cache = None
                st.session_state.loading_game = True
                st.rerun()

        st.write("")
        st.write("")

        # Leaderboard
        render_leaderboard()
    else:
        # Game is active
        render_game_interface()

        # Song history at bottom
        render_song_history()


if __name__ == "__main__":
    main()
