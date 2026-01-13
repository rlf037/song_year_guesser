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

    /* Import Inter font for modern typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Modern dark theme - sophisticated charcoal with indigo accents */
    .stApp {
        background: linear-gradient(135deg, #0a0e14 0%, #111827 35%, #1e293b 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #e2e8f0;
        line-height: 1.6;
    }

    /* ===== HEADER SECTION ===== */
    .game-header {
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(71, 85, 105, 0.4);
        padding: 1em 2em;
        margin: -1em -1em 2em -1em;
        display: flex;
        flex-direction: column;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    .header-title {
        font-size: 1.6em;
        font-weight: 600;
        color: #818cf8;
        display: flex;
        align-items: center;
        gap: 0.5em;
        letter-spacing: -0.02em;
        margin-bottom: 0.8em;
    }

    .header-controls {
        display: flex;
        flex-wrap: nowrap;
        justify-content: center;
        align-items: center;
        gap: 0.8em;
        width: 100%;
        margin: 0 auto;
        max-width: 1100px;
    }

    .header-item {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.4em;
        color: #94a3b8;
        font-size: 0.9em;
        padding: 0.4em 0.9em;
        background: rgba(30, 41, 59, 0.6);
        border-radius: 8px;
        border: 1px solid rgba(71, 85, 105, 0.3);
        backdrop-filter: blur(10px);
        white-space: nowrap;
        flex: 0 0 auto;
    }

    .header-item-label {
        color: #64748b;
        font-size: 0.7em;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }

    .header-item-value {
        color: #f1f5f9;
        font-weight: 600;
    }

    .round-indicator {
        background: rgba(139, 148, 158, 0.1);
        border: 1px solid rgba(139, 148, 158, 0.3);
        padding: 0.3em 0.8em;
        border-radius: 15px;
        color: #c9d1d9;
        font-weight: 600;
        font-size: 0.85em;
    }

    /* ===== MAIN TITLE (Welcome Screen) ===== */
    .main-title {
        text-align: center;
        margin: 6.5em 0 3.5em 0;
    }

    .main-title h1 {
        font-size: clamp(2.2em, 7vw, 4em);
        font-weight: 800;
        margin: 0 auto;
        padding: 0;
        line-height: 1.1;
        max-width: 95vw;
        word-break: break-word;
        overflow-wrap: break-word;
        white-space: normal;
        text-overflow: ellipsis;
    }
    @media (max-width: 600px) {
        .main-title {
            margin: 2em 0 1.2em 0;
        }
        .main-title h1 {
            font-size: clamp(1.3em, 9vw, 2.5em);
            padding: 0 0.2em;
        }
        .game-header {
            padding: 0.7em 0.5em;
            gap: 1em;
        }
        .header-title {
            font-size: 1.1em;
        }
    }

    .main-title .gradient-text {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 2px 10px rgba(99, 102, 241, 0.3);
    }

    .main-title .subtitle {
        font-size: 1.2em;
        color: #6e7681;
        margin-top: 2.5em;
        margin-bottom: 2.5em;
        font-weight: 400;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .main-title .music-icons {
        font-size: 0.6em;
        margin: 0 0.2em;
        opacity: 0.7;
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
        /* Stretch columns to equal height so we can align bottoms */
        align-items: stretch;
        gap: 2em;
        width: 100%;
        margin: 1em 0;
        /* Force a much taller row so timer/submit can be positioned lower */
        min-height: 700px;
    }

    @media (max-width: 600px) {
        .game-row {
            flex-direction: column;
            align-items: center;
        }
    }

    /* Make direct children of the main row behave as columns that distribute
       space vertically. This ensures bottom-aligned elements (timer/submit)
       sit aligned with the bottom of the song info card. */
    .game-row > div {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        /* Ensure both columns meet the forced row height so bottoms align (slightly increased) */
        min-height: 700px;
    }

    /* ===== SONG INFO CARD ===== */
    .song-info-card {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(71, 85, 105, 0.4);
        border-radius: 16px;
        padding: 1.2em 1.5em;
        max-width: 450px;
        width: 100%;
        margin-top: 0.5em;
        box-sizing: border-box;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }

    .song-info-item {
        display: flex;
        align-items: center;
        padding: 0.4em 0;
        border-bottom: 1px solid rgba(48, 54, 61, 0.6);
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
        color: #6e7681;
        font-size: 0.75em;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 50px;
    }

    .song-info-value {
        color: #c9d1d9;
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
        border-radius: 12px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.5);
        border: 2px solid rgba(48, 54, 61, 0.8);
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
        gap: 3px;
        height: 35px;
        margin: 0.8em 0 0.5em 0;
        max-width: 450px;
        width: 100%;
    }

    .audio-viz-bar {
        width: 5px;
        background: linear-gradient(to top, #5558b0, #818cf8);
        border-radius: 2px;
        animation: audioViz 0.5s ease-in-out infinite alternate;
    }

    .audio-viz-bar:nth-child(1) { animation-delay: 0s; height: 10px; }
    .audio-viz-bar:nth-child(2) { animation-delay: 0.1s; height: 18px; }
    .audio-viz-bar:nth-child(3) { animation-delay: 0.15s; height: 12px; }
    .audio-viz-bar:nth-child(4) { animation-delay: 0.2s; height: 24px; }
    .audio-viz-bar:nth-child(5) { animation-delay: 0.05s; height: 14px; }
    .audio-viz-bar:nth-child(6) { animation-delay: 0.25s; height: 20px; }
    .audio-viz-bar:nth-child(7) { animation-delay: 0.1s; height: 10px; }
    .audio-viz-bar:nth-child(8) { animation-delay: 0.3s; height: 26px; }
    .audio-viz-bar:nth-child(9) { animation-delay: 0.15s; height: 16px; }
    .audio-viz-bar:nth-child(10) { animation-delay: 0.2s; height: 12px; }
    .audio-viz-bar:nth-child(11) { animation-delay: 0.25s; height: 20px; }
    .audio-viz-bar:nth-child(12) { animation-delay: 0.05s; height: 14px; }
    .audio-viz-bar:nth-child(13) { animation-delay: 0.3s; height: 22px; }
    .audio-viz-bar:nth-child(14) { animation-delay: 0.1s; height: 10px; }
    .audio-viz-bar:nth-child(15) { animation-delay: 0.2s; height: 16px; }
    .audio-viz-bar:nth-child(16) { animation-delay: 0.15s; height: 20px; }
    .audio-viz-bar:nth-child(17) { animation-delay: 0.25s; height: 12px; }
    .audio-viz-bar:nth-child(18) { animation-delay: 0.1s; height: 18px; }
    .audio-viz-bar:nth-child(19) { animation-delay: 0.2s; height: 14px; }
    .audio-viz-bar:nth-child(20) { animation-delay: 0.05s; height: 20px; }

    @keyframes audioViz {
        0% { transform: scaleY(0.3); opacity: 0.4; }
        100% { transform: scaleY(1); opacity: 1; }
    }

    .audio-viz-static .audio-viz-bar {
        animation: none;
        opacity: 0.2;
        transform: scaleY(0.3);
    }

    /* ===== YEAR PICKER ===== */
    .year-picker-label {
        font-size: 0.9em;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        text-align: center;
        margin-bottom: 0.5em;
        font-weight: 500;
    }

    .year-display {
        font-size: 4em;
        font-weight: 700;
        color: #f1f5f9;
        text-align: center;
        font-family: 'SF Mono', Monaco, Consolas, monospace;
        margin: 0.2em 0 0.5em 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        letter-spacing: -0.02em;
    }

    .year-display.locked {
        color: #64748b;
    }

    /* ===== YEAR WHEEL (legacy) ===== */
    .year-wheel-container {
        background: rgba(22, 27, 34, 0.6);
        border: 1px solid rgba(48, 54, 61, 0.8);
        border-radius: 16px;
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
        /* Reduced height (50%) so the wheel takes less vertical space */
        height: 180px;
        overflow: hidden;
        position: relative;
        cursor: ns-resize;
        -webkit-user-select: none;
        user-select: none;
    }

    /* Ensure extra spacing above the year picker for clearer separation */
    #year-picker-wrapper {
        margin-top: 2.4em !important;
        /* Nudge bottom space slightly to move submit down (~10%) */
        margin-bottom: 6.6em !important;
        padding-bottom: 0.9em;
    }
    @media (max-width: 600px) {
        #year-picker-wrapper { margin-top: 1.2em !important; }
        .compact-settings { margin-bottom: 1.6em !important; }
    }

    .year-wheel-inner {
        display: flex;
        flex-direction: column;
        align-items: center;
        transition: transform 0.1s ease-out;
    }

    .year-wheel-item {
        height: 35px;
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
        font-size: 1.8em;
        color: #e6edf3;
        text-shadow: 0 0 20px rgba(230, 237, 243, 0.35);
    }

    .year-wheel-item.selected.locked {
        color: #8b949e;
        text-shadow: none;
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
        color: #8b949e;
        margin-top: 0.8em;
        padding: 0.5em;
        background: rgba(139, 148, 158, 0.1);
        border-radius: 8px;
    }

    /* ===== TIMER ===== */
    .timer-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
        /* Nudge timer upward slightly to move it up by roughly 2% */
        transform: translateY(-2%);
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
        color: #f1f5f9;
        line-height: 1;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    .timer-label {
        font-size: 0.9em;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 500;
        margin-top: 0.3em;
    }

    /* ===== BUTTONS ===== */
    .stButton > button {
        min-height: 3em;
        font-weight: 600;
        border-radius: 12px;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }

    /* Center the score message used in the status area */
    .score-card {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        width: 100%;
    }

    .stButton > button:disabled {
        opacity: 0.4;
        cursor: not-allowed;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2ea043 0%, #238636 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 12px rgba(35, 134, 54, 0.3);
    }

    .stButton > button[kind="primary"]:hover:not(:disabled) {
        background: linear-gradient(135deg, #3cb04c 0%, #2ea043 100%);
        box-shadow: 0 6px 20px rgba(35, 134, 54, 0.4);
        transform: translateY(-1px);
    }

    /* Main submit button styling - modern indigo gradient with depth */
    .stButton > button[kind="primary"][data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #7c3aed 100%);
        color: white;
        font-size: 1.2em;
        font-weight: 600;
        padding: 0.9em 2.5em;
        border-radius: 12px;
        border: none;
        box-shadow:
            0 8px 25px rgba(99, 102, 241, 0.3),
            0 2px 10px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        letter-spacing: 0.02em;
    }

    /* Move primary submit button much lower within its column so the scroll wheel is visible */
    .game-row > div .stButton > button[data-testid="baseButton-primary"] {
        position: absolute;
        top: 92%;
        left: 50%;
        transform: translate(-50%, -50%);
    }

    .stButton > button[kind="primary"][data-testid="baseButton-primary"]:hover:not(:disabled) {
        background: linear-gradient(135deg, #4f46e5 0%, #6d28d9 100%);
        box-shadow:
            0 12px 35px rgba(99, 102, 241, 0.4),
            0 4px 15px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        transform: translateY(-2px) scale(1.02);
    }

    .stButton > button[kind="primary"][data-testid="baseButton-primary"]:active:not(:disabled) {
        transform: translateY(0) scale(0.98);
        box-shadow:
            0 4px 15px rgba(99, 102, 241, 0.3),
            0 1px 6px rgba(0, 0, 0, 0.2);
        transition: all 0.1s ease;
    }

    /* Urgent submit button when time is up - applied via JavaScript */
    .stButton > button.urgent-submit {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 50%, #c2410c 100%) !important;
        color: white !important;
        font-size: 1.4em !important;
        font-weight: 700 !important;
        padding: 1.1em 2.5em !important;
        border-radius: 20px !important;
        border: none !important;
        box-shadow:
            0 0 40px rgba(239, 68, 68, 0.6),
            0 8px 24px rgba(220, 38, 38, 0.4),
            0 4px 12px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.3),
            inset 0 -2px 8px rgba(0, 0, 0, 0.2) !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        animation: urgentPulse 0.8s ease-in-out infinite !important;
        position: relative !important;
    }

    .stButton > button.urgent-submit::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, transparent 100%);
        border-radius: 20px;
        pointer-events: none;
    }

    .stButton > button.urgent-submit:hover:not(:disabled) {
        background: linear-gradient(135deg, #f87171 0%, #ef4444 50%, #dc2626 100%) !important;
        transform: translateY(-2px) scale(1.05) !important;
        box-shadow:
            0 0 50px rgba(239, 68, 68, 0.8),
            0 12px 32px rgba(220, 38, 38, 0.5),
            0 6px 16px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
    }

    @keyframes urgentPulse {
        0%, 100% {
            transform: scale(1) translateY(0);
            box-shadow:
                0 0 35px rgba(239, 68, 68, 0.5),
                0 8px 24px rgba(220, 38, 38, 0.35),
                0 4px 12px rgba(0, 0, 0, 0.25),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
        }
        50% {
            transform: scale(1.06) translateY(-3px);
            box-shadow:
                0 0 50px rgba(239, 68, 68, 0.8),
                0 12px 32px rgba(220, 38, 38, 0.5),
                0 6px 16px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.4);
        }
    }

    /* JavaScript to apply urgent styling removed from CSS; use URGENT_BUTTON_SCRIPT for injection */

    /* ===== SCORE CARD ===== */
    .score-card {
        background: rgba(35, 134, 54, 0.15);
        border: 1px solid rgba(35, 134, 54, 0.4);
        padding: 0.8em 1.5em;
        border-radius: 8px;
        text-align: center;
        color: #3fb950;
        font-size: 1em;
        font-weight: 500;
        margin: 0.8em auto;
        max-width: 400px;
        line-height: 1.4;
    }

    /* ===== CORRECT ANSWER ===== */
    .correct-answer {
        font-size: 1.8em;
        font-weight: 700;
        color: #818cf8;
        text-align: center;
        margin: 0.5em 0;
    }

    /* ===== ANSWER COMPARISON ===== */
    .answer-comparison {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid rgba(48, 54, 61, 0.8);
        border-radius: 12px;
        padding: 1.2em;
        margin: 0.5em 0;
    }

    .answer-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.6em 0;
        border-bottom: 1px solid rgba(48, 54, 61, 0.6);
    }

    .answer-row:last-of-type {
        border-bottom: none;
    }

    .answer-label {
        color: #6e7681;
        font-size: 0.85em;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .answer-value {
        font-size: 2em;
        font-weight: 700;
        font-family: 'SF Mono', Monaco, monospace;
    }

    .answer-value.correct {
        color: #3fb950;
    }

    .answer-value.guess {
        color: #818cf8;
    }

    .answer-diff {
        text-align: center;
        margin-top: 0.8em;
        padding-top: 0.8em;
        border-top: 1px solid rgba(48, 54, 61, 0.6);
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
        font-size: 3em;
        margin-bottom: 0.2em;
    }

    .result-message {
        font-size: 1.8em;
        font-weight: 700;
    }

    .result-subtitle {
        color: #8b949e;
        margin-top: 0.3em;
    }

    /* ===== AUDIO PLAYER ===== */
    .audio-container {
        margin: 0.5em auto;
        width: 450px;
        max-width: 100%;
        padding: 10px;
        background: rgba(22, 27, 34, 0.8);
        border-radius: 8px;
        border: 1px solid rgba(48, 54, 61, 0.8);
    }

    /* ===== SONG HISTORY ===== */
    .history-container {
        margin: 2em auto;
        max-width: 600px;
        padding: 1em;
    }

    .history-header {
        font-size: 0.85em;
        color: #6e7681;
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
        background: rgba(22, 27, 34, 0.6);
        border-radius: 6px;
        border-left: 3px solid #30363d;
        font-size: 0.85em;
    }

    .history-item.perfect { border-left-color: #3fb950; }
    .history-item.close { border-left-color: #58a6ff; }
    .history-item.ok { border-left-color: #8b949e; }
    .history-item.far { border-left-color: #484f58; }

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
        color: #a78bfa;
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
        color: #7b9ae0;
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
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 1.5em 2em;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        color: #f1f5f9;
        border: 1px solid rgba(71, 85, 105, 0.4);
        margin: 0.5em auto;
        max-width: 600px;
    }

    .leaderboard-header {
        text-align: center;
        font-size: 1.4em;
        font-weight: 600;
        color: #818cf8;
        margin-bottom: 1.2em;
        letter-spacing: -0.02em;
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
        color: #7b9ae0;
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

    /* Add extra space below compact settings (user input boxes) */
    .compact-settings {
        margin-bottom: 3.0em !important;
    }

    /* ===== HOW TO PLAY ===== */
    .how-to-play {
        background: rgba(22, 27, 34, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1.8em 2.5em;
        margin: 1em auto;
        max-width: 600px;
        border: 1px solid rgba(48, 54, 61, 0.6);
        color: #c9d1d9;
    }

    .how-to-play h3 {
        color: #e6edf3;
        margin-bottom: 1em;
        text-align: center;
        font-weight: 600;
        font-size: 1.2em;
    }

    .how-to-play ol {
        text-align: left;
        line-height: 2;
        color: #c9d1d9;
        margin: 0;
        padding-left: 1.5em;
    }

    .how-to-play ol li {
        margin-bottom: 0.5em;
    }

    .how-to-play-tip {
        text-align: center;
        margin-top: 1.5em;
        padding: 0.8em 1.2em;
        background: rgba(48, 54, 61, 0.4);
        border: 1px solid rgba(110, 118, 129, 0.3);
        border-radius: 8px;
        color: #8b949e;
        font-size: 0.85em;
        font-weight: 500;
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
        color: #a78bfa;
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
        background: linear-gradient(90deg, #30363d, #6e7681) !important;
    }

    .stSlider [data-baseweb="slider"] {
        margin-top: 0.5em;
    }

    .stSlider [data-baseweb="slider"] [role="slider"] {
        width: 24px !important;
        height: 24px !important;
        background: #c9d1d9 !important;
        border: 3px solid #fff !important;
        box-shadow: 0 0 8px rgba(0, 0, 0, 0.3) !important;
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
        border-color: #6b8dd6 !important;
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

    /* ===== SMOOTH COMPONENT APPEARANCE ===== */
    .fade-in {
        opacity: 0;
        transform: translateY(24px);
        animation: fadeInUp 0.7s cubic-bezier(0.4,0,0.2,1) forwards;
    }
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(24px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .game-header, .main-title, .game-main, .song-info-card, .album-container, .audio-viz-container, .timer-container, .score-card, .result-container, .audio-container, .history-container, .leaderboard {
        will-change: opacity, transform;
    }
</style>
"""

# Small JS snippet to apply urgent-submit styling reliably.
# Inject into the page using `components.html(URGENT_BUTTON_SCRIPT, height=0)` from the main app.
URGENT_BUTTON_SCRIPT = """
<script>
;(function(){
    function styleUrgentButtons(){
        try{
            const buttons = document.querySelectorAll('.stButton > button[data-testid="baseButton-primary"]');
            buttons.forEach(btn => {
                if (btn.textContent && btn.textContent.includes('NOW!')) {
                    btn.classList.add('urgent-submit');
                } else {
                    btn.classList.remove('urgent-submit');
                }
            });
        }catch(e){console.warn('urgent style error',e)}
    }
    document.addEventListener('DOMContentLoaded', ()=>{
        styleUrgentButtons();
        setInterval(styleUrgentButtons, 250);
    });
    // run once immediately in case script loads after DOMContentLoaded
    styleUrgentButtons();
})();
</script>
"""

# =============================================================================
# HTML TEMPLATE FUNCTIONS
# =============================================================================


def game_header(
    player_name: str,
    round_num: int,
    start_year: int,
    end_year: int,
    total_score: int = 0,
    genre: str = "",
    genre_icon: str = "",
) -> str:
    """Generate the game header with controls"""
    genre_display = f"{genre_icon} {genre}" if genre else ""
    return f"""
    <div class="game-header fade-in">
        <div class="header-title">
            &#x1F3B5; Song Year Guesser
        </div>
        <div class="header-controls">
            <div class="header-item">
                <span class="header-item-label">Player</span>
                <span class="header-item-value">{player_name}</span>
            </div>
            <div class="header-item">
                <span class="header-item-label">Genre</span>
                <span class="header-item-value">{genre_display}</span>
            </div>
            <div class="header-item">
                <span class="header-item-label">Years</span>
                <span class="header-item-value">{start_year} - {end_year}</span>
            </div>
            <div class="header-item">
                <span class="header-item-label">Score</span>
                <span class="header-item-value">{total_score}</span>
            </div>
            <div class="header-item">
                <span class="header-item-label">Round</span>
                <span class="header-item-value">{round_num}</span>
            </div>
        </div>
    </div>
    """


def main_title() -> str:
    """Generate the main title for the welcome screen"""
    return """
    <div class="main-title fade-in">
        <h1>
            <span class="gradient-text">Song Year Guesser</span>
        </h1>
        <div class="subtitle">Test your music knowledge</div>
    </div>
    """


def song_info_card(song: dict, blur_amount: float) -> str:
    """Generate the song info card with blur effect on values only"""
    blur_css = f"filter: blur({blur_amount:.1f}px);" if blur_amount > 0 else ""
    return f"""
    <div class="song-info-card fade-in">
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
    """Generate the JavaScript scroll wheel year picker that syncs via URL query params.
    Works with mouse wheel, trackpad, drag, click, keyboard."""
    locked_style = "opacity: 0.6; pointer-events: none;" if locked else ""
    locked_border = "rgba(248, 81, 73, 0.4)" if locked else "rgba(48, 54, 61, 0.8)"
    return f"""
    <div id='year-picker-wrapper' style='display: flex; flex-direction: column; align-items: center; padding: 0.5em 0; margin-top: 0.6em; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; {locked_style}' data-locked='{str(locked).lower()}'>
        <div style='color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; font-size: 0.7em; margin-bottom: 0.6em; font-weight: 500;'>Select release year</div>
        <div id='scroll-container' style='position: relative; height: 100%; width: 260px; overflow: hidden; cursor: ns-resize; background: linear-gradient(180deg, rgba(15,23,42,1) 0%, rgba(15,23,42,0.9) 15%, transparent 35%, transparent 65%, rgba(15,23,42,0.9) 85%, rgba(15,23,42,1) 100%); border-radius: 12px; border: 1px solid {locked_border}; touch-action: none; user-select: none; -webkit-user-select: none;'>
            <div id='year-track' style='position: absolute; width: 100%; text-align: center; transition: transform 0.08s ease-out; top: 0; left: 0;'></div>
            <div style='position: absolute; top: 50%; left: 10px; right: 10px; height: 50px; transform: translateY(-50%); border: 1px solid {"rgba(248, 81, 73, 0.5)" if locked else "rgba(88, 166, 255, 0.4)"}; border-radius: 8px; pointer-events: none; background: {"rgba(248, 81, 73, 0.03)" if locked else "transparent"}; z-index: 1;'></div>
        </div>
    </div>
    <script>
    (function() {{
        const minYear = {int(start_year)};
        const maxYear = {int(end_year)};
        let currentYear = {int(current_year)};
        const isLocked = {str(locked).lower()};
        let container, track;
        let itemHeight = 46; // will be recalculated based on container height
        function buildYearTrack() {{
            track.innerHTML = '';
            for (let year = minYear; year <= maxYear; year++) {{
                const div = document.createElement('div');
                div.className = 'year-item';
                div.dataset.year = year;
                div.style.cssText = 'height: ' + itemHeight + 'px; line-height: ' + itemHeight + 'px; font-size: 2em; font-weight: 600; font-family: "SF Mono", Monaco, Consolas, monospace; color: #30363d; display: flex; align-items: center; justify-content: center; width: 100%; position: relative; z-index: 2;';
                div.textContent = year.toString();
                track.appendChild(div);
            }}
        }}
        function updatePosition() {{
            const containerHeight = 400; // fixed height for scroll wheel
            // Recalculate itemHeight in case the iframe size changed
            itemHeight = Math.max(28, Math.round(containerHeight / 5));
            const offset = (currentYear - minYear) * itemHeight;
            const centerOffset = (containerHeight / 2) - (itemHeight / 2);
            track.style.transform = 'translateY(' + (centerOffset - offset) + 'px)';
            const yearItems = track.querySelectorAll('.year-item');
            yearItems.forEach(item => {{
                const year = parseInt(item.dataset.year);
                const distance = Math.abs(year - currentYear);
                if (distance === 0) {{
                    item.style.color = isLocked ? '#f59e0b' : '#818cf8';
                    item.style.transform = 'scale(1.1)';
                    item.style.opacity = '1';
                }} else if (distance === 1) {{
                    item.style.color = '#64748b';
                    item.style.transform = 'scale(0.9)';
                    item.style.opacity = '0.6';
                }} else {{
                    item.style.color = '#30363d';
                    item.style.transform = 'scale(0.8)';
                    item.style.opacity = '0.3';
                }}
            }});
        }}
        function setYear(year) {{
            if (isLocked) return;
            const newYear = Math.max(minYear, Math.min(maxYear, Math.round(year)));
            if (newYear !== currentYear) {{
                currentYear = newYear;
                updatePosition();
                syncToUrl();
            }}
        }}
        function syncToUrl() {{
            try {{
                const url = new URL(window.parent.location.href);
                url.searchParams.set('yr', currentYear.toString());
                window.parent.history.replaceState(null, '', url.toString());
                // Update submit button text immediately for better UX
                updateSubmitButton();
            }} catch(e) {{}}
        }}
        function updateSubmitButton() {{
            try {{
                const buttons = window.parent.document.querySelectorAll('button[data-testid="baseButton-primary"]');
                buttons.forEach(btn => {{
                    if (btn.textContent.includes('Submit')) {{
                        btn.textContent = btn.textContent.includes('⏰')
                            ? '⏰ Submit ' + currentYear
                            : 'Submit ' + currentYear;
                    }}
                }});
            }} catch(e) {{}}
        }}
        function init() {{
            container = document.getElementById('scroll-container');
            track = document.getElementById('year-track');
            if (!container || !track) {{ setTimeout(init, 100); return; }}
            buildYearTrack();
            updatePosition();
            if (!isLocked) {{
                // Mouse wheel scrolling (slowed down)
                let accumulatedDelta = 0;
                const SCROLL_THRESHOLD = Math.max(24, itemHeight * 0.9); // dynamic threshold
                container.addEventListener('wheel', function(e) {{
                    e.preventDefault();
                    accumulatedDelta += e.deltaY;
                    if (Math.abs(accumulatedDelta) >= SCROLL_THRESHOLD) {{
                        const years = Math.sign(accumulatedDelta);
                        setYear(currentYear + years);
                        accumulatedDelta = 0;
                    }}
                }}, {{ passive: false }});

                // Mouse drag support
                let isDragging = false;
                let dragStartY = 0;
                let dragStartYear = currentYear;
                container.addEventListener('mousedown', function(e) {{
                    isDragging = true;
                    dragStartY = e.clientY;
                    dragStartYear = currentYear;
                    container.style.cursor = 'grabbing';
                    e.preventDefault();
                }});
                document.addEventListener('mousemove', function(e) {{
                    if (!isDragging) return;
                    const deltaY = dragStartY - e.clientY;
                    const yearDelta = Math.round(deltaY / 30); // 30px per year
                    setYear(dragStartYear + yearDelta);
                }});
                document.addEventListener('mouseup', function() {{
                    isDragging = false;
                    container.style.cursor = 'ns-resize';
                }});

                // Click on year item
                container.addEventListener('click', function(e) {{
                    if (e.target.classList.contains('year-item')) {{
                        setYear(parseInt(e.target.dataset.year));
                    }}
                }});

                // Arrow key support
                container.setAttribute('tabindex', '0');
                container.addEventListener('keydown', function(e) {{
                    if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {{
                        e.preventDefault();
                        setYear(currentYear - 1);
                    }} else if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {{
                        e.preventDefault();
                        setYear(currentYear + 1);
                    }}
                }});
                // Focus container for keyboard input
                container.focus();
                // Ensure initial sizing and rendering
                updatePosition();
            }}
        }}
        setTimeout(init, 0);
    }})();
    </script>
"""


def timer_html(start_timestamp: float, max_time: int, delay_seconds: int = 0) -> str:
    """Generate the countdown timer with dynamic animations that intensify as time runs out"""
    return f"""
    <style>
        body {{ margin: 0; padding: 0; background: transparent; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
        .timer-container {{ display: flex; justify-content: center; align-items: center; width: 100%; height: 100%; }}
        .timer-ring {{
            position: relative;
            width: 190px;
            height: 190px;
            transition: opacity 0.3s ease;
        }}
        .timer-ring.paused {{ opacity: 0.5; }}
        .timer-ring.warning {{
            animation: warningPulse 1s ease-in-out infinite;
        }}
        .timer-ring.danger {{
            animation: dangerPulse 0.6s ease-in-out infinite;
        }}
        .timer-ring.critical {{
            animation: criticalPulse 0.4s ease-in-out infinite;
        }}
        .timer-text {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; }}
        .timer-seconds {{
            font-size: 3.8em;
            font-weight: 800;
            line-height: 1;
            transition: color 0.2s ease, transform 0.15s ease;
            font-family: 'SF Mono', Monaco, Consolas, monospace;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }}
        .timer-seconds.pulse {{ animation: numberPulse 0.4s ease-out; }}
        .timer-label {{
            font-size: 0.85em;
            color: #6e7681;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-top: 0.4em;
            transition: color 0.2s ease;
            font-weight: 600;
        }}
        .timer-label.paused {{ color: #8b949e; }}
        .timer-label.urgent {{ color: #ef4444; font-weight: 700; }}
        @keyframes warningPulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.02); }}
        }}
        @keyframes dangerPulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.04); }}
        }}
        @keyframes criticalPulse {{
            0%, 100% {{ transform: scale(1) rotate(0deg); }}
            25% {{ transform: scale(1.05) rotate(-1deg); }}
            75% {{ transform: scale(1.05) rotate(1deg); }}
        }}
        @keyframes numberPulse {{
            0% {{ transform: scale(1); }}
            40% {{ transform: scale(1.15); }}
            100% {{ transform: scale(1); }}
        }}
    </style>
    <div class="timer-container">
        <div class="timer-ring" id="timer-ring">
            <svg width="190" height="190" viewBox="0 0 190 190" style="transform: rotate(-90deg);">
                <defs>
                    <linearGradient id="timerGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#818cf8;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#0ea5e9;stop-opacity:1" />
                    </linearGradient>
                </defs>
                <circle cx="95" cy="95" r="80" fill="none" stroke="#21262d" stroke-width="10"/>
                <circle id="timer-bg" cx="95" cy="95" r="80" fill="none" stroke="#30363d" stroke-width="10" opacity="0.3"/>
                <circle id="timer-circle" cx="95" cy="95" r="80" fill="none" stroke="url(#timerGradient)" stroke-width="10"
                    stroke-linecap="round" stroke-dasharray="502.65" stroke-dashoffset="0"
                    style="transition: stroke-dashoffset 0.1s linear, stroke 0.2s ease;"/>
            </svg>
            <div class="timer-text">
                <div id="timer-seconds" class="timer-seconds" style="color: #c9d1d9;">{max_time}</div>
                <div id="timer-label" class="timer-label">seconds</div>
            </div>
        </div>
    </div>
    <script>
        (function() {{
            var startTime = {start_timestamp};
            var maxTime = {max_time};
            var delaySeconds = {delay_seconds};
            var circle = document.getElementById('timer-circle');
            var secondsEl = document.getElementById('timer-seconds');
            var ring = document.getElementById('timer-ring');
            var labelEl = document.getElementById('timer-label');
            var circumference = 2 * Math.PI * 80;
            var lastSecond = maxTime;

            // Pause tracking
            var isPaused = false;
            var pausedAt = null;
            var accumulatedPausedTime = 0;

            function pause() {{
                // Don't allow pausing if time has already elapsed
                var elapsed = getElapsedTime();
                if (elapsed >= maxTime) return;

                if (!isPaused) {{
                    isPaused = true;
                    pausedAt = Date.now();
                    ring.classList.add('paused');
                    ring.classList.remove('warning', 'danger', 'critical');
                    labelEl.textContent = 'paused';
                    labelEl.classList.add('paused');
                }}
            }}

            function resume() {{
                if (isPaused && pausedAt !== null) {{
                    accumulatedPausedTime += (Date.now() - pausedAt);
                    isPaused = false;
                    pausedAt = null;
                    ring.classList.remove('paused');
                    labelEl.textContent = 'seconds';
                    labelEl.classList.remove('paused');
                }}
            }}

            function getElapsedTime() {{
                var now = Date.now();
                var totalPausedTime = accumulatedPausedTime;
                if (isPaused && pausedAt !== null) {{
                    totalPausedTime += (now - pausedAt);
                }}
                var elapsed = ((now - startTime) - totalPausedTime) / 1000 - delaySeconds;
                return elapsed;
            }}

            function lerpColor(color1, color2, t) {{
                var r1 = parseInt(color1.slice(1,3), 16);
                var g1 = parseInt(color1.slice(3,5), 16);
                var b1 = parseInt(color1.slice(5,7), 16);
                var r2 = parseInt(color2.slice(1,3), 16);
                var g2 = parseInt(color2.slice(3,5), 16);
                var b2 = parseInt(color2.slice(5,7), 16);
                var r = Math.round(r1 + (r2 - r1) * t);
                var g = Math.round(g1 + (g2 - g1) * t);
                var b = Math.round(b1 + (b2 - b1) * t);
                return '#' + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
            }}

            function getProgressColor(progress) {{
                // Gray (#8b949e) -> Gray (#6e7681) -> Orange (#9e6a03) -> Red (#da3633)
                if (progress < 0.5) {{
                    return lerpColor('#8b949e', '#6e7681', progress * 2);
                }} else if (progress < 0.75) {{
                    return lerpColor('#6e7681', '#9e6a03', (progress - 0.5) * 4);
                }} else {{
                    return lerpColor('#9e6a03', '#da3633', (progress - 0.75) * 4);
                }}
            }}

            function updateTimer() {{
                var elapsed = getElapsedTime();

                if (elapsed < 0) {{
                    secondsEl.textContent = maxTime;
                    circle.style.strokeDashoffset = 0;
                    circle.style.stroke = '#8b949e';
                    secondsEl.style.color = '#c9d1d9';
                    ring.classList.remove('warning', 'danger', 'critical');
                    secondsEl.classList.remove('glow-effect');
                    labelEl.textContent = 'seconds';
                    labelEl.classList.remove('paused', 'urgent');
                    return;
                }}

                if (elapsed > maxTime) elapsed = maxTime;

                var remaining = Math.ceil(maxTime - elapsed);
                var progress = elapsed / maxTime;
                var offset = circumference * progress;

                circle.style.strokeDashoffset = offset;

                // Pulse animation on second change
                if (remaining !== lastSecond && remaining > 0) {{
                    secondsEl.classList.remove('pulse');
                    void secondsEl.offsetWidth; // Trigger reflow
                    secondsEl.classList.add('pulse');
                    lastSecond = remaining;
                }}

                secondsEl.textContent = remaining;

                var color = getProgressColor(progress);
                circle.style.stroke = color;
                secondsEl.style.color = color;

                // Progressive animation states
                ring.classList.remove('warning', 'danger', 'critical');
                secondsEl.classList.remove('glow-effect');
                labelEl.classList.remove('urgent');

                if (remaining <= 3 && remaining > 0) {{
                    ring.classList.add('critical');
                    secondsEl.classList.add('glow-effect');
                    labelEl.classList.add('urgent');
                }} else if (remaining <= 5) {{
                    ring.classList.add('danger');
                    secondsEl.classList.add('glow-effect');
                }} else if (remaining <= 10) {{
                    ring.classList.add('warning');
                }}

                if (remaining <= 0 && !isPaused) {{
                    labelEl.textContent = "TIME'S UP";
                    labelEl.classList.add('urgent');
                    ring.classList.remove('warning', 'danger', 'critical');
                    // No animation when time is up - just a steady display
                }} else if (!isPaused) {{
                    labelEl.textContent = remaining <= 5 ? 'hurry!' : 'seconds';
                }}

                try {{
                    var url = new URL(window.parent.location.href);
                    url.searchParams.set('et', elapsed.toFixed(1));
                    window.parent.history.replaceState(null, '', url.toString());
                }} catch(e) {{}}
            }}

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
    """Generate a static timer display - no glow effects"""
    return f"""
    <div style="display: flex; justify-content: center; align-items: center; width: 100%; height: 200px;">
        <div style="position: relative; width: 200px; height: 200px;">
            <svg width="200" height="200" viewBox="0 0 200 200" style="transform: rotate(-90deg);">
                <circle cx="100" cy="100" r="90" fill="none" stroke="#1e1e3f" stroke-width="10"/>
                <circle cx="100" cy="100" r="90" fill="none" stroke="#818cf8" stroke-width="10" stroke-dasharray="565" stroke-linecap="round"/>
            </svg>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                <div style="font-size: 4em; font-weight: 800; color: #818cf8; line-height: 1;">{seconds}</div>
                <div style="font-size: 0.9em; color: #888; text-transform: uppercase; letter-spacing: 2px; margin-top: 0.3em;">sec</div>
            </div>
        </div>
    </div>
    """


def get_selected_year_js() -> str:
    """Component that reads selected year from localStorage and returns it"""
    return """
    <script>
        (function() {
            function sendYear() {
                try {
                    var year = localStorage.getItem('selectedYear');
                    if (year) {
                        window.parent.postMessage({
                            type: 'streamlit:setComponentValue',
                            value: parseInt(year)
                        }, '*');
                    }
                } catch(e) {}
            }
            // Send immediately and periodically
            sendYear();
            setInterval(sendYear, 200);
        })();
    </script>
    """


def year_scroll_wheel(
    min_year: int, max_year: int, initial_year: int, disabled: bool = False
) -> str:
    """Generate a scroll wheel picker for year selection"""
    disabled_class = "disabled" if disabled else ""
    disabled_attr = "true" if disabled else "false"
    return f"""
    <style>
        .wheel-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            height: 300px;
            position: relative;
            overflow: hidden;
            user-select: none;
        }}
        .wheel-container.disabled {{
            opacity: 0.5;
            pointer-events: none;
        }}
        .wheel {{
            position: relative;
            height: 300px;
            width: 140px;
            overflow: hidden;
            -webkit-mask-image: linear-gradient(to bottom, transparent 0%, black 25%, black 75%, transparent 100%);
            mask-image: linear-gradient(to bottom, transparent 0%, black 25%, black 75%, transparent 100%);
        }}
        .wheel-inner {{
            transition: transform 0.1s ease-out;
        }}
        .wheel-item {{
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.2em;
            font-weight: 700;
            color: #666;
            transition: all 0.15s ease;
            cursor: pointer;
        }}
        .wheel-item.selected {{
            color: #a78bfa;
            font-size: 2.8em;
            text-shadow: 0 0 20px rgba(34, 211, 238, 0.5);
        }}
        .wheel-item:hover:not(.selected) {{
            color: #888;
        }}
        .wheel-highlight {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 130px;
            height: 60px;
            border-top: 2px solid rgba(34, 211, 238, 0.4);
            border-bottom: 2px solid rgba(34, 211, 238, 0.4);
            pointer-events: none;
            border-radius: 8px;
            background: rgba(34, 211, 238, 0.05);
        }}
        .wheel-container.disabled .wheel-highlight {{
            border-color: rgba(239, 68, 68, 0.4);
            background: rgba(239, 68, 68, 0.05);
        }}
        .wheel-container.disabled .wheel-item.selected {{
            color: #ef4444;
            text-shadow: none;
        }}
    </style>
    <div class="wheel-container {disabled_class}" id="wheel-container">
        <div class="wheel" id="wheel">
            <div class="wheel-inner" id="wheel-inner"></div>
        </div>
        <div class="wheel-highlight"></div>
    </div>
    <script>
        (function() {{
            var minYear = {min_year};
            var maxYear = {max_year};
            var currentYear = {initial_year};
            var disabled = {disabled_attr};
            var itemHeight = 60;
            var container = document.getElementById('wheel-container');
            var wheel = document.getElementById('wheel');
            var inner = document.getElementById('wheel-inner');

            // Build year items
            var years = [];
            for (var y = minYear; y <= maxYear; y++) {{
                years.push(y);
            }}

            // Create DOM elements
            inner.innerHTML = '';
            years.forEach(function(year, idx) {{
                var item = document.createElement('div');
                item.className = 'wheel-item';
                item.textContent = year;
                item.dataset.year = year;
                item.dataset.index = idx;
                if (year === currentYear) {{
                    item.classList.add('selected');
                }}
                inner.appendChild(item);
            }});

            // Position to show current year in center
            var currentIndex = years.indexOf(currentYear);
            if (currentIndex === -1) currentIndex = Math.floor(years.length / 2);

            // Center the wheel (account for 5 visible items, center is index 2)
            var offset = -(currentIndex * itemHeight) + (2 * itemHeight);
            inner.style.transform = 'translateY(' + offset + 'px)';

            function selectYear(year) {{
                if (disabled) return;
                currentYear = year;
                var idx = years.indexOf(year);
                var offset = -(idx * itemHeight) + (2 * itemHeight);
                inner.style.transform = 'translateY(' + offset + 'px)';

                // Update selected class
                var items = inner.querySelectorAll('.wheel-item');
                items.forEach(function(item) {{
                    item.classList.toggle('selected', parseInt(item.dataset.year) === year);
                }});

                // Send to Streamlit
                try {{
                    localStorage.setItem('selectedYear', year.toString());
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        value: year
                    }}, '*');
                }} catch(e) {{}}
            }}

            // Click handler
            inner.addEventListener('click', function(e) {{
                if (disabled) return;
                var item = e.target.closest('.wheel-item');
                if (item) {{
                    selectYear(parseInt(item.dataset.year));
                }}
            }});

            // Wheel scroll handler
            var scrollTimeout = null;
            wheel.addEventListener('wheel', function(e) {{
                if (disabled) return;
                e.preventDefault();

                var delta = e.deltaY > 0 ? 1 : -1;
                var idx = years.indexOf(currentYear);
                var newIdx = Math.max(0, Math.min(years.length - 1, idx + delta));

                if (newIdx !== idx) {{
                    selectYear(years[newIdx]);
                }}
            }}, {{ passive: false }});

            // Touch/drag support
            var touchStartY = 0;
            var touchMoveY = 0;
            var isDragging = false;

            wheel.addEventListener('touchstart', function(e) {{
                if (disabled) return;
                touchStartY = e.touches[0].clientY;
                isDragging = true;
            }});

            wheel.addEventListener('touchmove', function(e) {{
                if (disabled || !isDragging) return;
                e.preventDefault();
                touchMoveY = e.touches[0].clientY;
                var diff = touchStartY - touchMoveY;

                if (Math.abs(diff) > 30) {{
                    var delta = diff > 0 ? 1 : -1;
                    var idx = years.indexOf(currentYear);
                    var newIdx = Math.max(0, Math.min(years.length - 1, idx + delta));
                    if (newIdx !== idx) {{
                        selectYear(years[newIdx]);
                    }}
                    touchStartY = touchMoveY;
                }}
            }}, {{ passive: false }});

            wheel.addEventListener('touchend', function() {{
                isDragging = false;
            }});

            // Mouse drag support
            wheel.addEventListener('mousedown', function(e) {{
                if (disabled) return;
                touchStartY = e.clientY;
                isDragging = true;
            }});

            document.addEventListener('mousemove', function(e) {{
                if (disabled || !isDragging) return;
                touchMoveY = e.clientY;
                var diff = touchStartY - touchMoveY;

                if (Math.abs(diff) > 20) {{
                    var delta = diff > 0 ? 1 : -1;
                    var idx = years.indexOf(currentYear);
                    var newIdx = Math.max(0, Math.min(years.length - 1, idx + delta));
                    if (newIdx !== idx) {{
                        selectYear(years[newIdx]);
                    }}
                    touchStartY = touchMoveY;
                }}
            }});

            document.addEventListener('mouseup', function() {{
                isDragging = false;
            }});

            // Expose for external access
            window.yearWheel = {{
                getYear: function() {{ return currentYear; }},
                setYear: selectYear
            }};

            // Send initial value to Streamlit and localStorage
            function sendCurrentYear() {{
                try {{
                    localStorage.setItem('selectedYear', currentYear.toString());
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        value: currentYear
                    }}, '*');
                }} catch(e) {{}}
            }}

            // Send immediately and keep sending periodically to ensure sync
            sendCurrentYear();
            setInterval(sendCurrentYear, 300);
        }})();
    </script>
