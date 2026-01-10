# Claude Instructions for Song Year Guesser

## Project Overview
A **multiplayer web game** built with Streamlit where players listen to song previews and guess the release year. Features audio playback, progressive album art reveal, hints system, and competitive scoring.

## Architecture & Key Components

### Tech Stack
- **Framework**: Streamlit 1.41.1
- **Music API**: Deezer (free, no auth required)
- **Image Processing**: Pillow for album art blur effects
- **Language**: Python 3.11+
- **Deployment**: Streamlit Cloud

### File Structure
```
main.py              # Complete application (UI + game logic)
requirements.txt     # Python dependencies for Streamlit Cloud
pyproject.toml       # Project metadata and dependencies
packages.txt         # System-level apt packages
.python-version      # Python version (3.11)
```

### Key Functions in main.py
- `get_popular_songs_by_year(year)` - Fetches songs from Deezer API
- `get_random_song(start_year, end_year)` - Selects random song with verified release date
- `blur_image(image_url, blur_amount)` - Creates blurred album art
- `calculate_score(guess, actual, time, hints)` - Scoring algorithm
- `render_app()` - Main UI rendering function

## Development Workflow

### Local Development
```bash
# Activate virtual environment
source .venv/bin/activate

# Run the app
streamlit run main.py
```

### Deployment
Push to `main` branch -> Streamlit Cloud auto-deploys

## Streamlit Patterns Used

### Session State Keys
- `game_active` - Boolean for game in progress
- `current_song` - Dict with song data (name, artist, album, year, preview_url, image_url)
- `score` / `total_score` - Current and cumulative scores
- `hints_revealed` - List of revealed hint types
- `game_start_time` - Timestamp for scoring
- `leaderboard` - List of player scores
- `player_name` - Current player name

### UI Components
- `st.sidebar` - Settings and leaderboard
- `st.columns` - Layout for buttons and inputs
- `components.html` - Audio autoplay via JavaScript
- `@st.cache_data` - Not currently used (API calls need fresh data)

## API Integration

### Deezer API (No Auth Required)
- Search: `https://api.deezer.com/search?q=...`
- Album details: `https://api.deezer.com/album/{id}`
- Provides: 30-second previews, album art, release dates

### Song Filtering
- `MIN_POPULARITY_RANK = 200000` - Filter for popular songs
- `is_compilation_or_remaster()` - Excludes compilations/remasters
- Album year verification to ensure accurate release dates

## Code Conventions

### DO
- Use `st.session_state` for all persistent data
- Verify album release dates from Deezer album endpoint
- Strip numbers from song titles to prevent year leaks
- Use `components.html` for JavaScript (audio autoplay)

### DON'T
- Don't cache Deezer API calls (need variety)
- Don't show raw year numbers in song/album titles
- Don't store API tokens in code (Deezer doesn't need them)

## Common Issues

### Deployment
- Python version must be 3.11 (see `.python-version`)
- Streamlit must be pinned to 1.41.1 to avoid pyarrow build issues

### Game Logic
- Wrong years shown? Check album year verification in `get_popular_songs_by_year()`
- No songs found? Expand year range or adjust `MIN_POPULARITY_RANK`

### Audio
- Autoplay does not work in browsers - users must click play manually

## Scoring System
- **Accuracy**: Max 1000 points for exact match, decreasing for years off
- **Speed Bonus**: Max 300 points, formula: `max(0, 300 - (seconds * 10))`
- **Hint Penalty**: -100 points per hint (Album, Artist, Song Title)
