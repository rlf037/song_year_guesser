"""
UI Components for Song Year Guesser

This module contains all CSS styles, HTML templates, and JavaScript code
used in the Streamlit application. Separating these from main.py keeps
the business logic clean and makes styling easier to maintain.
"""

# =============================================================================
# GLOBAL CSS STYLES
# =============================================================================

MAIN_CSS = """
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Dark game theme - deep purple/blue */
    .stApp {
        background: linear-gradient(135deg, #0d0d1a 0%, #1a1a2e 50%, #0f0f23 100%);
    }
    
    /* ===== HEADER SECTION ===== */
    .game-header {
        background: rgba(13, 13, 26, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(139, 92, 246, 0.3);
        padding: 0.8em 1.5em;
        margin: -1em -1em 1.5em -1em;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1em;
    }
    
    .header-title {
        font-size: 1.8em;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(139, 92, 246, 0.5);
        display: flex;
        align-items: center;
        gap: 0.3em;
    }
    
    .header-controls {
        display: flex;
        align-items: center;
        gap: 1.5em;
        flex-wrap: wrap;
    }
    
    .header-item {
        display: flex;
        align-items: center;
        gap: 0.5em;
        color: #a0a0a0;
        font-size: 0.9em;
    }
    
    .header-item-label {
        color: #666;
        font-size: 0.75em;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .header-item-value {
        color: #22d3ee;
        font-weight: 600;
    }
    
    .round-indicator {
        background: rgba(139, 92, 246, 0.2);
        border: 1px solid rgba(139, 92, 246, 0.4);
        padding: 0.3em 0.8em;
        border-radius: 15px;
        color: #a78bfa;
        font-weight: 600;
        font-size: 0.85em;
    }
    
    /* ===== MAIN TITLE (Welcome Screen) ===== */
    .main-title {
        text-align: center;
        margin: 2em 0 1em 0;
    }
    
    .main-title h1 {
        font-size: 4em;
        font-weight: 900;
        margin: 0;
        padding: 0;
        line-height: 1.1;
    }
    
    .main-title .gradient-text {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 30%, #ec4899 60%, #f43f5e 100%);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-shift 8s ease infinite;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-title .subtitle {
        font-size: 1.2em;
        color: #666;
        margin-top: 0.5em;
        font-weight: 400;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    .main-title .music-icons {
        font-size: 0.6em;
        margin: 0 0.2em;
        opacity: 0.8;
    }
    
    /* ===== GAME LAYOUT - SIDE BY SIDE ===== */
    .game-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2em;
        max-width: 1000px;
        margin: 0 auto;
        padding: 1em;
    }
    
    @media (max-width: 768px) {
        .game-container {
            grid-template-columns: 1fr;
        }
    }
    
    .game-left {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .game-right {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    /* ===== SONG INFO CARD (Above Album Art) ===== */
    .song-info-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.2em;
        margin-bottom: 1em;
        width: 100%;
        max-width: 350px;
    }
    
    .song-info-item {
        display: flex;
        align-items: center;
        padding: 0.5em 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        transition: filter 0.3s ease;
    }
    
    .song-info-item:last-child {
        border-bottom: none;
    }
    
    .song-info-icon {
        font-size: 1.2em;
        margin-right: 0.8em;
        width: 1.5em;
        text-align: center;
    }
    
    .song-info-label {
        color: #666;
        font-size: 0.8em;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 50px;
    }
    
    .song-info-value {
        color: #fff;
        font-weight: 500;
        flex: 1;
        text-align: right;
    }
    
    /* ===== ALBUM ART ===== */
    .album-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0.5em 0;
    }
    
    .album-art {
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6), 0 0 60px rgba(139, 92, 246, 0.15);
        border: 2px solid rgba(255, 255, 255, 0.08);
        transition: filter 0.3s ease;
    }
    
    /* ===== YEAR PICKER ===== */
    .year-picker-container {
        background: rgba(255, 255, 255, 0.02);
        border: 2px solid rgba(139, 92, 246, 0.3);
        border-radius: 24px;
        padding: 2em;
        text-align: center;
        width: 100%;
        max-width: 320px;
    }
    
    .year-picker-container.locked {
        border-color: rgba(239, 68, 68, 0.5);
        background: rgba(239, 68, 68, 0.05);
    }
    
    .year-picker-label {
        font-size: 0.85em;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.5em;
    }
    
    .year-display {
        font-size: 5em;
        font-weight: 900;
        font-family: 'SF Mono', Monaco, Consolas, monospace;
        color: #22d3ee;
        text-shadow: 0 0 40px rgba(34, 211, 238, 0.4);
        line-height: 1;
        margin: 0.1em 0;
        user-select: none;
    }
    
    .year-display.locked {
        color: #f59e0b;
        text-shadow: 0 0 40px rgba(245, 158, 11, 0.4);
    }
    
    .year-range-label {
        font-size: 0.8em;
        color: #555;
        margin-top: 0.5em;
    }
    
    /* ===== TIMER ===== */
    .timer-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 1em 0;
    }
    
    .timer-ring {
        position: relative;
        width: 100px;
        height: 100px;
    }
    
    .timer-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
    }
    
    .timer-seconds {
        font-size: 2em;
        font-weight: 800;
        color: #22d3ee;
        line-height: 1;
    }
    
    .timer-label {
        font-size: 0.6em;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        min-height: 3em;
        font-weight: 600;
        border-radius: 12px;
        transition: all 0.15s ease;
    }
    
    .stButton > button:disabled {
        opacity: 0.4;
        cursor: not-allowed;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button[kind="primary"]:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(99, 102, 241, 0.5);
    }
    
    .submit-btn {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        font-size: 1.2em !important;
        padding: 0.8em 2em !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4) !important;
    }
    
    .submit-btn:hover:not(:disabled) {
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.5) !important;
    }
    
    /* ===== SCORE CARD ===== */
    .score-card {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        padding: 1.2em 2.5em;
        border-radius: 16px;
        text-align: center;
        color: white;
        font-size: 1.5em;
        font-weight: 700;
        margin: 1em auto;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4);
        max-width: 350px;
    }
    
    /* ===== CORRECT ANSWER ===== */
    .correct-answer {
        font-size: 1.8em;
        font-weight: 700;
        color: #22d3ee;
        text-align: center;
        margin: 0.5em 0;
        text-shadow: 0 0 20px rgba(34, 211, 238, 0.5);
    }
    
    /* ===== RESULT MESSAGE ===== */
    .result-container {
        text-align: center;
        padding: 1em;
        margin: 1em 0;
    }
    
    .result-emoji {
        font-size: 3.5em;
        margin-bottom: 0.2em;
    }
    
    .result-message {
        font-size: 2em;
        font-weight: 700;
    }
    
    .result-subtitle {
        color: #a0a0a0;
        margin-top: 0.3em;
    }
    
    /* ===== AUDIO PLAYER ===== */
    .audio-container {
        margin: 1em auto;
        max-width: 350px;
        padding: 12px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* ===== LEADERBOARD ===== */
    .leaderboard {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 1em 1.5em;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin: 0.5em auto;
        max-width: 600px;
    }
    
    .leaderboard-header {
        text-align: center;
        font-size: 1.3em;
        font-weight: 700;
        color: #a78bfa;
        margin-bottom: 1em;
    }
    
    /* ===== HOW TO PLAY ===== */
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
        text-align: center;
    }
    
    .how-to-play ol {
        text-align: left;
        line-height: 2;
    }
    
    /* ===== SETTINGS PANEL ===== */
    .settings-panel {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1em;
        margin: 1em 0;
    }
    
    .settings-row {
        display: flex;
        align-items: center;
        gap: 1em;
        flex-wrap: wrap;
    }
    
    .settings-item {
        display: flex;
        align-items: center;
        gap: 0.5em;
    }
    
    /* ===== STATUS LINE ===== */
    .status-line {
        text-align: center;
        padding: 0.6em 1.2em;
        background: rgba(34, 211, 238, 0.1);
        border-radius: 20px;
        margin: 0.5em auto;
        font-size: 0.95em;
        color: #22d3ee;
        max-width: 350px;
        border: 1px solid rgba(34, 211, 238, 0.2);
    }
    
    /* ===== SPOTIFY BUTTON ===== */
    .spotify-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5em;
        background: #1DB954;
        color: white;
        padding: 0.6em 1.2em;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.95em;
        transition: all 0.2s ease;
    }
    
    .spotify-btn:hover {
        background: #1ed760;
        transform: scale(1.05);
    }
    
    /* ===== LOCKED STATE INDICATOR ===== */
    .locked-indicator {
        background: rgba(245, 158, 11, 0.2);
        border: 1px solid rgba(245, 158, 11, 0.4);
        color: #f59e0b;
        padding: 0.4em 1em;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        text-align: center;
        margin: 0.5em 0;
    }
    
    /* ===== SCROLLBAR STYLING ===== */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(139, 92, 246, 0.3);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(139, 92, 246, 0.5);
    }
    
    /* ===== SLIDER STYLING ===== */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    }
    
    .stSlider [data-baseweb="slider"] {
        margin-top: 0.5em;
    }
    
    /* ===== NUMBER INPUT (scroll wheel) ===== */
    .stNumberInput input {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 2px solid rgba(139, 92, 246, 0.3) !important;
        color: #22d3ee !important;
        font-size: 3em !important;
        font-weight: 700 !important;
        text-align: center !important;
        border-radius: 12px !important;
        padding: 0.3em !important;
        height: auto !important;
    }
    
    .stNumberInput input:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.3) !important;
    }
    
    .stNumberInput button {
        display: none !important;
    }
    
    .stNumberInput input:disabled {
        color: #f59e0b !important;
        border-color: rgba(245, 158, 11, 0.5) !important;
        background: rgba(245, 158, 11, 0.1) !important;
    }
    
    /* Hide +/- buttons on number input */
    .stNumberInput [data-baseweb="input"] button {
        display: none !important;
    }
</style>
"""