"""


def result_display(emoji: str, message: str, subtitle: str, color: str) -> str:
    """Generate the result message display"""
    return f"""

    <div class="result-container fade-in">
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

    if diff == 0:
        diff_text = '<span style="color: #00ff88;">Perfect match!</span>'
    elif diff > 0:
        diff_text = f'<span style="color: #ef4444;">+{diff} years (too recent)</span>'
    else:
        diff_text = f'<span style="color: #3b82f6;">{diff} years (too early)</span>'

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
    """Generate the score card display - compact single line"""
    # Wrap the text in a no-wrap span so the message always stays on one line
    return (
        f'<div class="score-card">'
        f'<span style="font-size: 1.2em;">&#x1F3AF;</span> '
        f'<span style="white-space:nowrap;">You earned <strong>{score} points</strong> this round</span>'
        f"</div>"
    )


def status_line(message: str) -> str:
    """Generate a status message line"""
    return f'<div class="status-line">{message}</div>'


def spotify_button(url: str) -> str:
    """Generate a Spotify listen button"""
    return f"""
    <div class="listen-btn-container">
        <a href="{url}" target="_blank" class="listen-btn spotify-btn">
            <svg class="spotify-icon" width="20" height="20" viewBox="0 0 24 24" fill="#1DB954">
                <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.021-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
            </svg>
            Listen on Spotify
        </a>
    </div>
    """


