# Copilot Instructions

This file provides guidance to GitHub Copilot when working with code in this repository.

## Project Overview

A multiplayer web game built with Streamlit where players listen to 30-second song previews and guess the release year. Features progressive album art reveal, genre selection with "golden age" presets, scroll wheel year picker, and a persistent leaderboard.

## Development Commands

```bash
# Run locally
streamlit run main.py

# Activate virtual environment (if using)
source .venv/bin/activate

# Lint (using ruff, configured in pyproject.toml)
ruff check .
ruff format .
```

## Deployment

Push to `main` branch triggers automatic deployment to Streamlit Cloud at [song-year-game.streamlit.app](https://song-year-game.streamlit.app).

## Architecture

### File Structure
- `main.py` - Core application: game logic, API integration, Streamlit UI rendering
- `ui_components.py` - CSS styles, HTML templates, and JavaScript components (timer, scroll wheel, audio player)
- `requirements.txt` / `pyproject.toml` - Python dependencies (Streamlit 1.52.2, Pillow, requests, supabase, streamlit-autorefresh)
- `packages.txt` - System dependencies for Pillow image processing
- `.python-version` - Python 3.13 (for Streamlit Cloud)

### Data Flow
1. **Song Selection**: Spotify API provides track metadata (via client credentials flow) -> Deezer API provides 30-second audio previews
2. **State Management**: All game state stored in `st.session_state` (current_song, scores, timer, etc.)
3. **UI Communication**: JavaScript components (timer, scroll wheel) sync with Streamlit via URL query params (`?yr=`, `?et=`)
4. **Persistence**: Supabase stores leaderboard data; falls back to session state if unavailable

### Key Components

**main.py:**
- `get_songs_from_spotify(year, genre_query)` - Fetches tracks from Spotify's "Top Hits" playlists or search
- `get_deezer_preview(artist, track)` - Finds audio preview URL from Deezer
- `get_random_song(start_year, end_year, ...)` - Orchestrates song selection with parallel Deezer lookups
- `blur_image(image_url, blur_amount)` - Creates blurred album art using Pillow
- `calculate_score(guess, actual, time_taken)` - Scoring algorithm (accuracy + speed bonus)
- `render_game_interface()` / `render_settings_panel()` - Main UI rendering functions

**ui_components.py:**
- `MAIN_CSS` - Global styles (dark theme, animations, responsive layout)
- `scroll_wheel_year_picker()` - JavaScript scroll wheel that syncs via `?yr=` query param
- `timer_html()` - SVG countdown timer with color transitions and pause/resume support
- `audio_player()` - HTML5 audio with visualizer sync and timer integration

## Important Patterns

### Session State Keys
```python
game_active, current_song, current_round, player_scores,
start_time, game_over, timed_out, time_locked,
elapsed_playing_time, blur_level, current_guess
```

### Genre Configuration
`GENRE_CONFIG` dict maps genre names to Spotify search queries and "golden age" year ranges (e.g., Rock: 1968-1985).

### Song Filtering
- `COMPILATION_KEYWORDS` - Excludes remasters, greatest hits, etc.
- `MIN_SPOTIFY_POPULARITY = 50` - Filters for recognizable songs
- `is_likely_english()` - Filters non-Latin character tracks

### JavaScript-Streamlit Communication
- Scroll wheel writes selected year to `?yr=` query param
- Timer writes elapsed time to `?et=` query param
- Streamlit reads these via `st.query_params.get()`

## Code Conventions

- Use `st.session_state` for all persistent data between reruns
- Strip numbers from song titles (`strip_numbers_from_title()`) to prevent year leaks
- Use `components.html()` for JavaScript components (audio, timer, scroll wheel)
- Blur starts at 25px and decreases to 0 over `HINT_REVEAL_TIME` (25 seconds)
- Timer has 30 seconds (`MAX_GUESS_TIME`); locks scroll wheel when expired

## Common Issues

- **Streamlit version**: Must use pinned version to avoid pyarrow build issues on Streamlit Cloud
- **Spotify credentials**: Requires `spotify.client_id` and `spotify.client_secret` in Streamlit secrets
- **Supabase connection**: Requires `supabase.SUPABASE_URL` and `supabase.SUPABASE_KEY` in Streamlit secrets
- **Audio autoplay**: Browsers block autoplay; users must click play manually
- **No songs found**: Expand year range or try different genre; check Spotify API rate limits

## Scoring System

| Accuracy | Points |
|----------|--------|
| Exact match | 1000 |
| Off by 1 year | 800 |
| Off by 2 years | 600 |
| Off by 3 years | 400 |
| Off by 4-5 years | 200 |

**Speed Bonus**: `max(0, 300 - (seconds * 10))` - up to 300 points for fast submissions
