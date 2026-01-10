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
    
    /* Consistent button styling */
    .stButton > button {
        min-height: 3em;
        font-weight: 600;
    }
    
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
"""

# CSS for consistent button heights in columns
BUTTON_HEIGHT_CSS = """
<style>
div[data-testid="column"] > div > div > div > button {
    height: 3em;
}
</style>
"""


# =============================================================================
# SPOTIFY SVG ICON
# =============================================================================

SPOTIFY_SVG_ICON = """<svg width="20" height="20" viewBox="0 0 24 24" fill="white">
    <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
</svg>"""


# =============================================================================
# HTML TEMPLATES
# =============================================================================


def round_badge(round_number: int) -> str:
    """Generate round badge HTML"""
    return f'<div class="center-container"><div class="round-badge">🎮 Round {round_number}</div></div>'


def status_line(message: str) -> str:
    """Generate status line HTML"""
    return f'<div class="status-line">{message}</div>'


def album_image(image_url: str, width: int = 320) -> str:
    """Generate album artwork HTML"""
    return f'''
    <div class="album-container">
        <img src="{image_url}" width="{width}" class="album-art">
    </div>
    '''


def hints_display(album: str, artist: str, song: str, blur_amount: float) -> str:
    """Generate hints display with blur effect"""
    return f"""
    <div style="margin: 1em auto; max-width: 450px;">
        <div class="hint-text" style="filter: blur({blur_amount:.1f}px);">
            <span class="hint-label">💿 Album:</span> {album}
        </div>
        <div class="hint-text" style="filter: blur({blur_amount:.1f}px);">
            <span class="hint-label">🎤 Artist:</span> {artist}
        </div>
        <div class="hint-text" style="filter: blur({blur_amount:.1f}px);">
            <span class="hint-label">🎵 Song:</span> {song}
        </div>
    </div>
    """


def year_picker_header() -> str:
    """Generate year picker header"""
    return '<div style="text-align: center; color: #888; text-transform: uppercase; letter-spacing: 2px; font-size: 0.75em; margin-bottom: 0.5em;">📅 What year was this released?</div>'


def year_display(year: int) -> str:
    """Generate prominent year display box"""
    return f"""
    <div style="
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0.5em 0;
    ">
        <div style="
            background: linear-gradient(135deg, rgba(34, 211, 238, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
            border: 3px solid rgba(34, 211, 238, 0.6);
            border-radius: 16px;
            padding: 0.5em 2em;
            box-shadow: 0 0 30px rgba(34, 211, 238, 0.3);
        ">
            <div style="
                font-size: 4em;
                font-weight: 900;
                font-family: 'SF Mono', Monaco, Consolas, monospace;
                color: #22d3ee;
                text-shadow: 0 0 40px rgba(34, 211, 238, 0.6);
                text-align: center;
                line-height: 1.1;
            ">{year}</div>
            <div style="
                text-align: center;
                color: #666;
                font-size: 0.8em;
                text-transform: uppercase;
                letter-spacing: 2px;
            ">Your Guess</div>
        </div>
    </div>
    """


def score_card(score: int) -> str:
    """Generate score card HTML"""
    return f'<div class="score-card">🎯 {score} points</div>'


def correct_answer(year: int) -> str:
    """Generate correct answer HTML"""
    return f'<div class="correct-answer">The answer was {year}</div>'


def result_emoji(emoji: str) -> str:
    """Generate centered emoji display"""
    return f'<div style="text-align: center;"><span style="font-size: 4em;">{emoji}</span></div>'


def result_message(text: str, color: str) -> str:
    """Generate result message HTML"""
    return f'<div style="text-align: center; font-size: 2.5em; font-weight: 700; color: {color};">{text}</div>'


def result_subtitle(text: str) -> str:
    """Generate result subtitle HTML"""
    return f'<div style="text-align: center; color: #a0a0a0;">{text}</div>'


def song_details_card(song: dict) -> str:
    """Generate song details card with Spotify link"""
    return f'''
    <div class="song-details">
        <div style="text-align: center; margin-bottom: 1em; font-size: 1.2em; font-weight: 600; color: #8b5cf6;">Song Details</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5em;">
            <div><strong style="color: #22d3ee;">🎵 Song:</strong> {song["name"]}</div>
            <div><strong style="color: #22d3ee;">💿 Album:</strong> {song["album"]}</div>
            <div><strong style="color: #22d3ee;">🎤 Artist:</strong> {song["artist"]}</div>
            <div><strong style="color: #22d3ee;">📅 Year:</strong> {song["year"]}</div>
        </div>
        <div style="text-align: center; margin-top: 1.2em;">
            <a href="{song["deezer_url"]}" target="_blank" style="
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
            " onmouseover="this.style.background='#1ed760'; this.style.transform='scale(1.05)';" onmouseout="this.style.background='#1DB954'; this.style.transform='scale(1)';">
                {SPOTIFY_SVG_ICON}
                Listen on Spotify
            </a>
        </div>
    </div>
    '''


def spotify_link_button(url: str) -> str:
    """Generate standalone Spotify link button"""
    return f'''
    <div style="text-align: center;">
        <a href="{url}" target="_blank" style="
            display: inline-flex;
            align-items: center;
            gap: 0.5em;
            background: #1DB954;
            color: white;
            padding: 0.6em 1.2em;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
        ">
            {SPOTIFY_SVG_ICON}
            Listen on Spotify
        </a>
    </div>
    '''


def leaderboard_entry(idx: int, score: dict) -> str:
    """Generate a leaderboard entry HTML"""
    guess_display = score["guess"] if isinstance(score["guess"], int) else "TIMEOUT"
    medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"#{idx}"
    return f"""
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
    """


def leaderboard_header() -> str:
    """Generate leaderboard header"""
    return '<div style="text-align: center; font-size: 1.5em; font-weight: 700; color: #a78bfa; margin-bottom: 1em;">🏆 Leaderboard</div>'


def empty_leaderboard() -> str:
    """Generate empty leaderboard message"""
    return '<div style="text-align: center; color: #a0a0a0; padding: 2em;">🎮 No scores yet! Play a game to see your scores here.</div>'


def main_header() -> str:
    """Generate main game header"""
    return '<h1 class="main-header">🎵 Song Year Guesser 🎵</h1>'


def how_to_play() -> str:
    """Generate how to play box"""
    return """
    <div class="how-to-play">
        <h3 style="text-align: center;">🎮 How to Play</h3>
        <ol>
            <li><strong>🎧 Listen</strong> to a 30-second song preview</li>
            <li><strong>🖼️ Watch</strong> the album artwork gradually reveal</li>
            <li><strong>🤔 Guess</strong> the year the song was released</li>
            <li><strong>🏆 Score</strong> points based on accuracy and speed!</li>
        </ol>
        <div style="text-align: center; margin-top: 1em; padding: 0.8em; background: rgba(233, 69, 96, 0.2); border-radius: 10px;">
            💡 Use hints to reveal the album, artist, and song title (but you'll lose points!)
        </div>
    </div>
    """


# =============================================================================
# TIMER TEMPLATES
# =============================================================================


def static_timer(max_time: int = 30) -> str:
    """Generate static timer display (before game starts)"""
    return f"""<div style="display: flex; justify-content: center; align-items: center; margin: 1em 0;">
        <div style="position: relative; width: 140px; height: 140px;">
            <svg width="140" height="140" viewBox="0 0 140 140" style="transform: rotate(-90deg);">
                <circle cx="70" cy="70" r="60" fill="none" stroke="#1e1e3f" stroke-width="12"/>
                <circle cx="70" cy="70" r="60" fill="none" stroke="#22d3ee" stroke-width="12" stroke-dasharray="377"/>
            </svg>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                <div style="font-size: 2.8em; font-weight: 800; color: #22d3ee; line-height: 1;">{max_time}</div>
                <div style="font-size: 0.75em; color: #666; text-transform: uppercase; letter-spacing: 2px;">seconds</div>
            </div>
        </div>
    </div>"""


def animated_timer(start_timestamp: float, max_time: int = 30) -> str:
    """Generate animated countdown timer with hourglass"""
    return f"""
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
            var maxTime = {max_time};
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


# =============================================================================
# AUDIO PLAYER TEMPLATES
# =============================================================================


def audio_player_autoplay(preview_url: str, song_id: str) -> str:
    """Generate audio player with autoplay and playback detection"""
    return f'''
    <div class="audio-container">
        <audio id="gameAudio" controls autoplay style="width: 100%; border-radius: 10px;">
            <source src="{preview_url}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
    </div>
    <script>
        (function() {{
            var audio = document.getElementById('gameAudio');
            audio.volume = 1.0;
            
            audio.addEventListener('playing', function() {{
                if (!localStorage.getItem('audioStarted_{song_id}')) {{
                    localStorage.setItem('audioStarted_{song_id}', Date.now().toString());
                    window.parent.postMessage({{type: 'streamlit:setComponentValue', value: Date.now()}}, '*');
                }}
            }});
            
            audio.play().catch(function(e) {{
                console.log('Autoplay prevented:', e);
            }});
        }})();
    </script>
    '''


def audio_player_styled(preview_url: str) -> str:
    """Generate styled audio player without autoplay (for results screen)"""
    return f'''
    <div class="audio-container" style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);">
        <audio id="gameAudio" controls style="width: 100%; border-radius: 8px;">
            <source src="{preview_url}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
    </div>
    '''