# =============================================================================
# HTML TEMPLATE FUNCTIONS
# =============================================================================

def game_header(player_name: str, round_num: int, start_year: int, end_year: int, total_score: int = 0) -> str:
    """Generate the game header with controls"""
    return f"""
    <div class="game-header">
        <div class="header-title">
            🎵 Song Year Guesser
        </div>
        <div class="header-controls">
            <div class="header-item">
                <span class="header-item-label">Player</span>
                <span class="header-item-value">{player_name}</span>
            </div>
            <div class="header-item">
                <span class="header-item-label">Years</span>
                <span class="header-item-value">{start_year} - {end_year}</span>
            </div>
            <div class="header-item">
                <span class="header-item-label">Score</span>
                <span class="header-item-value">{total_score}</span>
            </div>
            <div class="round-indicator">Round {round_num}</div>
        </div>
    </div>
    """


def main_title() -> str:
    """Generate the main title for the welcome screen"""
    return """
    <div class="main-title">
        <h1>
            <span class="music-icons">🎵</span>
            <span class="gradient-text">Song Year Guesser</span>
            <span class="music-icons">🎵</span>
        </h1>
        <div class="subtitle">Test your music knowledge</div>
    </div>
    """


def song_info_card(song: dict, blur_amount: float) -> str:
    """Generate the song info card with blur effect"""
    blur_css = f"filter: blur({blur_amount:.1f}px);"
    return f"""
    <div class="song-info-card">
        <div class="song-info-item" style="{blur_css}">
            <span class="song-info-icon">🎵</span>
            <span class="song-info-label">Song</span>
            <span class="song-info-value">{song["name"]}</span>
        </div>
        <div class="song-info-item" style="{blur_css}">
            <span class="song-info-icon">🎤</span>
            <span class="song-info-label">Artist</span>
            <span class="song-info-value">{song["artist"]}</span>
        </div>
        <div class="song-info-item" style="{blur_css}">
            <span class="song-info-icon">💿</span>
            <span class="song-info-label">Album</span>
            <span class="song-info-value">{song["album"]}</span>
        </div>
    </div>
    """


