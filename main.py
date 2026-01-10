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
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Dark game theme - deep purple/blue */
    .stApp {
        background: linear-gradient(135deg, #0d0d1a 0%, #1a1a2e 50%, #0f0f23 100%);
    }
    
    /* Main header styling */
    .main-header {
        text-align: center;
        font-size: 3.5em;
        font-weight: 800;
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 50%, #6366f1 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s linear infinite;
        margin-bottom: 0.3em;
    }
    
    @keyframes shimmer {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    
    /* Round indicator */
    .round-badge {
        text-align: center;
        font-size: 1.2em;
        font-weight: 600;
        color: #8b5cf6;
        background: rgba(139, 92, 246, 0.15);
        padding: 0.5em 1.5em;
        border-radius: 25px;
        display: inline-block;
        margin: 0 auto 1em auto;
        border: 2px solid rgba(139, 92, 246, 0.3);
    }
    
    /* Center container */
    .center-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        width: 100%;
    }
    
    /* Score card */
    .score-card {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        padding: 1.5em 3em;
        border-radius: 20px;
        text-align: center;
        color: white;
        font-size: 1.8em;
        font-weight: 700;
        margin: 1em auto;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4);
        max-width: 400px;
    }
    
    /* Blurred hint text */
    .hint-text {
        text-align: center;
        font-size: 1.1em;
        color: #ffffff;
        padding: 0.6em 1em;
        margin: 0.3em auto;
        max-width: 450px;
        transition: filter 0.3s ease;
    }
    
    .hint-label {
        color: #8b5cf6;
        font-weight: 600;
        margin-right: 0.5em;
    }
    
    /* Timer */
    .timer {
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        color: #22d3ee;
        margin: 0.3em 0;
        text-shadow: 0 0 20px rgba(34, 211, 238, 0.5);
    }
    
    /* Leaderboard */
    .leaderboard {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 1em 1.5em;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Game over styling */
    .game-over {
        text-align: center;
        padding: 1em;
        margin: 0.5em 0;
    }
    
    /* Status line */
    .status-line {
        text-align: center;
        padding: 0.8em 1.5em;
        background: rgba(34, 211, 238, 0.1);
        border-radius: 25px;
        margin: 0.5em auto;
        font-size: 1em;
        color: #22d3ee;
        max-width: 400px;
        border: 1px solid rgba(34, 211, 238, 0.2);
    }
    
    /* Album artwork container */
    .album-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 1em auto;
    }
    
    .album-art {
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6), 0 0 60px rgba(139, 92, 246, 0.15);
        border: 2px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Audio player styling */
    .audio-container {
        margin: 1em auto;
        max-width: 380px;
        padding: 12px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* How to play box */
    .how-to-play {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2em;
        margin: 1em auto;
        max-width: 600px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #ffffff;
    }
    
    .how-to-play h3 {
        color: #8b5cf6;
        margin-bottom: 1em;
    }
    
    .how-to-play ol {
        text-align: left;
        line-height: 2;
    }
    
    /* Song details card */
    .song-details {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5em;
        margin: 1em auto;
        max-width: 500px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #ffffff;
    }
    
    /* Correct answer highlight */
    .correct-answer {
        font-size: 2em;
        font-weight: 700;
        color: #22d3ee;
        text-align: center;
        margin: 0.5em 0;
        text-shadow: 0 0 20px rgba(34, 211, 238, 0.5);
    }
    
    /* Button styling overrides */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6em 2em;
        font-weight: 600;
        font-size: 1.1em;
        transition: all 0.15s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(99, 102, 241, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
        box-shadow: 0 2px 10px rgba(99, 102, 241, 0.4);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(13, 13, 26, 0.98);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #ffffff;
    }
    
    /* Input fields */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #ffffff;
        border-radius: 8px;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #22d3ee;
    }
    
    /* Year picker - completely custom */
    .year-picker {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 1.5em;
        margin: 1em auto;
        max-width: 400px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        text-align: center;
    }
    
    .year-picker-label {
        font-size: 1em;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.8em;
    }
    
    .year-picker-display {
        font-size: 5em;
        font-weight: 800;
        color: #22d3ee;
        text-shadow: 0 0 40px rgba(34, 211, 238, 0.4);
        margin: 0.1em 0;
        font-family: 'SF Mono', 'Courier New', monospace;
        letter-spacing: -3px;
        user-select: none;
    }
    
    .year-picker-controls {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1em;
        margin-top: 1em;
    }
    
    .year-btn {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        border: 2px solid rgba(139, 92, 246, 0.5);
        background: rgba(139, 92, 246, 0.15);
        color: #8b5cf6;
        font-size: 1.5em;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.15s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .year-btn:hover {
        background: rgba(139, 92, 246, 0.3);
        border-color: #8b5cf6;
        transform: scale(1.1);
    }
    
    .year-btn:active {
        transform: scale(0.95);
    }
    
    .year-btn-big {
        width: 60px;
        height: 60px;
        font-size: 1.8em;
    }
    
    .year-range-hint {
        color: #555;
        font-size: 0.85em;
        margin-top: 1em;
    }
    
    /* Submit button special styling */
    .submit-btn-container {
        margin: 1.5em auto;
        max-width: 300px;
    }
    
    .submit-btn {
        width: 100%;
        padding: 1em 2em;
        font-size: 1.3em;
        font-weight: 700;
        color: white;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border: none;
        border-radius: 16px;
        cursor: pointer;
        transition: all 0.1s ease;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
    }
    
    .submit-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.5);
    }
    
    .submit-btn:active {
        transform: translateY(0);
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }
    
    /* Number input styling */
    .stNumberInput input {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 2px solid rgba(139, 92, 246, 0.3) !important;
        color: #22d3ee !important;
        font-size: 2em !important;
        font-weight: 700 !important;
        text-align: center !important;
        border-radius: 12px !important;
        padding: 0.5em !important;
    }
    
    .stNumberInput button {
        background: rgba(139, 92, 246, 0.2) !important;
        border: none !important;
        color: #8b5cf6 !important;
    }
    
    .stNumberInput button:hover {
        background: rgba(139, 92, 246, 0.4) !important;
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
MAX_GUESS_TIME = 30

# Time at which hints are fully revealed (seconds before end)
HINT_REVEAL_TIME = 25

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


# Cache for Deezer preview URLs to avoid repeated API calls
_deezer_preview_cache: dict[str, str | None] = {}


def get_deezer_preview(artist: str, track: str) -> str | None:
    """Find a Deezer preview URL for a song. Uses cache for performance."""
    cache_key = f"{artist}|{track}".lower()

    # Check cache first
    if cache_key in _deezer_preview_cache:
        return _deezer_preview_cache[cache_key]

    try:
        query = f"{artist} {track}"
        search_url = f"https://api.deezer.com/search?q={requests.utils.quote(query)}&limit=5"
        response = requests.get(search_url, timeout=3)  # Reduced timeout for faster response

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
        response = requests.get(search_url, headers=headers, timeout=5)

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

                    # Get release year from album - use actual album year, not playlist year
                    release_date = album.get("release_date", "")
                    album_year = int(release_date[:4]) if len(release_date) >= 4 else year

                    # Create a unique key for deduplication (artist + song name)
                    song_key = f"{artist_name.lower()}|{track_name.lower()}"

                    tracks.append(
                        {
                            "id": track["id"],
                            "name": track_name,
                            "artist": artist_name,
                            "album": album_name,
                            "year": album_year,  # Use actual album release year
                            "image_url": image_url,
                            "popularity": popularity,
                            "spotify_id": track["id"],
                            "song_key": song_key,  # For deduplication across playlists
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

                    # Skip non-English songs
                    if not is_likely_english(track_name, artist_name):
                        continue

                    images = album.get("images", [])
                    image_url = images[0]["url"] if images else None

                    # Create a unique key for deduplication (artist + song name)
                    song_key = f"{artist_name.lower()}|{track_name.lower()}"

                    tracks.append(
                        {
                            "id": item["id"],
                            "name": track_name,
                            "artist": artist_name,
                            "album": album_name,
                            "year": album_year,  # Use actual album year (already verified above)
                            "image_url": image_url,
                            "popularity": popularity,
                            "spotify_id": item["id"],
                            "song_key": song_key,  # For deduplication across playlists
                        }
                    )
        except Exception:
            pass

    # Deduplicate by song_key (same song can appear in multiple playlists)
    seen_keys = set()
    unique_tracks = []
    for track in tracks:
        if track.get("song_key") not in seen_keys:
            seen_keys.add(track.get("song_key"))
            unique_tracks.append(track)
    tracks = unique_tracks

    # Sort by popularity
    tracks.sort(key=lambda x: x.get("popularity", 0), reverse=True)

    result = tracks[:50]  # Return top 50 for variety
    _tracks_cache[year] = result
    return result


def _fetch_deezer_preview(track: dict) -> tuple[dict, str | None]:
    """Helper to fetch Deezer preview for a track (used in parallel)"""
    preview_url = get_deezer_preview(track["artist"], track["name"])
    return (track, preview_url)


def get_random_song(
    start_year: int, end_year: int, played_ids: set | None = None, played_keys: set | None = None
) -> dict | None:
    """Get a random popular song from the specified year range using Spotify + Deezer.
    Excludes songs with IDs in played_ids or keys in played_keys to prevent repeats within a session.
    """
    if played_ids is None:
        played_ids = set()
    if played_keys is None:
        played_keys = set()

    years_to_try = list(range(start_year, end_year + 1))
    random.shuffle(years_to_try)

    for year in years_to_try:  # Try all years if needed
        tracks = get_songs_from_spotify(year)

        if not tracks:
            continue

        # Filter out already played songs by ID and by artist+name key
        # Also ensure the song's actual year is within the user's selected range
        available_tracks = [
            t for t in tracks 
            if t["id"] not in played_ids 
            and t.get("song_key") not in played_keys
            and start_year <= t.get("year", year) <= end_year
        ]

        if not available_tracks:
            continue

        # Shuffle and pick candidates
        random.shuffle(available_tracks)
        candidates = available_tracks[:10]  # Check 10 tracks in parallel for better success rate

        # Fetch Deezer previews in parallel for speed
        with ThreadPoolExecutor(max_workers=6) as executor:
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
                            "song_key": track.get(
                                "song_key", f"{track['artist'].lower()}|{track['name'].lower()}"
                            ),
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
            response = requests.get(image_url, timeout=3)
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
    if "played_song_ids" not in st.session_state:
        st.session_state.played_song_ids = set()  # Track played songs to prevent repeats
    if "played_song_keys" not in st.session_state:
        st.session_state.played_song_keys = (
            set()
        )  # Track by artist+name to catch duplicates across playlists
    if "next_song_cache" not in st.session_state:
        st.session_state.next_song_cache = None  # Pre-fetched next song for instant loading
    if "audio_play_time" not in st.session_state:
        st.session_state.audio_play_time = None  # When audio actually started playing
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


def prefetch_next_song(start_year: int, end_year: int):
    """Prefetch the next song in background for instant loading"""
    played_ids = st.session_state.get("played_song_ids", set())
    played_keys = st.session_state.get("played_song_keys", set())
    next_song = get_random_song(start_year, end_year, played_ids, played_keys)
    if next_song:
        # Pre-cache images
        if next_song.get("image_url"):
            blur_image(next_song["image_url"], 25)
            blur_image(next_song["image_url"], 0)
        st.session_state.next_song_cache = next_song


def start_new_game(start_year: int, end_year: int):
    """Start a new game round"""
    # Check if we have a prefetched song ready
    song = st.session_state.get("next_song_cache")

    # Verify prefetched song hasn't been played (edge case protection)
    played_ids = st.session_state.get("played_song_ids", set())
    played_keys = st.session_state.get("played_song_keys", set())
    if song and (song["id"] in played_ids or song.get("song_key") in played_keys):
        song = None

    if song is None:
        # Show loading state only if we need to fetch
        st.session_state.status_message = "🔍 Searching for a song..."
        song = get_random_song(start_year, end_year, played_ids, played_keys)

    # Clear the prefetch cache
    st.session_state.next_song_cache = None

    if song is None:
        # Check if we've exhausted all songs
        played_count = len(st.session_state.get("played_song_ids", set()))
        if played_count > 0:
            st.warning(
                f"You've played {played_count} songs! No more unique songs available in this range. Try expanding the year range or start a new session."
            )
        else:
            st.error("Could not find a song in that year range. Try a different range!")
        st.session_state.status_message = ""
        return

    # Track this song as played (both by ID and by artist+name key)
    st.session_state.played_song_ids.add(song["id"])
    if song.get("song_key"):
        st.session_state.played_song_keys.add(song["song_key"])

    # Preload and cache the album image at max blur (if not already cached)
    if song.get("image_url"):
        st.session_state.status_message = "🎨 Loading album artwork..."
        blur_image(song["image_url"], 25)  # Pre-cache blurred version
        blur_image(song["image_url"], 0)  # Pre-cache clear version

    # Increment round counter
    st.session_state.current_round += 1

    st.session_state.current_song = song
    st.session_state.game_active = True
    st.session_state.start_time = None  # Timer will start when audio plays
    st.session_state.audio_play_time = None  # Reset audio play time
    st.session_state.hints_revealed = 0
    st.session_state.game_over = False
    st.session_state.timed_out = False
    st.session_state.blur_level = 25
    st.session_state.year_options = generate_year_options(song["year"])
    st.session_state.audio_started = False  # Will be set true when audio starts
    st.session_state.song_loaded_time = time.time()
    st.session_state.status_message = "🎵 Press play to start!"
    st.session_state.current_guess = start_year  # Reset guess to start year

    # Start prefetching the next song in background
    prefetch_next_song(start_year, end_year)


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

    # Auto-refresh for game state updates
    if not st.session_state.game_over:
        if st.session_state.audio_started:
            # Refresh every 1 second for timeout check
            st_autorefresh(interval=1000, key="game_timer")
        else:
            # Refresh more frequently to detect when audio starts
            st_autorefresh(interval=500, key="audio_start_check")

    # Display round counter with styled badge
    st.markdown(
        f'<div class="center-container"><div class="round-badge">🎮 Round {st.session_state.current_round}</div></div>',
        unsafe_allow_html=True,
    )

    # Calculate elapsed time for server-side checks
    if st.session_state.start_time is not None:
        elapsed_float = time.time() - st.session_state.start_time
        elapsed_seconds = int(elapsed_float)
        elapsed = elapsed_seconds  # For blur calculation
        start_timestamp = st.session_state.start_time * 1000  # Convert to JS timestamp (ms)
    else:
        elapsed_float = 0
        elapsed_seconds = 0
        elapsed = 0
        start_timestamp = 0

    # Check for timeout - auto-submit current guess
    if (
        not st.session_state.game_over
        and st.session_state.audio_started
        and elapsed_seconds >= MAX_GUESS_TIME
    ):
        # Submit whatever year the user has currently selected
        current_guess = st.session_state.get("current_guess", st.session_state.start_year)
        make_guess(current_guess, timed_out=True)
        st.rerun()

    # Display prominent circular countdown timer with hourglass animation
    if st.session_state.audio_started and not st.session_state.game_over:
        timer_html = f"""
        <div style="display: flex; justify-content: center; align-items: center; margin: 1em 0;">
            <div id="timer-container" style="position: relative; width: 140px; height: 140px;">
                <svg width="140" height="140" viewBox="0 0 140 140" style="transform: rotate(-90deg);">
                    <circle cx="70" cy="70" r="60" fill="none" stroke="#1e1e3f" stroke-width="12"/>
                    <circle id="timer-circle" cx="70" cy="70" r="60" fill="none" stroke="#22d3ee" stroke-width="12"
                        stroke-linecap="round" stroke-dasharray="377" stroke-dashoffset="0"
                        style="transition: stroke-dashoffset 0.1s linear, stroke 0.3s ease;"/>
                </svg>
                <div id="timer-text" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
                    text-align: center; font-family: 'SF Mono', 'Monaco', monospace;">
                    <div id="timer-seconds" style="font-size: 2.8em; font-weight: 800; color: #22d3ee; line-height: 1;">30</div>
                    <div style="font-size: 0.75em; color: #666; text-transform: uppercase; letter-spacing: 2px;">seconds</div>
                </div>
                <div id="hourglass" style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 1.5em; opacity: 0.8;">⏳</div>
            </div>
        </div>
        <script>
            (function() {{
                var startTime = {start_timestamp};
                var maxTime = {MAX_GUESS_TIME};
                var circle = document.getElementById('timer-circle');
                var secondsEl = document.getElementById('timer-seconds');
                var hourglass = document.getElementById('hourglass');
                var circumference = 2 * Math.PI * 60; // 377
                
                function updateTimer() {{
                    var now = Date.now();
                    var elapsed = (now - startTime) / 1000;
                    if (elapsed < 0) elapsed = 0;
                    if (elapsed > maxTime) elapsed = maxTime;
                    
                    var remaining = Math.ceil(maxTime - elapsed);
                    var progress = elapsed / maxTime;
                    var offset = circumference * progress;
                    
                    circle.style.strokeDashoffset = offset;
                    secondsEl.textContent = remaining;
                    
                    // Rotate hourglass
                    var rotation = (elapsed * 30) % 360;
                    hourglass.style.transform = 'translateX(-50%) rotate(' + rotation + 'deg)';
                    
                    // Color transitions based on remaining time
                    if (remaining <= 5) {{
                        circle.style.stroke = '#ef4444';
                        secondsEl.style.color = '#ef4444';
                        secondsEl.style.animation = 'pulse 0.5s infinite';
                        hourglass.textContent = '⌛';
                    }} else if (remaining <= 10) {{
                        circle.style.stroke = '#f59e0b';
                        secondsEl.style.color = '#f59e0b';
                        hourglass.textContent = '⏳';
                    }} else {{
                        circle.style.stroke = '#22d3ee';
                        secondsEl.style.color = '#22d3ee';
                        hourglass.textContent = '⏳';
                    }}
                }}
                
                updateTimer();
                setInterval(updateTimer, 100);
            }})();
        </script>
        <style>
            @keyframes pulse {{
                0%, 100% {{ transform: translate(-50%, -50%) scale(1); }}
                50% {{ transform: translate(-50%, -50%) scale(1.1); }}
            }}
            #timer-seconds {{ animation: none; }}
        </style>
        """
        components.html(timer_html, height=180)
    elif not st.session_state.game_over:
        st.markdown(
            '''<div style="display: flex; justify-content: center; align-items: center; margin: 1em 0;">
                <div style="position: relative; width: 140px; height: 140px;">
                    <svg width="140" height="140" viewBox="0 0 140 140" style="transform: rotate(-90deg);">
                        <circle cx="70" cy="70" r="60" fill="none" stroke="#1e1e3f" stroke-width="12"/>
                        <circle cx="70" cy="70" r="60" fill="none" stroke="#22d3ee" stroke-width="12" stroke-dasharray="377"/>
                    </svg>
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                        <div style="font-size: 2.8em; font-weight: 800; color: #22d3ee; line-height: 1;">30</div>
                        <div style="font-size: 0.75em; color: #666; text-transform: uppercase; letter-spacing: 2px;">seconds</div>
                    </div>
                </div>
            </div>''',
            unsafe_allow_html=True,
        )

    # Status line with styled message
    if st.session_state.status_message and not st.session_state.game_over:
        st.markdown(
            f'<div class="status-line">{st.session_state.status_message}</div>',
            unsafe_allow_html=True,
        )

    # Calculate progressive blur based on time (starts at 25, fully reveals at 25 seconds)
    if not st.session_state.game_over:
        if st.session_state.audio_started:
            # Gradually reduce blur - fully reveal by HINT_REVEAL_TIME (25 seconds)
            time_based_blur = max(0, 25 - (elapsed * 25 / HINT_REVEAL_TIME))
            current_blur = min(st.session_state.blur_level, time_based_blur)
        else:
            current_blur = st.session_state.blur_level
    else:
        current_blur = 0

    # Display album artwork with progressive reveal
    if song["image_url"]:
        blurred_image = blur_image(song["image_url"], int(current_blur))
        if blurred_image:
            st.markdown(
                f'''
                <div class="album-container">
                    <img src="{blurred_image}" width="320" class="album-art">
                </div>
                ''',
                unsafe_allow_html=True,
            )

    st.write("")

    # Audio player with autoplay and playback detection
    if song["preview_url"]:
        if not st.session_state.game_over:
            # During gameplay - autoplay with playback detection
            audio_html = f'''
            <div class="audio-container">
                <audio id="gameAudio" controls autoplay style="width: 100%; border-radius: 10px;">
                    <source src="{song["preview_url"]}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
            </div>
            <script>
                (function() {{
                    var audio = document.getElementById('gameAudio');
                    audio.volume = 1.0;
                    
                    audio.addEventListener('playing', function() {{
                        if (!localStorage.getItem('audioStarted_{song["id"]}')) {{
                            localStorage.setItem('audioStarted_{song["id"]}', Date.now().toString());
                            window.parent.postMessage({{type: 'streamlit:setComponentValue', value: Date.now()}}, '*');
                        }}
                    }});
                    
                    audio.play().catch(function(e) {{
                        console.log('Autoplay prevented:', e);
                    }});
                }})();
            </script>
            '''
            components.html(audio_html, height=80)

            # Check if we should start the timer (either already started or auto-start after brief delay)
            if not st.session_state.audio_started:
                # Auto-start timer after 1 second delay to allow audio to load
                if (
                    st.session_state.song_loaded_time
                    and (time.time() - st.session_state.song_loaded_time) > 1.0
                ):
                    st.session_state.audio_started = True
                    st.session_state.start_time = time.time()
                    st.session_state.status_message = "🎵 Listening... make your guess!"
                    st.rerun()
        else:
            # After guess - styled player without autoplay
            audio_html = f'''
            <div class="audio-container" style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);">
                <audio id="gameAudio" controls style="width: 100%; border-radius: 8px;">
                    <source src="{song["preview_url"]}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
            </div>
            '''
            components.html(audio_html, height=80)
    else:
        st.warning("No audio preview available for this song")
        st.markdown(f"[Listen on Spotify]({song['deezer_url']})")

    # Progressive blur hints - reveal by 25 seconds (no button needed)
    if st.session_state.audio_started and not st.session_state.game_over:
        # Calculate blur amount based on elapsed time (fully reveal by HINT_REVEAL_TIME)
        hint_blur = max(0, 8 - (elapsed * 8 / HINT_REVEAL_TIME))  # Starts at 8px blur, reaches 0 at 25s

        st.markdown(
            f"""
            <div style="margin: 1em auto; max-width: 450px;">
                <div class="hint-text" style="filter: blur({hint_blur:.1f}px);">
                    <span class="hint-label">💿 Album:</span> {song["album"]}
                </div>
                <div class="hint-text" style="filter: blur({hint_blur:.1f}px);">
                    <span class="hint-label">🎤 Artist:</span> {song["artist"]}
                </div>
                <div class="hint-text" style="filter: blur({hint_blur:.1f}px);">
                    <span class="hint-label">🎵 Song:</span> {song["name"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # Year guessing interface - visual scroll display with Streamlit buttons
    if not st.session_state.game_over:
        # Initialize guess_year in session state if not present
        if "current_guess" not in st.session_state:
            st.session_state.current_guess = st.session_state.start_year

        start_year = st.session_state.start_year
        end_year = st.session_state.end_year
        current_guess = st.session_state.current_guess
        
        # Calculate prev/next years for display
        prev_year = current_guess - 1 if current_guess > start_year else ""
        next_year = current_guess + 1 if current_guess < end_year else ""

        # Visual year picker display
        st.markdown(
            f"""
            <div style="display: flex; flex-direction: column; align-items: center; padding: 1em 0;">
                <div style="color: #666; text-transform: uppercase; letter-spacing: 3px; font-size: 0.75em; margin-bottom: 0.5em;">
                    📅 What year was this released?
                </div>
                
                <div style="
                    position: relative;
                    height: 160px;
                    width: 220px;
                    overflow: hidden;
                    background: linear-gradient(180deg, 
                        rgba(13,13,26,0.95) 0%, 
                        transparent 35%, 
                        transparent 65%, 
                        rgba(13,13,26,0.95) 100%);
                    border-radius: 15px;
                    border: 2px solid rgba(139, 92, 246, 0.3);
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                ">
                    <div style="font-size: 1.4em; color: #555; font-family: monospace; height: 40px; display: flex; align-items: center;">
                        {prev_year}
                    </div>
                    <div style="
                        font-size: 4em;
                        font-weight: 900;
                        font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
                        color: #22d3ee;
                        text-shadow: 0 0 40px rgba(34, 211, 238, 0.5);
                        height: 80px;
                        display: flex;
                        align-items: center;
                        border-top: 2px solid rgba(139, 92, 246, 0.4);
                        border-bottom: 2px solid rgba(139, 92, 246, 0.4);
                        padding: 0 20px;
                    ">
                        {current_guess}
                    </div>
                    <div style="font-size: 1.4em; color: #555; font-family: monospace; height: 40px; display: flex; align-items: center;">
                        {next_year}
                    </div>
                </div>
                
                <div style="color: #555; font-size: 0.8em; margin-top: 0.5em;">
                    {start_year} — {end_year}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Streamlit buttons for year control
        col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
        
        with col1:
            if st.button("−10", key="year_minus_10", use_container_width=True):
                st.session_state.current_guess = max(start_year, current_guess - 10)
                st.rerun()
        
        with col2:
            if st.button("−5", key="year_minus_5", use_container_width=True):
                st.session_state.current_guess = max(start_year, current_guess - 5)
                st.rerun()
        
        with col3:
            if st.button("−1", key="year_minus_1", use_container_width=True):
                st.session_state.current_guess = max(start_year, current_guess - 1)
                st.rerun()
        
        with col4:
            if st.button("+1", key="year_plus_1", use_container_width=True):
                st.session_state.current_guess = min(end_year, current_guess + 1)
                st.rerun()
        
        with col5:
            if st.button("+5", key="year_plus_5", use_container_width=True):
                st.session_state.current_guess = min(end_year, current_guess + 5)
                st.rerun()
        
        with col6:
            if st.button("+10", key="year_plus_10", use_container_width=True):
                st.session_state.current_guess = min(end_year, current_guess + 10)
                st.rerun()

    # Game over display
    if st.session_state.game_over:
        last_score = st.session_state.player_scores[-1]

        st.markdown('<div class="game-over">', unsafe_allow_html=True)

        # Show results - even for timeout, we now have a guess
        guess_val = last_score["guess"]
        if isinstance(guess_val, int):
            year_diff = abs(guess_val - last_score["actual"])

            if st.session_state.timed_out:
                # Time's up but we submitted their current selection
                st.markdown(
                    '<div style="text-align: center;"><span style="font-size: 4em;">⏰</span></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<div style="text-align: center; font-size: 2.5em; font-weight: 700; color: #f59e0b;">TIME\'S UP!</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div style="text-align: center; color: #a0a0a0;">Your guess of {guess_val} was submitted.</div>',
                    unsafe_allow_html=True,
                )
            elif year_diff == 0:
                st.balloons()
                st.markdown(
                    '<div style="text-align: center;"><span style="font-size: 4em;">🎉</span></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<div style="text-align: center; font-size: 2.5em; font-weight: 700; color: #00ff88;">PERFECT!</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<div style="text-align: center; color: #a0a0a0;">You got it exactly right!</div>',
                    unsafe_allow_html=True,
                )
            elif year_diff <= 2:
                st.markdown(
                    '<div style="text-align: center;"><span style="font-size: 4em;">🎵</span></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<div style="text-align: center; font-size: 2.5em; font-weight: 700; color: #22d3ee;">Excellent!</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div style="text-align: center; color: #a0a0a0;">Off by only {year_diff} year{"s" if year_diff > 1 else ""}!</div>',
                    unsafe_allow_html=True,
                )
            elif year_diff <= 5:
                st.markdown(
                    '<div style="text-align: center;"><span style="font-size: 4em;">🎶</span></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<div style="text-align: center; font-size: 2.5em; font-weight: 700; color: #a78bfa;">Good job!</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div style="text-align: center; color: #a0a0a0;">Close! Off by {year_diff} years.</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div style="text-align: center;"><span style="font-size: 4em;">🎸</span></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<div style="text-align: center; font-size: 2.5em; font-weight: 700; color: #8b5cf6;">Nice try!</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div style="text-align: center; color: #a0a0a0;">Off by {year_diff} years.</div>',
                    unsafe_allow_html=True,
                )

        st.markdown(
            f'<div class="correct-answer">The answer was {song["year"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Score display
        st.markdown(
            f'<div class="score-card">🎯 {last_score["score"]} points</div>',
            unsafe_allow_html=True,
        )

        # Reveal all info in styled card
        st.markdown(
            f'''
            <div class="song-details">
                <div style="text-align: center; margin-bottom: 1em; font-size: 1.2em; font-weight: 600; color: #8b5cf6;">Song Details</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5em;">
                    <div><strong style="color: #22d3ee;">🎵 Song:</strong> {song["name"]}</div>
                    <div><strong style="color: #22d3ee;">💿 Album:</strong> {song["album"]}</div>
                    <div><strong style="color: #22d3ee;">🎤 Artist:</strong> {song["artist"]}</div>
                    <div><strong style="color: #22d3ee;">📅 Year:</strong> {song["year"]}</div>
                </div>
                <div style="text-align: center; margin-top: 1em;">
                    <a href="{song["deezer_url"]}" target="_blank" style="color: #22d3ee;">🎧 Listen on Spotify</a>
                </div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

        st.write("")

        # Next song and end game buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            col_a, col_b = st.columns(2)
            with col_a:
                played_count = len(st.session_state.get("played_song_ids", set()))
                if st.button(
                    "▶️ Next Song",
                    type="primary",
                    use_container_width=True,
                    key="next_song",
                ):
                    start_new_game(st.session_state.start_year, st.session_state.end_year)
                    st.rerun()
            with col_b:
                if st.button("🏁 End Game", use_container_width=True, key="end_game"):
                    st.session_state.game_active = False
                    st.session_state.game_over = False
                    st.session_state.current_round = 0
                    st.session_state.played_song_ids = set()
                    st.session_state.played_song_keys = set()
                    st.session_state.next_song_cache = None
                    st.rerun()


def render_leaderboard():
    """Display the leaderboard"""
    if not st.session_state.player_scores:
        st.markdown(
            '<div style="text-align: center; color: #a0a0a0; padding: 2em;">🎮 No scores yet! Play a game to see your scores here.</div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        '<div style="text-align: center; font-size: 1.5em; font-weight: 700; color: #a78bfa; margin-bottom: 1em;">🏆 Leaderboard</div>',
        unsafe_allow_html=True,
    )

    # Sort by score
    sorted_scores = sorted(st.session_state.player_scores, key=lambda x: x["score"], reverse=True)

    for idx, score in enumerate(sorted_scores[:10], 1):
        guess_display = score["guess"] if isinstance(score["guess"], int) else "TIMEOUT"
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"#{idx}"
        st.markdown(
            f"""
            <div class="leaderboard" style="margin: 0.5em auto; max-width: 600px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 1.3em;">{medal}</span>
                        <strong style="color: #8b5cf6;">{score["player"]}</strong>
                    </div>
                    <div style="font-size: 1.2em; font-weight: 700; color: #22d3ee;">{score["score"]} pts</div>
                </div>
                <div style="font-size: 0.85em; color: #a0a0a0; margin-top: 0.3em;">
                    {score["song"]} • Guessed: {guess_display} • Actual: {score["actual"]} • {score["time"]}s
                </div>
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

        # Session stats
        played_count = len(st.session_state.get("played_song_ids", set()))
        year_range = end_year - start_year + 1
        estimated_pool = year_range * 50  # ~50 songs per year
        st.metric("Songs Played (Session)", f"{played_count} / ~{estimated_pool}")

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
        st.markdown(
            """
            <div class="how-to-play">
                <h3 style="text-align: center;">🎮 How to Play</h3>
                <ol>
                    <li><strong>🎧 Listen</strong> to a 30-second song preview</li>
                    <li><strong>🖼️ Watch</strong> the album artwork gradually reveal</li>
                    <li><strong>🤔 Guess</strong> the year the song was released</li>
                    <li><strong>🏆 Score</strong> points based on accuracy and speed!</li>
                </ol>
                <div style="text-align: center; margin-top: 1em; padding: 0.8em; background: rgba(233, 69, 96, 0.2); border-radius: 10px;">
                    💡 Use hints to reveal the album, artist, and song title (but you\'ll lose points!)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")
        st.write("")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "🎵 Start New Game", type="primary", use_container_width=True, key="start_game"
            ):
                st.session_state.current_round = 0
                st.session_state.played_song_ids = set()
                st.session_state.played_song_keys = set()
                st.session_state.next_song_cache = None
                start_new_game(start_year, end_year)
                st.rerun()

        st.write("")

        # Show leaderboard
        render_leaderboard()

    else:
        # Game is active
        render_game_interface()


if __name__ == "__main__":
    main()