def how_to_play() -> str:
    """Generate the how to play section"""
    return """
    <div class="how-to-play" style="font-size:1.02em; margin: 0.6em auto 1.2em auto; color:#cbd5ff; max-width: 720px; width: min(92vw, 720px);">
        <h3 style="margin:0 0 0.4em 0; color:#e6edf3; font-weight:700;">How to Play</h3>
        <ol style="text-align: left; margin: 0 1em 0 1.2em; padding-left: 1.1em; line-height: 1.5; color:#cbd5ff;">
            <li>Listen to the 30‑second preview and recall the song's release year.</li>
            <li>Use the scroll wheel, drag, or arrow keys to select the year.</li>
            <li>Submit your guess before the timer runs out.</li>
            <li>Play multiple rounds to earn points and climb the leaderboard.</li>
        </ol>
            <div class="how-to-play-tip" style="margin-top:0.6em;">Tip: Guess early for a speed bonus!</div>
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
                <strong style="color: #c9d1d9;">{score["player"]}</strong>
            </div>
            <div style="font-size: 1.2em; font-weight: 700; color: #58a6ff;">{score["total_score"]} pts</div>
        </div>
        <div style="font-size: 0.85em; color: #8b949e; margin-top: 0.3em;">
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
                    // Directly set localStorage with song-specific key
                    localStorage.setItem('autoplayBlocked_{song_id}', blocked ? 'true' : 'false');
                }} catch(e) {{
                    console.log('Could not set autoplay status:', e);
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

                // Signal to Streamlit that audio has started
                try {{
                    localStorage.setItem('audio_started_{song_id}', 'true');
                }} catch(e) {{
                    console.log('Could not signal audio start:', e);
                }}
            }});
            audio.addEventListener('pause', function() {{
                // Only pause timer if audio was manually paused (not ended)
                if (!audio.ended) {{
                    updateViz(false);
                    updateTimer(false);
                }}
            }});
            audio.addEventListener('ended', function() {{
                // Audio ended naturally - stop visualizer but DON'T pause timer
                updateViz(false);
                // Timer continues running - user must submit before time runs out
            }});

            {'audio.volume = 1.0; audio.play().then(function() { notifyAutoplayStatus(false); }).catch(function(e) { console.log("Autoplay prevented:", e); notifyAutoplayStatus(true); });' if autoplay else ""}
        }})();
    </script>
"""


