# Song Year Guesser

A multiplayer web game where players listen to song previews and guess the release year. Built with Streamlit.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://song-year-game.streamlit.app)

## Features

### Gameplay
- **Genre Selection**: Choose from Pop, Rock, Hip-Hop, R&B, Electronic, Country, Alternative, Metal, Disco/Funk, or 80s hits
- **Golden Age Presets**: Each genre defaults to its best era (e.g., Rock: 1968-1985, Disco/Funk: 1975-1985)
- **Audio Playback**: 30-second preview clips from Spotify
- **Progressive Reveal**: Album artwork and song info gradually unblur as time passes
- **Scroll Wheel Picker**: Intuitive year selection with touch and mouse scroll support
- **30-Second Timer**: Pauses when audio is paused, with visual countdown

### Scoring
| Component | Points |
|-----------|--------|
| Exact year match | 1000 |
| Off by 1 year | 800 |
| Off by 2 years | 600 |
| Off by 3 years | 400 |
| Off by 4-5 years | 200 |
| Speed bonus | Up to 300 (faster = more) |

### Multiplayer
- Custom player names
- Persistent leaderboard tracking top scores
- Per-session score history

## Quick Start

### Play Online
**[song-year-game.streamlit.app](https://song-year-game.streamlit.app)**

### Run Locally

```bash
git clone https://github.com/rlf037/song_year_guesser.git
cd song_year_guesser
pip install -r requirements.txt
streamlit run main.py
```

## How to Play

1. **Select Genre**: Pick a music genre from the dropdown
2. **Adjust Year Range**: Optionally modify the year range slider
3. **Start Game**: Click "Start New Game"
4. **Listen**: Press play to start the song and timer
5. **Guess**: Use the scroll wheel to select a year
6. **Submit**: Click submit or wait for time to run out
7. **Continue**: Play more rounds or end the game

## Tech Stack

- **Framework**: Streamlit 1.41.1
- **Music API**: Spotify (via Deezer fallback)
- **Image Processing**: Pillow
- **Deployment**: Streamlit Cloud
- **Python**: 3.11+

## Project Structure

```
song_year_guesser/
├── main.py              # Main application
├── ui_components.py     # UI components and HTML templates
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project configuration
├── packages.txt         # System dependencies
├── .python-version      # Python version (3.11)
├── CLAUDE.md            # AI assistant instructions
└── README.md            # This file
```

## Troubleshooting

**Audio not playing**: Browsers block autoplay. Click the play button manually.

**No songs found**: Try expanding the year range or selecting a different genre.

**Timer keeps running when paused**: The visual timer pauses, but ensure you're using the latest version.

## License

Apache License 2.0

## Contributing

Issues and pull requests welcome!

---

**Test your music knowledge!**