def album_image(image_url: str, width: int = 280) -> str:
    """Generate album image HTML"""
    return f"""
    <div class="album-container">
        <img src="{image_url}" width="{width}" class="album-art">
    </div>
    """


def year_picker_display(year: int, start_year: int, end_year: int, locked: bool = False) -> str:
    """Generate the year display (not the input, just the visual)"""
    locked_class = "locked" if locked else ""
    locked_indicator = '<div class="locked-indicator">🔒 TIME\'S UP - Submit your guess!</div>' if locked else ''
    return f"""
    <div class="year-picker-container {locked_class}">
        <div class="year-picker-label">What year was this released?</div>
        <div class="year-display {locked_class}">{year}</div>
        <div class="year-range-label">{start_year} - {end_year}</div>
        {locked_indicator}
    </div>
    """


def timer_html(start_timestamp: float, max_time: int) -> str:
    """Generate the countdown timer with animation"""
    return f"""
    <div class="timer-container">
        <div class="timer-ring">
            <svg width="100" height="100" viewBox="0 0 100 100" style="transform: rotate(-90deg);">
                <circle cx="50" cy="50" r="42" fill="none" stroke="#1e1e3f" stroke-width="8"/>
                <circle id="timer-circle" cx="50" cy="50" r="42" fill="none" stroke="#22d3ee" stroke-width="8"
                    stroke-linecap="round" stroke-dasharray="264" stroke-dashoffset="0"
                    style="transition: stroke-dashoffset 0.1s linear, stroke 0.3s ease;"/>
            </svg>
            <div class="timer-text">
                <div id="timer-seconds" class="timer-seconds">30</div>
                <div class="timer-label">sec</div>
            </div>
        </div>
    </div>
    <script>
        (function() {{
            var startTime = {start_timestamp};
            var maxTime = {max_time};
            var circle = document.getElementById('timer-circle');
            var secondsEl = document.getElementById('timer-seconds');
            var circumference = 2 * Math.PI * 42;
            
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
                
                if (remaining <= 5) {{
                    circle.style.stroke = '#ef4444';
                    secondsEl.style.color = '#ef4444';
                }} else if (remaining <= 10) {{
                    circle.style.stroke = '#f59e0b';
                    secondsEl.style.color = '#f59e0b';
                }} else {{
                    circle.style.stroke = '#22d3ee';
                    secondsEl.style.color = '#22d3ee';
                }}
            }}
            
            updateTimer();
            setInterval(updateTimer, 100);
        }})();
    </script>
    """