def leaderboard_header() -> str:
    """Generate the leaderboard header"""
    return '<div class="leaderboard-header">Leaderboard</div>'


def empty_leaderboard() -> str:
    """Generate empty leaderboard message"""
    return '<div style="text-align: center; color: #6e7681; padding: 1.5em; font-size: 0.9em;">No scores yet. Play a game to see your scores here.</div>'


def elapsed_time_receiver() -> str:
    """Component that receives elapsed time from timer and stores in localStorage"""
    return """
    <script>
        (function() {
            var lastElapsed = 0;

            window.addEventListener('message', function(event) {
                try {
                    if (event.data && event.data.type === 'timer:elapsed') {
                        lastElapsed = event.data.elapsed;
                        try { localStorage.setItem('gameTimerElapsed', lastElapsed.toString()); } catch(e) {}
                    } else if (event.data && event.data.type === 'year:selected') {
                        try { localStorage.setItem('gameSelectedYear', event.data.year.toString()); } catch(e) {}
                        // Show overlay label instantly
                        try {
                            const yearStr = event.data.year.toString();
                            function attachOverlay() {
                                const btn = document.querySelector('button[data-testid="baseButton-primary"]');
                                if (!btn) return;
                                let overlay = document.getElementById('submit-year-overlay');
                                if (!overlay) {
                                    overlay = document.createElement('div');
                                    overlay.id = 'submit-year-overlay';
                                    overlay.style.position = 'absolute';
                                    overlay.style.pointerEvents = 'none';
                                    overlay.style.zIndex = 9999;
                                    overlay.style.display = 'flex';
                                    overlay.style.alignItems = 'center';
                                    overlay.style.justifyContent = 'center';
                                    overlay.style.color = 'white';
                                    overlay.style.fontWeight = '800';
                                    overlay.style.fontFamily = "'SF Mono', Monaco, Consolas, monospace";
                                    document.body.appendChild(overlay);
                                }
                                const rect = btn.getBoundingClientRect();
                                overlay.style.left = (rect.left + window.scrollX) + 'px';
                                overlay.style.top = (rect.top + window.scrollY) + 'px';
                                overlay.style.width = rect.width + 'px';
                                overlay.style.height = rect.height + 'px';
                                overlay.style.fontSize = Math.max(16, Math.min(28, rect.height * 0.45)) + 'px';
                                overlay.style.borderRadius = window.getComputedStyle(btn).borderRadius || '8px';
                                overlay.style.boxSizing = 'border-box';
                                overlay.textContent = yearStr;
                            }
                            attachOverlay();
                        } catch(e) {}
                    } else if (event.data && event.data.type === 'urgent:click') {
                        try {
                            const btn = document.querySelector('button[key="submit_guess_urgent"]') || document.querySelector('button[data-testid="baseButton-primary"]');
                            if (btn && typeof btn.click === 'function') btn.click();
                        } catch(e) {}
                    }
                } catch(e) {}
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


def settings_row() -> str:
    """Generate opening div for compact settings row"""
    return '<div class="compact-settings">'
