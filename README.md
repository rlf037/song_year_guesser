# 🎵 Song Year Guesser

A fun and interactive web game built with Streamlit where players guess the release year of popular songs!

## 🎮 Features

### Core Gameplay
- **Random Song Selection**: Songs are randomly selected from popular tracks within your chosen year range
- **Audio Playback**: Listen to 30-second Spotify preview clips
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

## 🚀 Setup

### Prerequisites
- Python 3.8+
- Spotify Developer Account

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd song_year_guesser
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Spotify API credentials**

   a. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

   b. Create a new app to get your Client ID and Client Secret

   c. Create a `.streamlit/secrets.toml` file in the project root:
   ```toml
   [spotify]
   client_id = "your_spotify_client_id_here"
   client_secret = "your_spotify_client_secret_here"
   ```

4. **Run the app**
   ```bash
   streamlit run main.py
   ```

## 🎯 How to Play

1. **Set Your Name**: Enter your player name in the sidebar
2. **Choose Year Range**: Select the start and end years for song selection
3. **Start Game**: Click "Start New Game" button
4. **Listen & Watch**:
   - Listen to the 30-second preview
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
- **Exact match**: 1000 points
- **Off by 1 year**: 800 points
- **Off by 2 years**: 600 points
- **Off by 3 years**: 400 points
- **Off by 4-5 years**: 200 points
- **Off by 6+ years**: Decreasing points

### Speed Bonus (max 300)
- Faster guesses earn more bonus points
- Bonus = max(0, 300 - (time_in_seconds * 10))

### Hint Penalty
- Each hint used: -100 points
- 3 hints available total

## 📊 Features Breakdown

### Progressive Reveal System
- **Initial State**: Album artwork heavily blurred (blur radius: 25)
- **Each Hint**: Blur reduces by 8 units
- **Final State**: Fully clear artwork after all hints or game end

### Song Selection Algorithm
1. Random year selected from your specified range
2. Searches Spotify for tracks from that year
3. Sorts by popularity and selects from top 20 tracks
4. Ensures you get well-known, popular songs

### Multi-User System
- Each player tracked independently
- Leaderboard shows best performances across all players
- Player stats in sidebar show personal performance
- Session persists across multiple games

## 🛠️ Technical Stack

- **Framework**: Streamlit
- **Music API**: Spotify Web API (via Spotipy)
- **Image Processing**: Pillow (PIL)
- **State Management**: Streamlit Session State

## 📝 Configuration Options

### Sidebar Settings
- **Player Name**: Custom name for the current player (max 20 chars)
- **Year Range**: Select from 1950 to current year
- **Clear Leaderboard**: Reset all scores

### Default Settings
- Start Year: 1980
- End Year: 2020
- Initial Player: "Player 1"

## 🎨 Customization

The app uses custom CSS for styling. You can modify the colors and styles in the CSS section at the top of `main.py`:

- Gradient colors: `#667eea` and `#764ba2`
- Border radius, padding, shadows, etc.

## 🐛 Troubleshooting

### No audio preview available
Some songs on Spotify don't have preview URLs. The app will show a link to listen on Spotify instead.

### Error connecting to Spotify
Verify your credentials in `.streamlit/secrets.toml` are correct.

### No tracks found for year range
Try expanding the year range or selecting a more recent time period.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 🎵 Have Fun!

Enjoy testing your music knowledge and competing with friends!