def static_timer(seconds: int = 30) -> str:
    """Generate a static timer display"""
    return f"""
    <div class="timer-container">
        <div class="timer-ring">
            <svg width="100" height="100" viewBox="0 0 100 100" style="transform: rotate(-90deg);">
                <circle cx="50" cy="50" r="42" fill="none" stroke="#1e1e3f" stroke-width="8"/>
                <circle cx="50" cy="50" r="42" fill="none" stroke="#22d3ee" stroke-width="8" stroke-dasharray="264"/>
            </svg>
            <div class="timer-text">
                <div class="timer-seconds">{seconds}</div>
                <div class="timer-label">sec</div>
            </div>
        </div>
    </div>
    """


def result_display(emoji: str, message: str, subtitle: str, color: str) -> str:
    """Generate the result message display"""
    return f"""
    <div class="result-container">
        <div class="result-emoji">{emoji}</div>
        <div class="result-message" style="color: {color};">{message}</div>
        <div class="result-subtitle">{subtitle}</div>
    </div>
    """


def correct_answer(year: int) -> str:
    """Generate the correct answer display"""
    return f'<div class="correct-answer">The answer was {year}</div>'


def score_card(score: int) -> str:
    """Generate the score card display"""
    return f'<div class="score-card">🎯 {score} points</div>'


def status_line(message: str) -> str:
    """Generate a status message line"""
    return f'<div class="status-line">{message}</div>'


def spotify_button(url: str) -> str:
    """Generate a Spotify listen button"""
    return f"""
    <div style="text-align: center; margin-top: 1em;">
        <a href="{url}" target="_blank" class="spotify-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
            </svg>
            Listen on Spotify
        </a>
    </div>
    """


def how_to_play() -> str:
    """Generate the how to play section"""
    return """
    <div class="how-to-play">
        <h3>🎮 How to Play</h3>
        <ol>
            <li><strong>🎧 Listen</strong> to a 30-second song preview</li>
            <li><strong>🖼️ Watch</strong> the album artwork and song info gradually reveal</li>
            <li><strong>🎯 Scroll</strong> to select your guess for the release year</li>
            <li><strong>⏱️ Submit</strong> before time runs out for bonus points!</li>
        </ol>
        <div style="text-align: center; margin-top: 1em; padding: 0.8em; background: rgba(139, 92, 246, 0.2); border-radius: 10px;">
            💡 The faster and more accurate you are, the more points you score!
        </div>
    </div>
    """


def leaderboard_entry(idx: int, score: dict) -> str:
    """Generate a single leaderboard entry"""
    guess_display = score["guess"] if isinstance(score["guess"], int) else "TIMEOUT"
    medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"#{idx}"
    return f"""
    <div class="leaderboard">
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
    """


def audio_player(preview_url: str, song_id: str, autoplay: bool = True) -> str:
    """Generate an audio player"""
    autoplay_attr = "autoplay" if autoplay else ""
    script = ""
    if autoplay:
        script = f"""
        <script>
            (function() {{
                var audio = document.getElementById('gameAudio');
                audio.volume = 1.0;
                audio.play().catch(function(e) {{
                    console.log('Autoplay prevented:', e);
                }});
            }})();
        </script>
        """
    return f"""
    <div class="audio-container">
        <audio id="gameAudio" controls {autoplay_attr} style="width: 100%; border-radius: 10px;">
            <source src="{preview_url}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
    </div>
    {script}
    """
