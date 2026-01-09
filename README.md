# 🎵 Song Year Guesser

A fun and interactive web game built with Streamlit where players guess the release year of popular songs!

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://songyearguesser.streamlit.app)

## 🎮 Features

### Core Gameplay
- **Random Song Selection**: Songs randomly selected from popular tracks within your chosen year range
- **Audio Playback**: Listen to 30-second preview clips with autoplay
- **Progressive Artwork Reveal**: Album artwork starts blurred and gradually becomes clearer
- **Multiple Choice & Custom Input**: Choose from 4 suggested years or enter your own guess
- **Countdown Timer**: Track how long it takes you to make your guess

### Game Mechanics
- **Progressive Hints System**: Reveal album, artist, and song title (costs points!)
- **Smart Scoring**: Points based on:
  - Accuracy (max 1000 points for exact match)
  - Speed (bonus points for quick guesses)
  - Hints used (penalty for each hint revealed)

### Multiplayer Features
- **Multi-Player Support**: Multiple players can compete with custom names
- **Leaderboard**: Track top 10 scores across all players
- **Player Stats**: View games played, total score, and average score per player

### UI/UX
- **Clean, Modern Design**: Beautiful gradient UI with smooth animations
- **Responsive Layout**: Centered layout optimized for all screen sizes
- **Visual Feedback**: Balloons for perfect guesses, styled score cards
- **Sidebar Settings**: Easy configuration for year range and player name

## 🚀 Quick Start

### Play Online
Visit the deployed app: **[songyearguesser.streamlit.app](https://songyearguesser.streamlit.app)**

### Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/rlf037/song_year_guesser.git
   cd song_year_guesser
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run main.py
   ```

No API keys required! The app uses the free Deezer API for song data.

## 🎯 How to Play

1. **Set Your Name**: Enter your player name in the sidebar
2. **Choose Year Range**: Select the start and end years for song selection
3. **Start Game**: Click "Start New Game" button
4. **Listen & Watch**:
   - Audio automatically plays when the song loads
   - Watch the album artwork gradually reveal
   - Timer starts counting!
5. **Get Hints** (optional): Reveal album, artist, or song title (costs 100 points each)
6. **Make Your Guess**:
   - Click one of the 4 multiple choice years, OR
   - Enter a specific year and click "Submit Guess"
7. **See Results**: View your score and how close you were!
8. **Play Again**: Start a new round or check the leaderboard

## 🏆 Scoring System

### Accuracy Points (max 1000)
| Accuracy | Points |
|----------|--------|
| Exact match | 1000 |
| Off by 1 year | 800 |
| Off by 2 years | 600 |
| Off by 3 years | 400 |
| Off by 4-5 years | 200 |
| Off by 6+ years | Decreasing |

### Speed Bonus (max 300)
- Faster guesses earn more bonus points
- Formula: `max(0, 300 - (seconds × 10))`

### Hint Penalty
- Each hint used: **-100 points**
- 3 hints available: Album, Artist, Song Title

## 🛠️ Technical Stack

| Component | Technology |
|-----------|------------|
| Framework | Streamlit 1.41.1 |
| Music API | Deezer (free, no auth required) |
| Image Processing | Pillow (PIL) |
| State Management | Streamlit Session State |
| Deployment | Streamlit Cloud |

## 📁 Project Structure

```
song_year_guesser/
├── main.py              # Main application code
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project configuration
├── packages.txt         # System dependencies for Streamlit Cloud
├── .python-version      # Python version for deployment
├── .streamlit/          # Streamlit configuration (local)
│   └── secrets.toml     # Local secrets (gitignored)
├── LICENSE              # Apache 2.0 License
└── README.md            # This file
```

## 🔧 Configuration

### Environment
- **Python Version**: 3.11+ (specified in `.python-version`)
- **Dependencies**: See `requirements.txt`

### Customization
The app uses custom CSS for styling. Modify the colors in `main.py`:
- Primary gradient: `#667eea` → `#764ba2`
- Adjust blur levels, timing, and other UI elements

## 🐛 Troubleshooting

### No audio playing
- Some browsers block autoplay - click the play button manually
- Ensure your volume is turned up

### No songs found for year range
- Try expanding the year range
- Some years have more songs available than others

### Deployment issues
- Ensure `.python-version` is set to `3.11`
- Check that all dependencies are in `requirements.txt`

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests with improvements
- Share the game with friends!

## 🙏 Acknowledgments

- **Deezer API** for providing free access to song previews and metadata
- **Streamlit** for the amazing web framework
- All the music lovers who play and enjoy the game!

---

**🎵 Have fun testing your music knowledge!**
