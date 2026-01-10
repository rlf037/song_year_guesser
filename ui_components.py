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
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        gap: 2em;
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
    
    /* ===== GAME LAYOUT - CENTERED STACK ===== */
    .game-main {
        display: flex;
        flex-direction: column;
        align-items: center;
        max-width: 500px;
        margin: 0 auto;
        padding: 0 1em;
    }
    
    .game-row {
        display: flex;
        justify-content: center;
        align-items: flex-start;
        gap: 2em;
        width: 100%;
        margin: 1em 0;
    }
    
    @media (max-width: 600px) {
        .game-row {
            flex-direction: column;
            align-items: center;
        }
    }
    
    /* ===== SONG INFO CARD ===== */
    .song-info-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 0.8em 1em;
        max-width: 450px;
        width: 100%;
        margin-top: 0.5em;
        box-sizing: border-box;
    }
    
    .song-info-item {
        display: flex;
        align-items: center;
        padding: 0.4em 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .song-info-item:last-child {
        border-bottom: none;
    }
    
    .song-info-icon {
        font-size: 1em;
        margin-right: 0.6em;
        width: 1.2em;
        text-align: center;
    }
    
    .song-info-label {
        color: #888;
        font-size: 0.75em;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 50px;
    }
    
    .song-info-value {
        color: #fff;
        font-weight: 500;
        font-size: 0.9em;
        flex: 1;
        text-align: right;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        transition: filter 0.3s ease;
    }
    
    /* ===== ALBUM ART ===== */
    .album-container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .album-art {
        border-radius: 16px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.6), 0 0 60px rgba(139, 92, 246, 0.2);
        border: 3px solid rgba(255, 255, 255, 0.1);
        transition: filter 0.3s ease;
        display: block;
        max-width: 100%;
        height: auto;
    }
    
    /* ===== AUDIO VISUALIZER ===== */
    .audio-viz-container {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        gap: 4px;
        height: 40px;
        margin: 1em 0 0.5em 0;
        max-width: 450px;
        width: 100%;
    }
    
    .audio-viz-bar {
        width: 6px;
        background: linear-gradient(to top, #6366f1, #22d3ee);
        border-radius: 3px;
        animation: audioViz 0.5s ease-in-out infinite alternate;
    }
    
    .audio-viz-bar:nth-child(1) { animation-delay: 0s; height: 12px; }
    .audio-viz-bar:nth-child(2) { animation-delay: 0.1s; height: 20px; }
    .audio-viz-bar:nth-child(3) { animation-delay: 0.15s; height: 14px; }
    .audio-viz-bar:nth-child(4) { animation-delay: 0.2s; height: 28px; }
    .audio-viz-bar:nth-child(5) { animation-delay: 0.05s; height: 16px; }
    .audio-viz-bar:nth-child(6) { animation-delay: 0.25s; height: 24px; }
    .audio-viz-bar:nth-child(7) { animation-delay: 0.1s; height: 12px; }
    .audio-viz-bar:nth-child(8) { animation-delay: 0.3s; height: 30px; }
    .audio-viz-bar:nth-child(9) { animation-delay: 0.15s; height: 18px; }
    .audio-viz-bar:nth-child(10) { animation-delay: 0.2s; height: 14px; }
    .audio-viz-bar:nth-child(11) { animation-delay: 0.25s; height: 22px; }
    .audio-viz-bar:nth-child(12) { animation-delay: 0.05s; height: 16px; }
    .audio-viz-bar:nth-child(13) { animation-delay: 0.3s; height: 26px; }
    .audio-viz-bar:nth-child(14) { animation-delay: 0.1s; height: 12px; }
    .audio-viz-bar:nth-child(15) { animation-delay: 0.2s; height: 18px; }
    .audio-viz-bar:nth-child(16) { animation-delay: 0.15s; height: 24px; }
    .audio-viz-bar:nth-child(17) { animation-delay: 0.25s; height: 14px; }
    .audio-viz-bar:nth-child(18) { animation-delay: 0.1s; height: 20px; }
    .audio-viz-bar:nth-child(19) { animation-delay: 0.2s; height: 16px; }
    .audio-viz-bar:nth-child(20) { animation-delay: 0.05s; height: 22px; }
    
    @keyframes audioViz {
        0% { transform: scaleY(0.3); opacity: 0.5; }
        100% { transform: scaleY(1); opacity: 1; }
    }
    
    .audio-viz-static .audio-viz-bar {
        animation: none;
        opacity: 0.3;
        transform: scaleY(0.3);
    }
    
    /* ===== YEAR PICKER ===== */
    .year-picker-label {
        font-size: 0.9em;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-align: center;
        margin-bottom: 0.5em;
    }
    
    .year-display {
        font-size: 4em;
        font-weight: 800;
        color: #22d3ee;
        text-align: center;
        text-shadow: 0 0 30px rgba(34, 211, 238, 0.5);
        font-family: 'SF Mono', Monaco, Consolas, monospace;
        margin: 0.2em 0 0.5em 0;
    }
    
    .year-display.locked {
        color: #f59e0b;
        text-shadow: 0 0 30px rgba(245, 158, 11, 0.5);
    }
    
    /* ===== YEAR WHEEL (legacy) ===== */
    .year-wheel-container {
        background: rgba(255, 255, 255, 0.02);
        border: 2px solid rgba(139, 92, 246, 0.3);
        border-radius: 20px;
        padding: 1em 1.5em;
        text-align: center;
        width: 100%;
        max-width: 260px;
        margin: 0 auto;
    }
    
    .year-wheel-container.locked {
        border-color: rgba(239, 68, 68, 0.5);
        background: rgba(239, 68, 68, 0.05);
    }
    
    .year-wheel-label {
        font-size: 0.75em;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.8em;
    }
    
    .year-wheel {
        height: 150px;
        overflow: hidden;
        position: relative;
        cursor: ns-resize;
        -webkit-user-select: none;
        user-select: none;
    }
    
    .year-wheel-inner {
        display: flex;
        flex-direction: column;
        align-items: center;
        transition: transform 0.1s ease-out;
    }
    
    .year-wheel-item {
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'SF Mono', Monaco, Consolas, monospace;
        font-weight: 700;
        transition: all 0.15s ease;
        width: 100%;
    }
    
    .year-wheel-item.adjacent {
        font-size: 1.2em;
        color: #444;
        opacity: 0.4;
    }
    
    .year-wheel-item.selected {
        font-size: 2.8em;
        color: #22d3ee;
        text-shadow: 0 0 30px rgba(34, 211, 238, 0.5);
    }
    
    .year-wheel-item.selected.locked {
        color: #f59e0b;
        text-shadow: 0 0 30px rgba(245, 158, 11, 0.5);
    }
    
    .year-range-label {
        font-size: 0.75em;
        color: #555;
        margin-top: 0.8em;
    }
    
    .year-wheel-hint {
        font-size: 0.7em;
        color: #666;
        margin-top: 0.5em;
    }
    
    .locked-indicator {
        font-size: 0.8em;
        color: #f59e0b;
        margin-top: 0.8em;
        padding: 0.5em;
        background: rgba(245, 158, 11, 0.1);
        border-radius: 8px;
    }
    
    /* ===== TIMER ===== */
    .timer-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
        padding: 0.5em;
        width: 100%;
    }
    
    .timer-ring {
        position: relative;
        width: 200px;
        height: 200px;
    }
    
    .timer-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
    }
    
    .timer-seconds {
        font-size: 4em;
        font-weight: 800;
        color: #22d3ee;
        line-height: 1;
    }
    
    .timer-label {
        font-size: 0.9em;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.3em;
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
    
    /* ===== ANSWER COMPARISON ===== */
    .answer-comparison {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.2em;
        margin: 0.5em 0;
    }
    
    .answer-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.6em 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .answer-row:last-of-type {
        border-bottom: none;
    }
    
    .answer-label {
        color: #888;
        font-size: 0.85em;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .answer-value {
        font-size: 2em;
        font-weight: 800;
        font-family: 'SF Mono', Monaco, monospace;
    }
    
    .answer-value.correct {
        color: #00ff88;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.4);
    }
    
    .answer-value.guess {
        color: #22d3ee;
        text-shadow: 0 0 20px rgba(34, 211, 238, 0.4);
    }
    
    .answer-diff {
        text-align: center;
        margin-top: 0.8em;
        padding-top: 0.8em;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        font-size: 1em;
        font-weight: 600;
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
        margin: 0.5em auto;
        width: 450px;
        max-width: 100%;
        padding: 10px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* ===== SONG HISTORY ===== */
    .history-container {
        margin: 2em auto;
        max-width: 600px;
        padding: 1em;
    }
    
    .history-header {
        font-size: 0.85em;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.8em;
        text-align: center;
    }
    
    .history-item {
        display: flex;
        align-items: center;
        gap: 0.8em;
        padding: 0.6em 1em;
        margin: 0.3em 0;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 8px;
        border-left: 3px solid #444;
        font-size: 0.85em;
    }
    
    .history-item.perfect { border-left-color: #22c55e; }
    .history-item.close { border-left-color: #22d3ee; }
    .history-item.ok { border-left-color: #a78bfa; }
    .history-item.far { border-left-color: #666; }
    
    .history-accuracy {
        width: 20px;
        text-align: center;
    }
    
    .history-song {
        flex: 1;
        color: #ccc;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .history-years {
        color: #888;
        font-family: 'SF Mono', Monaco, Consolas, monospace;
        font-size: 0.9em;
    }
    
    .history-score {
        color: #22d3ee;
        font-weight: 600;
        min-width: 45px;
        text-align: right;
    }
    
    /* ===== LISTEN BUTTON ===== */
    .listen-btn-container {
        text-align: center;
        margin: 1em 0;
    }
    
    .listen-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5em;
        padding: 0.6em 1.2em;
        background: transparent;
        border: 1px solid rgba(139, 92, 246, 0.4);
        border-radius: 20px;
        color: #a78bfa;
        font-size: 0.85em;
        text-decoration: none;
        transition: all 0.2s ease;
    }
    
    .listen-btn:hover {
        background: rgba(139, 92, 246, 0.15);
        border-color: rgba(139, 92, 246, 0.6);
        color: #c4b5fd;
        transform: scale(1.02);
    }
    
    .listen-btn.spotify-btn {
        background: rgba(30, 215, 96, 0.1);
        border-color: rgba(30, 215, 96, 0.5);
        color: #1DB954;
    }
    
    .listen-btn.spotify-btn:hover {
        background: rgba(30, 215, 96, 0.2);
        border-color: rgba(30, 215, 96, 0.8);
        color: #1ed760;
    }
    
    .listen-btn .spotify-icon {
        width: 20px;
        height: 20px;
        flex-shrink: 0;
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
    
    /* ===== CONTENT CONTAINER ===== */
    .content-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 1em;
    }
    
    /* ===== COMPACT SETTINGS ===== */
    .compact-settings {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2em;
        flex-wrap: wrap;
        padding: 0.8em 1em;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin: 0 auto 1em auto;
        max-width: 600px;
    }
    
    .setting-item {
        display: flex;
        align-items: center;
        gap: 0.4em;
        font-size: 0.85em;
    }
    
    .setting-label {
        color: #666;
        font-size: 0.75em;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .setting-value {
        color: #a78bfa;
        font-weight: 500;
    }
    
    /* Small inputs */
    .compact-settings .stTextInput > div > div > input {
        padding: 0.3em 0.5em !important;
        font-size: 0.85em !important;
        max-width: 120px !important;
    }
    
    .compact-settings .stNumberInput > div > div > input {
        padding: 0.3em 0.5em !important;
        font-size: 0.85em !important;
        width: 80px !important;
        min-width: 80px !important;
        max-width: 80px !important;
        text-align: center !important;
    }
    
    .compact-settings .stNumberInput {
        max-width: 100px !important;
    }
    
    .compact-settings .stNumberInput label {
        font-size: 0.7em !important;
        color: #888 !important;
    }
    
    .compact-settings .stNumberInput [data-baseweb="input"] button {
        display: none !important;
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
    
    .stSlider [data-baseweb="slider"] [role="slider"] {
        width: 24px !important;
        height: 24px !important;
        background: #22d3ee !important;
        border: 3px solid #fff !important;
        box-shadow: 0 0 15px rgba(34, 211, 238, 0.5) !important;
    }
    
    .stSlider [data-baseweb="slider"] [data-testid="stTickBar"] {
        display: none !important;
    }
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


def game_header(
    player_name: str, round_num: int, start_year: int, end_year: int, total_score: int = 0
) -> str:
    """Generate the game header with controls"""
    return f"""
    <div class="game-header">
        <div class="header-title">
            &#x1F3B5; Song Year Guesser
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
            <span class="music-icons">&#x1F3B5;</span>
            <span class="gradient-text">Song Year Guesser</span>
            <span class="music-icons">&#x1F3B5;</span>
        </h1>
        <div class="subtitle">Test your music knowledge</div>
    </div>
    """


def song_info_card(song: dict, blur_amount: float) -> str:
    """Generate the song info card with blur effect on values only"""
    blur_css = f"filter: blur({blur_amount:.1f}px);" if blur_amount > 0 else ""
    return f"""
    <div class="song-info-card">
        <div class="song-info-item">
            <span class="song-info-icon">&#x1F3B5;</span>
            <span class="song-info-label">Song</span>
            <span class="song-info-value" style="{blur_css}">{song["name"]}</span>
        </div>
        <div class="song-info-item">
            <span class="song-info-icon">&#x1F3A4;</span>
            <span class="song-info-label">Artist</span>
            <span class="song-info-value" style="{blur_css}">{song["artist"]}</span>
        </div>
        <div class="song-info-item">
            <span class="song-info-icon">&#x1F4BF;</span>
            <span class="song-info-label">Album</span>
            <span class="song-info-value" style="{blur_css}">{song["album"]}</span>
        </div>
    </div>
    """


def album_image(image_url: str, width: int = 280) -> str:
    """Generate album image HTML"""
    return f"""
    <div class="album-container">
        <img src="{image_url}" width="{width}" height="{width}" class="album-art">
    </div>
    """


def audio_visualizer(is_playing: bool = True) -> str:
    """Generate animated audio visualizer bars"""
    static_class = "" if is_playing else "audio-viz-static"
    bars = "".join(['<div class="audio-viz-bar"></div>' for _ in range(20)])
    return f"""
    <div class="audio-viz-container {static_class}">
        {bars}
    </div>
    """


def song_history_item(song: dict) -> str:
    """Generate a single song history item"""
    diff = abs(song["guess"] - song["actual"])
    if diff == 0:
        accuracy_class = "perfect"
        accuracy_icon = "&#x1F3AF;"
    elif diff <= 2:
        accuracy_class = "close"
        accuracy_icon = "&#x2713;"
    elif diff <= 5:
        accuracy_class = "ok"
        accuracy_icon = "&#x25CB;"
    else:
        accuracy_class = "far"
        accuracy_icon = "&#x2717;"

    return f"""
    <div class="history-item {accuracy_class}">
        <span class="history-accuracy">{accuracy_icon}</span>
        <span class="history-song">{song["song_name"]} - {song["artist"]}</span>
        <span class="history-years">{song["guess"]} / {song["actual"]}</span>
        <span class="history-score">+{song["score"]}</span>
    </div>
    """


def year_picker_display(year: int, start_year: int, end_year: int, locked: bool = False) -> str:
    """Generate the year display (not the input, just the visual)"""
    locked_class = "locked" if locked else ""
    locked_indicator = (
        '<div class="locked-indicator">&#x1F512; TIME\'S UP - Submit now!</div>' if locked else ""
    )
    prev_year = max(start_year, year - 1)
    next_year = min(end_year, year + 1)
    return f"""
    <div class="year-wheel-container {locked_class}">
        <div class="year-wheel-label">What year was this released?</div>
        <div class="year-wheel">
            <div class="year-wheel-inner">
                <div class="year-wheel-item adjacent">{prev_year if year > start_year else ""}</div>
                <div class="year-wheel-item selected {locked_class}">{year}</div>
                <div class="year-wheel-item adjacent">{next_year if year < end_year else ""}</div>
            </div>
        </div>
        <div class="year-range-label">{start_year} - {end_year}</div>
        <div class="year-wheel-hint">Scroll or use arrows</div>
        {locked_indicator}
    </div>
    """


def scroll_wheel_year_picker(
    current_year: int, start_year: int, end_year: int, locked: bool = False
) -> str:
    """Generate the JavaScript scroll wheel year picker - works with mouse wheel, trackpad, drag, click, keyboard"""
    locked_style = "opacity: 0.6; pointer-events: none;" if locked else ""
    locked_border = "rgba(239, 68, 68, 0.5)" if locked else "rgba(139, 92, 246, 0.4)"
    locked_indicator = (
        '<div style="color: #f59e0b; font-size: 0.8em; margin-top: 0.5em;">&#x1F512; TIME\'S UP - Submit now!</div>'
        if locked
        else ""
    )

    return f"""
    <div id="year-picker-wrapper" style="
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 0.5em 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        {locked_style}
    ">
        <div style="color: #888; text-transform: uppercase; letter-spacing: 2px; font-size: 0.7em; margin-bottom: 0.8em;">
            &#x1F3AF; Scroll to select year
        </div>
        
        <div id="scroll-container" style="
            position: relative;
            height: 200px;
            width: 280px;
            overflow: hidden;
            cursor: ns-resize;
            background: linear-gradient(180deg,
                rgba(10,10,20,1) 0%,
                rgba(10,10,20,0.8) 15%,
                transparent 35%,
                transparent 65%,
                rgba(10,10,20,0.8) 85%,
                rgba(10,10,20,1) 100%);
            border-radius: 16px;
            border: 2px solid {locked_border};
            touch-action: none;
            user-select: none;
            -webkit-user-select: none;
        ">
            <div id="year-track" style="
                position: absolute;
                width: 100%;
                text-align: center;
                transition: transform 0.08s ease-out;
            "></div>
            
            <div style="
                position: absolute;
                top: 50%;
                left: 10px;
                right: 10px;
                height: 56px;
                transform: translateY(-50%);
                border: 2px solid {"rgba(245, 158, 11, 0.6)" if locked else "rgba(34, 211, 238, 0.6)"};
                border-radius: 10px;
                pointer-events: none;
                box-shadow: 0 0 20px {"rgba(245, 158, 11, 0.2)" if locked else "rgba(34, 211, 238, 0.2)"};
            "></div>
        </div>
        
        <div style="color: #666; font-size: 0.75em; margin-top: 0.6em; letter-spacing: 1px;">
            {start_year} &#x2014; {end_year}
        </div>
        {locked_indicator}
    </div>
    
    <script>
    (function() {{
        const minYear = {start_year};
        const maxYear = {end_year};
        const isLocked = {"true" if locked else "false"};
        let currentYear = {current_year};
        let velocity = 0;
        let lastY = 0;
        let isDragging = false;
        let animationId = null;
        
        const container = document.getElementById('scroll-container');
        const track = document.getElementById('year-track');
        const itemHeight = 52;
        
        if (isLocked) {{
            container.style.cursor = 'not-allowed';
        }}
        
        function buildYearTrack() {{
            track.innerHTML = '';
            for (let year = minYear; year <= maxYear; year++) {{
                const div = document.createElement('div');
                div.className = 'year-item';
                div.dataset.year = year;
                div.style.cssText = `
                    height: ${{itemHeight}}px;
                    line-height: ${{itemHeight}}px;
                    font-size: 2.2em;
                    font-weight: 700;
                    font-family: 'SF Mono', Monaco, Consolas, monospace;
                    color: #444;
                    transition: color 0.1s, transform 0.1s, text-shadow 0.1s;
                `;
                div.textContent = year;
                track.appendChild(div);
            }}
            updatePosition(false);
        }}
        
        function updatePosition(animate = true) {{
            const offset = (currentYear - minYear) * itemHeight;
            const containerHeight = 200;
            const centerOffset = (containerHeight / 2) - (itemHeight / 2);
            track.style.transform = `translateY(${{centerOffset - offset}}px)`;
            if (!animate) track.style.transition = 'none';
            else track.style.transition = 'transform 0.08s ease-out';
            
            document.querySelectorAll('.year-item').forEach(item => {{
                const year = parseInt(item.dataset.year);
                const distance = Math.abs(year - currentYear);
                if (distance === 0) {{
                    item.style.color = isLocked ? '#f59e0b' : '#22d3ee';
                    item.style.transform = 'scale(1.15)';
                    item.style.textShadow = isLocked ? '0 0 30px rgba(245, 158, 11, 0.6)' : '0 0 30px rgba(34, 211, 238, 0.6)';
                }} else if (distance === 1) {{
                    item.style.color = '#666';
                    item.style.transform = 'scale(0.9)';
                    item.style.textShadow = 'none';
                }} else {{
                    item.style.color = '#444';
                    item.style.transform = 'scale(0.8)';
                    item.style.textShadow = 'none';
                }}
            }});
        }}
        
        function setYear(year, sendToStreamlit = true) {{
            if (isLocked) return;
            const newYear = Math.max(minYear, Math.min(maxYear, Math.round(year)));
            if (newYear !== currentYear) {{
                currentYear = newYear;
                updatePosition();
                if (sendToStreamlit) {{
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        value: currentYear
                    }}, '*');
                }}
            }}
        }}
        
        if (!isLocked) {{
            container.addEventListener('wheel', (e) => {{
                e.preventDefault();
                const delta = Math.sign(e.deltaY);
                setYear(currentYear + delta);
            }}, {{ passive: false }});
            
            container.addEventListener('mousedown', (e) => {{
                isDragging = true;
                lastY = e.clientY;
                velocity = 0;
                if (animationId) cancelAnimationFrame(animationId);
                e.preventDefault();
            }});
            
            container.addEventListener('touchstart', (e) => {{
                isDragging = true;
                lastY = e.touches[0].clientY;
                velocity = 0;
                if (animationId) cancelAnimationFrame(animationId);
            }}, {{ passive: true }});
            
            document.addEventListener('mousemove', (e) => {{
                if (!isDragging) return;
                const deltaY = lastY - e.clientY;
                velocity = deltaY;
                const yearDelta = deltaY / (itemHeight / 2);
                if (Math.abs(yearDelta) >= 0.5) {{
                    setYear(currentYear + Math.sign(yearDelta));
                    lastY = e.clientY;
                }}
            }});
            
            document.addEventListener('touchmove', (e) => {{
                if (!isDragging) return;
                const deltaY = lastY - e.touches[0].clientY;
                velocity = deltaY;
                const yearDelta = deltaY / (itemHeight / 2);
                if (Math.abs(yearDelta) >= 0.5) {{
                    setYear(currentYear + Math.sign(yearDelta));
                    lastY = e.touches[0].clientY;
                }}
            }}, {{ passive: true }});
            
            document.addEventListener('mouseup', () => {{
                if (isDragging) {{
                    isDragging = false;
                    if (Math.abs(velocity) > 5) {{
                        let momentum = velocity * 0.3;
                        function animate() {{
                            if (Math.abs(momentum) > 0.5) {{
                                setYear(currentYear + Math.sign(momentum));
                                momentum *= 0.85;
                                animationId = requestAnimationFrame(animate);
                            }}
                        }}
                        animate();
                    }}
                }}
            }});
            
            document.addEventListener('touchend', () => {{
                if (isDragging) {{
                    isDragging = false;
                    if (Math.abs(velocity) > 5) {{
                        let momentum = velocity * 0.3;
                        function animate() {{
                            if (Math.abs(momentum) > 0.5) {{
                                setYear(currentYear + Math.sign(momentum));
                                momentum *= 0.85;
                                animationId = requestAnimationFrame(animate);
                            }}
                        }}
                        animate();
                    }}
                }}
            }});
            
            container.addEventListener('click', (e) => {{
                if (Math.abs(velocity) > 2) return;
                const rect = container.getBoundingClientRect();
                const clickY = e.clientY - rect.top;
                const centerY = rect.height / 2;
                const diff = Math.round((clickY - centerY) / itemHeight);
                if (diff !== 0) setYear(currentYear + diff);
            }});
            
            container.setAttribute('tabindex', '0');
            container.addEventListener('keydown', (e) => {{
                if (e.key === 'ArrowUp') {{ setYear(currentYear - 1); e.preventDefault(); }}
                if (e.key === 'ArrowDown') {{ setYear(currentYear + 1); e.preventDefault(); }}
                if (e.key === 'PageUp') {{ setYear(currentYear - 5); e.preventDefault(); }}
                if (e.key === 'PageDown') {{ setYear(currentYear + 5); e.preventDefault(); }}
            }});
        }}
        
        buildYearTrack();
        
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: currentYear
        }}, '*');
    }})();
    </script>
    """


def timer_html(start_timestamp: float, max_time: int) -> str:
    """Generate the countdown timer with animation - includes inline styles for iframe"""
    return f"""
    <style>
        body {{ margin: 0; padding: 0; background: transparent; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
        .timer-container {{ display: flex; justify-content: center; align-items: center; width: 100%; height: 100%; }}
        .timer-ring {{ position: relative; width: 200px; height: 200px; filter: drop-shadow(0 0 20px rgba(34, 211, 238, 0.4)); transition: filter 0.3s ease; }}
        .timer-ring.warning {{ filter: drop-shadow(0 0 25px rgba(245, 158, 11, 0.5)); }}
        .timer-ring.danger {{ filter: drop-shadow(0 0 30px rgba(239, 68, 68, 0.6)); animation: pulse 0.5s ease-in-out infinite; }}
        .timer-ring.paused {{ opacity: 0.6; }}
        .timer-text {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; }}
        .timer-seconds {{ font-size: 4em; font-weight: 800; color: #22d3ee; line-height: 1; text-shadow: 0 0 30px currentColor; transition: color 0.3s ease, text-shadow 0.3s ease; }}
        .timer-label {{ font-size: 0.9em; color: #888; text-transform: uppercase; letter-spacing: 2px; margin-top: 0.3em; }}
        @keyframes pulse {{ 0%, 100% {{ transform: scale(1); }} 50% {{ transform: scale(1.05); }} }}
    </style>
    <div class="timer-container">
        <div class="timer-ring" id="timer-ring">
            <svg width="200" height="200" viewBox="0 0 200 200" style="transform: rotate(-90deg);">
                <circle cx="100" cy="100" r="90" fill="none" stroke="#1e1e3f" stroke-width="10"/>
                <circle id="timer-circle" cx="100" cy="100" r="90" fill="none" stroke="#22d3ee" stroke-width="10"
                    stroke-linecap="round" stroke-dasharray="565" stroke-dashoffset="0"
                    style="transition: stroke-dashoffset 0.1s linear, stroke 0.3s ease; filter: drop-shadow(0 0 8px currentColor);"/>
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
            var ring = document.getElementById('timer-ring');
            var circumference = 2 * Math.PI * 90;

            // Pause tracking
            var isPaused = false;
            var pausedAt = null;
            var accumulatedPausedTime = 0;

            function pause() {{
                if (!isPaused) {{
                    isPaused = true;
                    pausedAt = Date.now();
                    ring.classList.add('paused');
                }}
            }}

            function resume() {{
                if (isPaused && pausedAt !== null) {{
                    accumulatedPausedTime += (Date.now() - pausedAt);
                    isPaused = false;
                    pausedAt = null;
                    ring.classList.remove('paused');
                }}
            }}

            function getElapsedTime() {{
                var now = Date.now();
                var totalPausedTime = accumulatedPausedTime;
                if (isPaused && pausedAt !== null) {{
                    totalPausedTime += (now - pausedAt);
                }}
                var elapsed = ((now - startTime) - totalPausedTime) / 1000;
                return elapsed;
            }}

            function updateTimer() {{
                var elapsed = getElapsedTime();
                if (elapsed < 0) elapsed = 0;
                if (elapsed > maxTime) elapsed = maxTime;

                var remaining = Math.ceil(maxTime - elapsed);
                var progress = elapsed / maxTime;
                var offset = circumference * progress;

                circle.style.strokeDashoffset = offset;
                secondsEl.textContent = remaining;

                ring.classList.remove('warning', 'danger');
                if (remaining <= 5) {{
                    circle.style.stroke = '#ef4444';
                    secondsEl.style.color = '#ef4444';
                    secondsEl.style.textShadow = '0 0 40px #ef4444';
                    ring.classList.add('danger');
                }} else if (remaining <= 10) {{
                    circle.style.stroke = '#f59e0b';
                    secondsEl.style.color = '#f59e0b';
                    secondsEl.style.textShadow = '0 0 35px #f59e0b';
                    ring.classList.add('warning');
                }} else {{
                    circle.style.stroke = '#22d3ee';
                    secondsEl.style.color = '#22d3ee';
                    secondsEl.style.textShadow = '0 0 30px #22d3ee';
                }}

                // Send elapsed time to parent for blur calculation
                try {{
                    window.parent.postMessage({{
                        type: 'timer:elapsed',
                        elapsed: elapsed
                    }}, '*');
                }} catch(e) {{}}
            }}

            // Expose pause/resume to parent window
            window.timerControl = {{
                pause: pause,
                resume: resume,
                getElapsedTime: getElapsedTime
            }};

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
            <svg width="200" height="200" viewBox="0 0 200 200" style="transform: rotate(-90deg);">
                <circle cx="100" cy="100" r="90" fill="none" stroke="#1e1e3f" stroke-width="10"/>
                <circle cx="100" cy="100" r="90" fill="none" stroke="#22d3ee" stroke-width="10" stroke-dasharray="565"/>
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


def correct_answer_with_diff(actual_year: int, guessed_year: int) -> str:
    """Generate the correct answer display with year difference"""
    diff = guessed_year - actual_year
    abs_diff = abs(diff)

    if diff == 0:
        diff_text = '<span style="color: #00ff88;">Perfect match!</span>'
        diff_class = "perfect"
    elif diff > 0:
        diff_text = f'<span style="color: #ef4444;">+{diff} years (too recent)</span>'
        diff_class = "off"
    else:
        diff_text = f'<span style="color: #3b82f6;">{diff} years (too early)</span>'
        diff_class = "off"

    return f"""
    <div class="answer-comparison">
        <div class="answer-row">
            <span class="answer-label">Correct Year</span>
            <span class="answer-value correct">{actual_year}</span>
        </div>
        <div class="answer-row">
            <span class="answer-label">Your Guess</span>
            <span class="answer-value guess">{guessed_year}</span>
        </div>
        <div class="answer-diff">{diff_text}</div>
    </div>
    """


def score_card(score: int) -> str:
    """Generate the score card display"""
    return f'<div class="score-card">&#x1F3AF; {score} points</div>'


def status_line(message: str) -> str:
    """Generate a status message line"""
    return f'<div class="status-line">{message}</div>'


def spotify_button(url: str) -> str:
    """Generate a Spotify listen button"""
    return f"""
    <div class="listen-btn-container">
        <a href="{url}" target="_blank" class="listen-btn spotify-btn">
            <svg class="spotify-icon" width="20" height="20" viewBox="0 0 24 24" fill="#1DB954">
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
        <h3>&#x1F3AE; How to Play</h3>
        <ol>
            <li><strong>&#x1F3A7; Listen</strong> to a 30-second song preview</li>
            <li><strong>&#x1F5BC;&#xFE0F; Watch</strong> the album artwork and song info gradually reveal</li>
            <li><strong>&#x1F3AF; Select</strong> your guess for the release year</li>
            <li><strong>&#x26A1; Submit</strong> anytime - the faster you guess, the more bonus points!</li>
        </ol>
        <div style="text-align: center; margin-top: 1em; padding: 0.8em; background: rgba(34, 211, 238, 0.15); border: 1px solid rgba(34, 211, 238, 0.3); border-radius: 10px; color: #22d3ee;">
            &#x26A1; <strong>Time Bonus:</strong> Submit early for up to 300 extra points!
        </div>
        <div style="text-align: center; margin-top: 0.5em; padding: 0.8em; background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 10px; color: #f59e0b;">
            &#x1F512; After 30 seconds, your selection locks - submit before time runs out!
        </div>
    </div>
    """


def leaderboard_entry(idx: int, score: dict) -> str:
    """Generate a single leaderboard entry for cumulative leaderboard"""
    medal = (
        "&#x1F947;"
        if idx == 1
        else "&#x1F948;"
        if idx == 2
        else "&#x1F949;"
        if idx == 3
        else f"#{idx}"
    )
    genre = score.get("genre", "All Genres")
    songs_played = score.get("songs_played", 0)
    avg_score = score.get("avg_score", 0)
    date = score.get("date", "")
    return f"""
    <div class="leaderboard">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: 1.3em;">{medal}</span>
                <strong style="color: #8b5cf6;">{score["player"]}</strong>
            </div>
            <div style="font-size: 1.2em; font-weight: 700; color: #22d3ee;">{score["total_score"]} pts</div>
        </div>
        <div style="font-size: 0.85em; color: #a0a0a0; margin-top: 0.3em;">
            {genre} • {songs_played} songs • Avg: {avg_score} pts • {date}
        </div>
    </div>
    """


def audio_player(preview_url: str, song_id: str, autoplay: bool = True) -> str:
    """Generate an audio player with visualizer and timer sync"""
    autoplay_attr = "autoplay" if autoplay else ""
    return f"""
    <div class="audio-container">
        <audio id="gameAudio" controls {autoplay_attr} style="width: 100%; border-radius: 10px;">
            <source src="{preview_url}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
    </div>
    <script>
        (function() {{
            var audio = document.getElementById('gameAudio');
            if (!audio) return;

            // Find visualizer in parent document
            function getVizContainer() {{
                try {{
                    return window.parent.document.querySelector('.audio-viz-container');
                }} catch(e) {{
                    return null;
                }}
            }}

            // Find timer iframe and access its control functions
            function getTimerControl() {{
                try {{
                    var iframes = window.parent.document.querySelectorAll('iframe');
                    for (var i = 0; i < iframes.length; i++) {{
                        if (iframes[i].contentWindow && iframes[i].contentWindow.timerControl) {{
                            return iframes[i].contentWindow.timerControl;
                        }}
                    }}
                }} catch(e) {{
                    return null;
                }}
                return null;
            }}

            function notifyAutoplayStatus(blocked) {{
                try {{
                    window.parent.postMessage({{
                        type: 'audio:autoplay',
                        blocked: blocked
                    }}, '*');
                }} catch(e) {{
                    console.log('Could not notify autoplay status:', e);
                }}
            }}

            function updateViz(playing) {{
                var viz = getVizContainer();
                if (viz) {{
                    if (playing) {{
                        viz.classList.remove('audio-viz-static');
                    }} else {{
                        viz.classList.add('audio-viz-static');
                    }}
                }}
            }}

            function updateTimer(playing) {{
                var timerControl = getTimerControl();
                if (timerControl) {{
                    if (playing) {{
                        timerControl.resume();
                    }} else {{
                        timerControl.pause();
                    }}
                }}
            }}

            audio.addEventListener('play', function() {{
                updateViz(true);
                updateTimer(true);
                notifyAutoplayStatus(false);
            }});
            audio.addEventListener('pause', function() {{
                updateViz(false);
                updateTimer(false);
            }});
            audio.addEventListener('ended', function() {{
                updateViz(false);
                updateTimer(false);
            }});

            {'audio.volume = 1.0; audio.play().then(function() { notifyAutoplayStatus(false); }).catch(function(e) { console.log("Autoplay prevented:", e); notifyAutoplayStatus(true); });' if autoplay else ""}
        }})();
    </script>
    """


def leaderboard_header() -> str:
    """Generate the leaderboard header"""
    return '<div class="leaderboard-header">&#x1F3C6; Leaderboard</div>'


def empty_leaderboard() -> str:
    """Generate empty leaderboard message"""
    return '<div style="text-align: center; color: #666; padding: 1.5em; font-size: 0.9em;">&#x1F3AE; No scores yet! Play a game to see your scores here.</div>'


def elapsed_time_receiver() -> str:
    """Component that receives elapsed time from timer and stores in localStorage"""
    return """
    <script>
        (function() {
            var lastElapsed = 0;

            window.addEventListener('message', function(event) {
                if (event.data && event.data.type === 'timer:elapsed') {
                    lastElapsed = event.data.elapsed;
                    try {
                        localStorage.setItem('gameTimerElapsed', lastElapsed.toString());
                    } catch(e) {}
                }
            });

            // Also check timer iframes directly
            function updateFromTimer() {
                try {
                    var iframes = window.parent.document.querySelectorAll('iframe');
                    for (var i = 0; i < iframes.length; i++) {
                        if (iframes[i].contentWindow && iframes[i].contentWindow.timerControl) {
                            var elapsed = iframes[i].contentWindow.timerControl.getElapsedTime();
                            if (elapsed !== undefined && elapsed !== null) {
                                lastElapsed = elapsed;
                                localStorage.setItem('gameTimerElapsed', elapsed.toString());
                            }
                            break;
                        }
                    }
                } catch(e) {}
            }

            setInterval(updateFromTimer, 200);
        })();
    </script>
    """


def get_elapsed_time_js() -> str:
    """Component that gets elapsed time from timer or localStorage"""
    return """
    <script>
        (function() {
            function getElapsedTime() {
                // First try to get directly from timer iframe
                try {
                    var iframes = window.parent.document.querySelectorAll('iframe');
                    for (var i = 0; i < iframes.length; i++) {
                        if (iframes[i].contentWindow && iframes[i].contentWindow.timerControl) {
                            var elapsed = iframes[i].contentWindow.timerControl.getElapsedTime();
                            if (elapsed !== undefined && elapsed !== null) {
                                window.parent.postMessage({
                                    type: 'streamlit:setComponentValue',
                                    value: elapsed
                                }, '*');
                                return;
                            }
                        }
                    }
                } catch(e) {}

                // Fallback to localStorage
                try {
                    var stored = localStorage.getItem('gameTimerElapsed');
                    if (stored) {
                        window.parent.postMessage({
                            type: 'streamlit:setComponentValue',
                            value: parseFloat(stored)
                        }, '*');
                        return;
                    }
                } catch(e) {}

                // Default to 0
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: 0
                }, '*');
            }

            getElapsedTime();
        })();
    </script>
    """


def autoplay_status_receiver() -> str:
    """Component that receives autoplay status from audio player"""
    return """<script>(function(){try{localStorage.removeItem('autoplayBlocked');}catch(e){}window.addEventListener('message',function(e){if(e.data&&e.data.type==='audio:autoplay'){try{localStorage.setItem('autoplayBlocked',e.data.blocked?'true':'false')}catch(err){}}})})();</script>"""


def check_autoplay_blocked() -> str:
    """Check if autoplay is blocked in localStorage"""
    return """<script>(function(){try{var b=localStorage.getItem('autoplayBlocked');window.parent.postMessage({type:'streamlit:setComponentValue',value:b==='true'},'*')}catch(e){window.parent.postMessage({type:'streamlit:setComponentValue',value:false},'*')}})();</script>"""


def autoplay_warning() -> str:
    """Warning message when autoplay is blocked"""
    return """
    <div style="
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.15) 100%);
        border: 2px solid rgba(239, 68, 68, 0.5);
        border-radius: 12px;
        padding: 1.2em;
        margin: 1em 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.2);
    ">
        <div style="font-size: 2em; margin-bottom: 0.3em;">🔇</div>
        <div style="font-size: 1.1em; font-weight: 700; color: #ef4444; margin-bottom: 0.5em;">
            Autoplay is Blocked
        </div>
        <div style="font-size: 0.95em; color: #fca5a5; line-height: 1.5; margin-bottom: 0.8em;">
            Your browser has prevented the audio from playing automatically.<br>
            <strong>Please click the play button (▶) below to start the song!</strong>
        </div>
        <details style="margin-top: 0.8em; padding: 0.8em; background: rgba(0, 0, 0, 0.2); border-radius: 8px; cursor: pointer;">
            <summary style="color: #fca5a5; font-weight: 600; font-size: 0.9em;">How to enable autoplay in your browser</summary>
            <div style="margin-top: 0.8em; text-align: left; font-size: 0.85em; color: #fecaca; line-height: 1.6;">
                <strong style="color: #f87171;">Chrome/Edge:</strong><br>
                • Click the lock/info icon in the address bar<br>
                • Find "Sound" and change it to "Allow"<br>
                • Refresh the page<br><br>

                <strong style="color: #f87171;">Firefox:</strong><br>
                • Click the settings icon in the address bar<br>
                • Find "Autoplay" and set to "Allow Audio and Video"<br>
                • Refresh the page<br><br>

                <strong style="color: #f87171;">Safari:</strong><br>
                • Go to Settings for This Website<br>
                • Set "Auto-Play" to "Allow All Auto-Play"<br>
                • Refresh the page
            </div>
        </details>
    </div>
    """


def settings_row() -> str:
    """Generate opening div for compact settings row"""
    return '<div class="compact-settings">'
