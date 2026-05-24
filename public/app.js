const app = document.querySelector("#app");

const LOCAL_LEADERBOARD_KEY = "song-year-guesser-leaderboard";
const MAX_LEADERBOARD_ENTRIES = 20;

let maxGuessTime = 30;
let hintRevealTime = 25;

let genreConfig = {
  "All Genres": { query: "", bestYears: [1995, 2020], icon: "🎵" },
  Pop: { query: "pop", bestYears: [1985, 2000], icon: "🎤" },
  Rock: { query: "rock", bestYears: [1968, 1985], icon: "🎸" },
  "Hip-Hop": { query: "hip hop rap", bestYears: [1994, 2009], icon: "🎧" },
  "R&B": { query: "r&b soul", bestYears: [1990, 2005], icon: "💜" },
  Electronic: { query: "electronic dance edm", bestYears: [1998, 2013], icon: "🎹" },
  Country: { query: "country", bestYears: [1990, 2005], icon: "🤠" },
  Alternative: { query: "alternative indie", bestYears: [1991, 2006], icon: "🎪" },
  Metal: { query: "metal heavy", bestYears: [1983, 1998], icon: "🤘" },
  "Disco/Funk": { query: "disco funk", bestYears: [1975, 1985], icon: "🕺" },
  "80s": { query: "80s hits", bestYears: [1980, 1989], icon: "📼" }
};

let genreList = Object.keys(genreConfig);

const state = {
  gameActive: false,
  currentSong: null,
  currentRound: 0,
  playerScores: [],
  currentPlayer: "Player 1",
  selectedGenre: "All Genres",
  startYear: 1995,
  endYear: 2020,
  playedSongIds: new Set(),
  playedSongKeys: new Set(),
  currentGuess: 2000,
  gameOver: false,
  timedOut: false,
  timeLocked: false,
  audioStarted: false,
  timerStartedAt: 0,
  timerPausedAt: 0,
  timerPausedMs: 0,
  timerPaused: true,
  timerInterval: null,
  revealInterval: null,
  leaderboard: [],
  leaderboardPersistent: false,
  statusMessage: ""
};

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttr(value) {
  return escapeHtml(value).replaceAll("`", "&#096;");
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function calculateScore(guess, actual, timeTaken) {
  const yearDiff = Math.abs(Number(guess) - Number(actual));
  let accuracyScore;

  if (yearDiff === 0) {
    accuracyScore = 1000;
  } else if (yearDiff === 1) {
    accuracyScore = 800;
  } else if (yearDiff === 2) {
    accuracyScore = 600;
  } else if (yearDiff <= 3) {
    accuracyScore = 400;
  } else if (yearDiff <= 5) {
    accuracyScore = 200;
  } else {
    accuracyScore = Math.max(0, 100 - yearDiff * 10);
  }

  const timeBonus = Math.max(0, 300 - Number(timeTaken) * 10);
  return Math.trunc(Math.max(0, accuracyScore + timeBonus));
}

function totalScore() {
  return state.playerScores
    .filter((score) => score.player === state.currentPlayer)
    .reduce((sum, score) => sum + score.score, 0);
}

function songsPlayed() {
  return state.playerScores.filter((score) => score.player === state.currentPlayer).length;
}

async function apiJson(path, options = {}) {
  const response = await fetch(path, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers ?? {})
    },
    ...options
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error || `Request failed with ${response.status}`);
  }
  return data;
}

function clearTimers() {
  if (state.timerInterval) {
    clearInterval(state.timerInterval);
    state.timerInterval = null;
  }
  if (state.revealInterval) {
    clearInterval(state.revealInterval);
    state.revealInterval = null;
  }
}

function resetRoundTimer() {
  state.audioStarted = false;
  state.timerStartedAt = 0;
  state.timerPausedAt = performance.now();
  state.timerPausedMs = 0;
  state.timerPaused = true;
  state.timeLocked = false;
}

function currentElapsedSeconds() {
  if (!state.audioStarted || !state.timerStartedAt) {
    return 0;
  }
  const now = performance.now();
  const activePausedMs = state.timerPaused ? now - state.timerPausedAt : 0;
  const elapsedMs = now - state.timerStartedAt - state.timerPausedMs - activePausedMs;
  return Math.max(0, elapsedMs / 1000);
}

function timerColor(progress) {
  if (progress < 0.5) {
    return mixColor("#8b949e", "#6e7681", progress * 2);
  }
  if (progress < 0.75) {
    return mixColor("#6e7681", "#9e6a03", (progress - 0.5) * 4);
  }
  return mixColor("#9e6a03", "#da3633", (progress - 0.75) * 4);
}

function mixColor(colorA, colorB, amount) {
  const a = colorA.match(/[0-9a-f]{2}/gi).map((part) => Number.parseInt(part, 16));
  const b = colorB.match(/[0-9a-f]{2}/gi).map((part) => Number.parseInt(part, 16));
  const mixed = a.map((channel, index) =>
    Math.round(channel + (b[index] - channel) * amount)
      .toString(16)
      .padStart(2, "0")
  );
  return `#${mixed.join("")}`;
}

function getLocalLeaderboard() {
  try {
    const parsed = JSON.parse(localStorage.getItem(LOCAL_LEADERBOARD_KEY) || "[]");
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function setLocalLeaderboard(entries) {
  const sorted = [...entries]
    .sort((a, b) => Number(b.total_score ?? 0) - Number(a.total_score ?? 0))
    .slice(0, MAX_LEADERBOARD_ENTRIES);
  localStorage.setItem(LOCAL_LEADERBOARD_KEY, JSON.stringify(sorted));
}

function makeLocalLeaderboardEntry() {
  const total = totalScore();
  const count = songsPlayed();
  const formatter = new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "2-digit",
    timeZone: "Australia/Sydney"
  });

  return {
    player: state.currentPlayer,
    total_score: total,
    songs_played: count,
    avg_score: count > 0 ? Math.round(total / count) : 0,
    genre: state.selectedGenre,
    date: formatter.format(new Date())
  };
}

async function loadLeaderboard() {
  try {
    const result = await apiJson("/api/leaderboard");
    state.leaderboardPersistent = Boolean(result.persistent);
    state.leaderboard = state.leaderboardPersistent ? result.entries ?? [] : getLocalLeaderboard();
  } catch {
    state.leaderboardPersistent = false;
    state.leaderboard = getLocalLeaderboard();
  }
}

async function loadConfig() {
  try {
    const config = await apiJson("/api/config");
    genreConfig = config.genreConfig ?? genreConfig;
    genreList = config.genres ?? Object.keys(genreConfig);
    maxGuessTime = Number(config.maxGuessTime ?? maxGuessTime);
    hintRevealTime = Number(config.hintRevealTime ?? hintRevealTime);
  } catch {
    genreList = Object.keys(genreConfig);
  }
}

function renderHeader() {
  const genre = genreConfig[state.selectedGenre] ?? genreConfig["All Genres"];
  return `
    <div class="game-header fade-in">
      <div class="header-title">🎵 Song Year Guesser</div>
      <div class="header-controls">
        <div class="header-item">
          <span class="header-item-label">Player</span>
          <span class="header-item-value">${escapeHtml(state.currentPlayer)}</span>
        </div>
        <div class="header-item">
          <span class="header-item-label">Genre</span>
          <span class="header-item-value">${escapeHtml(genre.icon)} ${escapeHtml(state.selectedGenre)}</span>
        </div>
        <div class="header-item">
          <span class="header-item-label">Years</span>
          <span class="header-item-value">${state.startYear} - ${state.endYear}</span>
        </div>
        <div class="header-item">
          <span class="header-item-label">Score</span>
          <span class="header-item-value">${totalScore()}</span>
        </div>
        <div class="header-item">
          <span class="header-item-label">Round</span>
          <span class="header-item-value">${state.currentRound}</span>
        </div>
      </div>
    </div>
  `;
}

function mainTitle() {
  return `
    <section class="main-title fade-in">
      <h1><span class="gradient-text">Song Year Guesser</span></h1>
      <div class="subtitle">Test your music knowledge</div>
    </section>
  `;
}

function howToPlay() {
  return `
    <section class="how-to-play fade-in">
      <h2>How to Play</h2>
      <ol>
        <li>Listen to the 30-second preview and recall the song's release year.</li>
        <li>Use the scroll wheel, drag, or arrow keys to select the year.</li>
        <li>Submit your guess before the timer runs out.</li>
        <li>Play multiple rounds to earn points and climb the leaderboard.</li>
      </ol>
      <div class="how-to-play-tip">Tip: Guess early for a speed bonus!</div>
    </section>
  `;
}

function settingsPanel() {
  const genreOptions = genreList
    .map((name) => {
      const genre = genreConfig[name];
      return `<option value="${escapeAttr(name)}" ${name === state.selectedGenre ? "selected" : ""}>${escapeHtml(genre.icon)} ${escapeHtml(name)}</option>`;
    })
    .join("");

  const currentYear = new Date().getFullYear();
  const genre = genreConfig[state.selectedGenre];

  return `
    <section class="settings-panel fade-in">
      <div class="settings-grid">
        <div class="field">
          <label for="genre-select">Genre</label>
          <select id="genre-select" data-testid="genre-select">${genreOptions}</select>
        </div>
        <div class="field">
          <label for="player-name">Player Name</label>
          <input id="player-name" data-testid="player-name" value="${escapeAttr(state.currentPlayer)}" maxlength="15" placeholder="Enter your name" />
        </div>
      </div>
      <div class="range-panel">
        <div class="range-caption">Year Range</div>
        <div class="range-line">
          <input class="year-number" id="start-year-number" data-testid="start-year" type="number" min="1960" max="${currentYear}" value="${state.startYear}" />
          <div class="range-sliders">
            <input id="start-year-range" type="range" min="1960" max="${currentYear}" value="${state.startYear}" />
            <input id="end-year-range" type="range" min="1960" max="${currentYear}" value="${state.endYear}" />
          </div>
          <input class="year-number" id="end-year-number" data-testid="end-year" type="number" min="1960" max="${currentYear}" value="${state.endYear}" />
        </div>
        <div class="selected-range" data-testid="selected-range">${escapeHtml(genre.icon)} ${escapeHtml(state.selectedGenre)} • ${state.startYear} - ${state.endYear}</div>
      </div>
    </section>
  `;
}

function leaderboardHtml() {
  if (!state.leaderboard.length) {
    return `<div class="empty-leaderboard" data-testid="empty-leaderboard">No scores yet. Play a game to see your scores here.</div>`;
  }

  const entries = [...state.leaderboard]
    .sort((a, b) => Number(b.total_score ?? 0) - Number(a.total_score ?? 0))
    .slice(0, 10);

  const entryHtml = entries
    .map((entry, index) => {
      const rank = index + 1;
      const medal = rank === 1 ? "🥇" : rank === 2 ? "🥈" : rank === 3 ? "🥉" : `#${rank}`;
      return `
        <article class="leaderboard-entry" data-testid="leaderboard-entry">
          <div class="leaderboard-top">
            <div class="leaderboard-player"><span>${medal}</span><span>${escapeHtml(entry.player)}</span></div>
            <div class="leaderboard-score">${Number(entry.total_score ?? 0)} pts</div>
          </div>
          <div class="leaderboard-meta">
            ${escapeHtml(entry.genre ?? "All Genres")} • ${Number(entry.songs_played ?? 0)} songs • Avg: ${Number(entry.avg_score ?? 0)} pts • ${escapeHtml(entry.date ?? "")}
          </div>
        </article>
      `;
    })
    .join("");

  return `
    <section class="leaderboard-list">
      <div class="leaderboard-header">Leaderboard</div>
      ${entryHtml}
    </section>
  `;
}

function renderWelcome() {
  clearTimers();
  state.gameActive = false;
  const statusClass = state.statusMessage.startsWith("Could not") || state.statusMessage.startsWith("Spotify")
    ? " error"
    : "";

  app.innerHTML = `
    ${mainTitle()}
    ${settingsPanel()}
    ${state.statusMessage ? `<div class="status-line${statusClass}" data-testid="status-line">${escapeHtml(state.statusMessage)}</div>` : ""}
    ${howToPlay()}
    <div class="welcome-actions">
      <button class="primary-button" id="start-game" data-testid="start-game">🎵 Start New Game</button>
    </div>
    ${leaderboardHtml()}
  `;

  document.querySelector("#start-game").addEventListener("click", startGame);
  attachSettingsEvents();
}

function attachSettingsEvents() {
  const genreSelect = document.querySelector("#genre-select");
  const playerInput = document.querySelector("#player-name");
  const startNumber = document.querySelector("#start-year-number");
  const endNumber = document.querySelector("#end-year-number");
  const startRange = document.querySelector("#start-year-range");
  const endRange = document.querySelector("#end-year-range");

  genreSelect.addEventListener("change", () => {
    state.selectedGenre = genreSelect.value;
    const [startYear, endYear] = genreConfig[state.selectedGenre].bestYears;
    state.startYear = startYear;
    state.endYear = endYear;
    renderWelcome();
  });

  playerInput.addEventListener("input", () => {
    state.currentPlayer = playerInput.value.slice(0, 15);
  });

  function syncYears(source) {
    const currentYear = new Date().getFullYear();
    const startValue = Number(source === "startRange" ? startRange.value : startNumber.value);
    const endValue = Number(source === "endRange" ? endRange.value : endNumber.value);

    if (source.startsWith("start")) {
      state.startYear = clamp(startValue, 1960, state.endYear);
    } else {
      state.endYear = clamp(endValue, state.startYear, currentYear);
    }

    startNumber.value = state.startYear;
    startRange.value = state.startYear;
    endNumber.value = state.endYear;
    endRange.value = state.endYear;

    const rangeLabel = document.querySelector("[data-testid='selected-range']");
    const genre = genreConfig[state.selectedGenre];
    rangeLabel.textContent = `${genre.icon} ${state.selectedGenre} • ${state.startYear} - ${state.endYear}`;
  }

  startNumber.addEventListener("change", () => syncYears("startNumber"));
  startRange.addEventListener("input", () => syncYears("startRange"));
  endNumber.addEventListener("change", () => syncYears("endNumber"));
  endRange.addEventListener("input", () => syncYears("endRange"));
}

function audioVisualizerHtml(isPlaying = false) {
  return `
    <div class="audio-viz-container ${isPlaying ? "" : "audio-viz-static"}" id="audio-viz">
      ${Array.from({ length: 20 }, () => `<div class="audio-viz-bar"></div>`).join("")}
    </div>
  `;
}

function songInfoCard(song, blurAmount) {
  const blurStyle = blurAmount > 0 ? `style="filter: blur(${blurAmount.toFixed(1)}px)"` : "";
  return `
    <section class="song-info-card fade-in">
      <div class="song-info-item">
        <span class="song-info-icon">🎵</span>
        <span class="song-info-label">Song</span>
        <span class="song-info-value reveal-text" ${blurStyle}>${escapeHtml(song.name)}</span>
      </div>
      <div class="song-info-item">
        <span class="song-info-icon">🎤</span>
        <span class="song-info-label">Artist</span>
        <span class="song-info-value reveal-text" ${blurStyle}>${escapeHtml(song.artist)}</span>
      </div>
      <div class="song-info-item">
        <span class="song-info-icon">💿</span>
        <span class="song-info-label">Album</span>
        <span class="song-info-value reveal-text" ${blurStyle}>${escapeHtml(song.album)}</span>
      </div>
    </section>
  `;
}

function timerHtml() {
  return `
    <div class="timer-container">
      <div class="timer-ring paused" id="timer-ring">
        <svg class="timer-svg" width="190" height="190" viewBox="0 0 190 190">
          <defs>
            <linearGradient id="timerGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#818cf8" />
              <stop offset="100%" stop-color="#0ea5e9" />
            </linearGradient>
          </defs>
          <circle cx="95" cy="95" r="80" fill="none" stroke="#21262d" stroke-width="10"></circle>
          <circle cx="95" cy="95" r="80" fill="none" stroke="#30363d" stroke-width="10" opacity="0.3"></circle>
          <circle id="timer-circle" cx="95" cy="95" r="80" fill="none" stroke="url(#timerGradient)" stroke-width="10"
            stroke-linecap="round" stroke-dasharray="502.65" stroke-dashoffset="0"></circle>
        </svg>
        <div class="timer-text">
          <div id="timer-seconds" class="timer-seconds">${maxGuessTime}</div>
          <div id="timer-label" class="timer-label">paused</div>
        </div>
      </div>
    </div>
  `;
}

function gameOverMessage(lastScore) {
  const guess = lastScore.guess;
  const diff = Math.abs(guess - lastScore.actual);
  let emoji;
  let message;
  let subtitle;
  let color;

  if (state.timedOut) {
    emoji = "⏰";
    message = "TIME'S UP!";
    subtitle = `Your guess of ${guess} was submitted.`;
    color = "#f59e0b";
  } else if (diff === 0) {
    emoji = "🎉";
    message = "PERFECT!";
    subtitle = "You got it exactly right!";
    color = "#00ff88";
  } else if (diff <= 2) {
    emoji = "🎵";
    message = "Excellent!";
    subtitle = `Off by only ${diff} year${diff > 1 ? "s" : ""}!`;
    color = "#22d3ee";
  } else if (diff <= 5) {
    emoji = "🎶";
    message = "Good job!";
    subtitle = `Close! Off by ${diff} years.`;
    color = "#a78bfa";
  } else {
    emoji = "🎸";
    message = "Nice try!";
    subtitle = `Off by ${diff} years.`;
    color = "#8b5cf6";
  }

  return `
    <section class="result-container fade-in">
      <div class="result-emoji">${emoji}</div>
      <div class="result-message" style="color: ${color}">${message}</div>
      <div class="result-subtitle">${escapeHtml(subtitle)}</div>
    </section>
  `;
}

function answerComparison(actualYear, guessedYear) {
  const diff = guessedYear - actualYear;
  let diffText;
  if (diff === 0) {
    diffText = `<span style="color: #00ff88;">Perfect match!</span>`;
  } else if (diff > 0) {
    diffText = `<span style="color: #ef4444;">+${diff} years (too recent)</span>`;
  } else {
    diffText = `<span style="color: #3b82f6;">${diff} years (too early)</span>`;
  }

  return `
    <section class="answer-comparison" data-testid="answer-comparison">
      <div class="answer-row">
        <span class="answer-label">Correct Year</span>
        <span class="answer-value correct">${actualYear}</span>
      </div>
      <div class="answer-row">
        <span class="answer-label">Your Guess</span>
        <span class="answer-value guess">${guessedYear}</span>
      </div>
      <div class="answer-diff">${diffText}</div>
    </section>
  `;
}

function scoreCard(score) {
  const scoreClass =
    score >= 800
      ? "score-excellent"
      : score >= 600
        ? "score-great"
        : score >= 400
          ? "score-good"
          : score >= 200
            ? "score-okay"
            : "score-poor";

  return `<div class="score-card"><span class="${scoreClass}">+${score} points</span></div>`;
}

function spotifyButton(url) {
  return `
    <div class="listen-btn-container">
      <a class="spotify-btn" href="${escapeAttr(url)}" target="_blank" rel="noreferrer">
        <svg class="spotify-icon" width="20" height="20" viewBox="0 0 24 24" fill="#1DB954" aria-hidden="true">
          <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.021-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
        </svg>
        Listen on Spotify
      </a>
    </div>
  `;
}

function songHistoryHtml() {
  if (!state.playerScores.length) {
    return "";
  }

  const items = [...state.playerScores]
    .slice(-5)
    .reverse()
    .map((score) => {
      const diff = Math.abs(score.guess - score.actual);
      const accuracyClass = diff === 0 ? "perfect" : diff <= 2 ? "close" : diff <= 5 ? "ok" : "far";
      const icon = diff === 0 ? "🎯" : diff <= 2 ? "✓" : diff <= 5 ? "○" : "✗";
      return `
        <div class="history-item ${accuracyClass}">
          <span class="history-accuracy">${icon}</span>
          <span class="history-song">${escapeHtml(score.song)}</span>
          <span class="history-years">${score.guess} / ${score.actual}</span>
          <span class="history-score">+${score.score}</span>
        </div>
      `;
    })
    .join("");

  return `
    <section class="history-container">
      <div class="history-header">📜 Recent Songs</div>
      ${items}
    </section>
  `;
}

function renderGame() {
  clearTimers();

  const song = state.currentSong;
  const lastScore = state.playerScores[state.playerScores.length - 1];
  const audioType = String(song.preview_url).startsWith("data:audio/wav")
    ? "audio/wav"
    : "audio/mpeg";
  const resultMarkup = state.gameOver && lastScore ? gameOverMessage(lastScore) : "";
  const rightMarkup =
    state.gameOver && lastScore
      ? `
          ${answerComparison(song.year, lastScore.guess)}
          ${scoreCard(lastScore.score)}
          ${spotifyButton(song.deezer_url)}
          <div class="button-row">
            <button class="primary-button" id="next-song" data-testid="next-song">▶️ Next Song</button>
            <button class="secondary-button" id="end-game" data-testid="end-game">🏁 End Game</button>
          </div>
        `
      : `
          <div class="year-picker-wrap">
            <div class="year-picker-label">Select release year</div>
            <div class="year-wheel" id="year-wheel" data-testid="year-wheel" tabindex="0">
              <div class="year-track" id="year-track"></div>
              <div class="selection-box"></div>
            </div>
            <div class="submit-label" id="submit-label"><strong>Click to submit:</strong></div>
            <button class="year-submit" id="submit-guess" data-testid="submit-guess">${state.currentGuess}</button>
          </div>
          ${timerHtml()}
        `;

  app.innerHTML = `
    ${renderHeader()}
    ${resultMarkup}
    <section class="game-layout fade-in" data-testid="game-layout">
      <div class="left-column">
        <div class="album-container">
          <img class="album-art" id="album-art" data-testid="album-art" src="${escapeAttr(song.image_url)}" alt="Album artwork" style="filter: blur(${state.gameOver ? 0 : 25}px)" />
        </div>
        ${audioVisualizerHtml(false)}
        <div class="audio-container">
          <audio id="game-audio" controls ${state.gameOver ? "" : "autoplay"} data-testid="audio-player">
            <source src="${escapeAttr(song.preview_url)}" type="${audioType}" />
            Your browser does not support the audio element.
          </audio>
        </div>
        ${songInfoCard(song, state.gameOver ? 0 : 8)}
      </div>
      <div class="right-column">
        ${rightMarkup}
      </div>
    </section>
    ${songHistoryHtml()}
  `;

  attachAudioEvents();

  if (state.gameOver) {
    document.querySelector("#next-song").addEventListener("click", () => loadNextSong());
    document.querySelector("#end-game").addEventListener("click", endGame);
  } else {
    setupYearPicker();
    setupTimer();
    document.querySelector("#submit-guess").addEventListener("click", () => submitGuess(false));
  }
}

function attachAudioEvents() {
  const audio = document.querySelector("#game-audio");
  const visualizer = document.querySelector("#audio-viz");
  if (!audio) {
    return;
  }

  function setViz(playing) {
    visualizer?.classList.toggle("audio-viz-static", !playing);
  }

  audio.addEventListener("play", () => {
    setViz(true);
    if (!state.audioStarted) {
      state.audioStarted = true;
      state.timerStartedAt = performance.now();
      state.timerPausedAt = 0;
      state.timerPausedMs = 0;
      state.timerPaused = false;
    } else if (state.timerPaused) {
      state.timerPausedMs += performance.now() - state.timerPausedAt;
      state.timerPausedAt = 0;
      state.timerPaused = false;
    }
    updateTimer();
    updateReveal();
  });

  audio.addEventListener("pause", () => {
    if (audio.ended) {
      setViz(false);
      return;
    }
    setViz(false);
    if (state.audioStarted && !state.timerPaused) {
      state.timerPaused = true;
      state.timerPausedAt = performance.now();
    }
    updateTimer();
  });

  audio.addEventListener("ended", () => {
    setViz(false);
  });

  if (!state.gameOver) {
    audio.play().catch(() => {
      setViz(false);
    });
  }
}

function setupYearPicker() {
  const wheel = document.querySelector("#year-wheel");
  const track = document.querySelector("#year-track");
  const itemHeight = Math.round(350 / 7);

  function buildTrack() {
    const years = [];
    for (let year = state.startYear; year <= state.endYear; year += 1) {
      years.push(year);
    }
    track.innerHTML = years
      .map((year) => `<div class="year-item" data-year="${year}" style="height:${itemHeight}px">${year}</div>`)
      .join("");
  }

  function updatePosition() {
    const offset = (state.currentGuess - state.startYear) * itemHeight;
    const centerOffset = 350 / 2 - itemHeight / 2;
    track.style.transform = `translateY(${centerOffset - offset}px)`;

    for (const item of track.querySelectorAll(".year-item")) {
      const year = Number(item.dataset.year);
      const distance = Math.abs(year - state.currentGuess);
      item.classList.toggle("selected", distance === 0);
      item.classList.toggle("near", distance === 1);
    }

    const submit = document.querySelector("#submit-guess");
    if (submit) {
      submit.textContent = String(state.currentGuess);
    }
  }

  function setYear(year) {
    if (state.timeLocked) {
      return;
    }
    const newYear = clamp(Math.round(year), state.startYear, state.endYear);
    if (newYear !== state.currentGuess) {
      state.currentGuess = newYear;
      updatePosition();
    }
  }

  buildTrack();
  updatePosition();

  let accumulatedDelta = 0;
  wheel.addEventListener(
    "wheel",
    (event) => {
      event.preventDefault();
      accumulatedDelta += event.deltaY;
      if (Math.abs(accumulatedDelta) >= 15) {
        setYear(state.currentGuess + Math.sign(accumulatedDelta));
        accumulatedDelta = 0;
      }
    },
    { passive: false }
  );

  let dragging = false;
  let didDrag = false;
  let dragStartY = 0;
  let dragStartYear = state.currentGuess;

  function startDrag(clientY) {
    if (state.timeLocked) {
      return;
    }
    dragging = true;
    didDrag = false;
    dragStartY = clientY;
    dragStartYear = state.currentGuess;
    wheel.style.cursor = "grabbing";
  }

  function moveDrag(clientY) {
    if (!dragging) {
      return;
    }
    const deltaY = dragStartY - clientY;
    if (Math.abs(deltaY) > 5) {
      didDrag = true;
    }
    setYear(dragStartYear + Math.round(deltaY / 30));
  }

  function endDrag() {
    if (dragging && didDrag && !state.timeLocked && !state.gameOver) {
      submitGuess(false);
    }
    dragging = false;
    didDrag = false;
    wheel.style.cursor = "ns-resize";
  }

  wheel.addEventListener("mousedown", (event) => {
    startDrag(event.clientY);
    event.preventDefault();
  });
  wheel.addEventListener(
    "touchstart",
    (event) => {
      startDrag(event.touches[0].clientY);
      event.preventDefault();
    },
    { passive: false }
  );
  document.addEventListener("mousemove", (event) => moveDrag(event.clientY));
  document.addEventListener(
    "touchmove",
    (event) => {
      if (dragging) {
        moveDrag(event.touches[0].clientY);
        event.preventDefault();
      }
    },
    { passive: false }
  );
  document.addEventListener("mouseup", endDrag);
  document.addEventListener("touchend", endDrag);

  wheel.addEventListener("click", (event) => {
    const item = event.target.closest(".year-item");
    if (item) {
      setYear(Number(item.dataset.year));
    }
  });

  wheel.addEventListener("keydown", (event) => {
    if (event.key === "ArrowUp" || event.key === "ArrowLeft") {
      event.preventDefault();
      setYear(state.currentGuess - 1);
    } else if (event.key === "ArrowDown" || event.key === "ArrowRight") {
      event.preventDefault();
      setYear(state.currentGuess + 1);
    }
  });
}

function setupTimer() {
  updateTimer();
  updateReveal();
  state.timerInterval = setInterval(updateTimer, 100);
  state.revealInterval = setInterval(updateReveal, 250);
}

function updateTimer() {
  if (state.gameOver) {
    return;
  }

  const elapsed = Math.min(currentElapsedSeconds(), maxGuessTime);
  const remaining = Math.max(0, Math.ceil(maxGuessTime - elapsed));
  const progress = elapsed / maxGuessTime;
  const offset = 2 * Math.PI * 80 * progress;
  const color = timerColor(progress);

  const ring = document.querySelector("#timer-ring");
  const circle = document.querySelector("#timer-circle");
  const seconds = document.querySelector("#timer-seconds");
  const label = document.querySelector("#timer-label");

  if (!ring || !circle || !seconds || !label) {
    return;
  }

  circle.style.strokeDashoffset = String(offset);
  circle.style.stroke = color;
  seconds.style.color = color;

  if (seconds.textContent !== String(remaining)) {
    seconds.classList.remove("pulse");
    void seconds.offsetWidth;
    seconds.classList.add("pulse");
    seconds.textContent = String(remaining);
  }

  ring.classList.toggle("paused", state.timerPaused);
  ring.classList.toggle("warning", !state.timerPaused && remaining <= 10 && remaining > 5);
  ring.classList.toggle("danger", !state.timerPaused && remaining <= 5 && remaining > 3);
  ring.classList.toggle("critical", !state.timerPaused && remaining <= 3 && remaining > 0);
  label.classList.toggle("urgent", remaining <= 5);

  if (state.timerPaused) {
    label.textContent = "paused";
  } else if (remaining <= 0) {
    label.textContent = "TIME'S UP";
  } else {
    label.textContent = remaining <= 5 ? "hurry!" : "seconds";
  }

  if (state.audioStarted && elapsed >= maxGuessTime && !state.timeLocked) {
    state.timeLocked = true;
    const wheel = document.querySelector("#year-wheel");
    const submit = document.querySelector("#submit-guess");
    const labelEl = document.querySelector("#submit-label");
    wheel?.classList.add("locked");
    submit?.classList.add("urgent");
    if (labelEl) {
      labelEl.innerHTML = "<strong>⏰ TIME'S UP - submitting:</strong>";
    }
    submitGuess(true);
  }
}

function updateReveal() {
  if (state.gameOver) {
    return;
  }

  let albumBlur = 25;
  let textBlur = 8;
  const elapsed = currentElapsedSeconds();
  if (state.audioStarted && elapsed >= 1) {
    albumBlur = Math.max(0, 25 - (elapsed * 25) / hintRevealTime);
    textBlur = Math.max(0, 8 - (elapsed * 8) / hintRevealTime);
  }

  const album = document.querySelector("#album-art");
  if (album) {
    album.style.filter = `blur(${albumBlur.toFixed(1)}px)`;
  }
  for (const item of document.querySelectorAll(".reveal-text")) {
    item.style.filter = textBlur > 0 ? `blur(${textBlur.toFixed(1)}px)` : "";
  }
}

async function startGame() {
  if (!state.currentPlayer.trim()) {
    state.currentPlayer = "Player 1";
  }
  state.statusMessage = "🔍 Searching for a song...";
  renderWelcome();

  state.currentRound = 0;
  state.playerScores = [];
  state.playedSongIds = new Set();
  state.playedSongKeys = new Set();
  await loadNextSong();
}

async function loadNextSong() {
  clearTimers();
  state.gameActive = true;
  state.statusMessage = "";
  resetRoundTimer();

  app.innerHTML = `
    ${mainTitle()}
    <div class="status-line" data-testid="status-line">🔍 Searching for a song...</div>
  `;

  try {
    const result = await apiJson("/api/song", {
      method: "POST",
      body: JSON.stringify({
        startYear: state.startYear,
        endYear: state.endYear,
        genre: state.selectedGenre,
        playedIds: [...state.playedSongIds],
        playedKeys: [...state.playedSongKeys]
      })
    });

    state.currentSong = result.song;
    state.playedSongIds.add(result.song.id);
    if (result.song.song_key) {
      state.playedSongKeys.add(result.song.song_key);
    }
    state.currentRound += 1;
    state.currentGuess = Math.floor((state.startYear + state.endYear) / 2);
    state.gameOver = false;
    state.timedOut = false;
    renderGame();
  } catch (error) {
    state.statusMessage = error.message;
    renderWelcome();
  }
}

function submitGuess(timedOut) {
  if (state.gameOver || !state.currentSong) {
    return;
  }

  const timeTaken = timedOut ? maxGuessTime : Math.trunc(currentElapsedSeconds());
  const song = state.currentSong;
  const score = calculateScore(state.currentGuess, song.year, timeTaken);

  state.timedOut = Boolean(timedOut);
  state.gameOver = true;
  state.timeLocked = false;
  state.playerScores.push({
    player: state.currentPlayer,
    song: `${song.name} by ${song.artist}`,
    guess: state.currentGuess,
    actual: song.year,
    score,
    time: timeTaken
  });

  clearTimers();
  renderGame();
}

async function endGame() {
  app.innerHTML = `
    ${mainTitle()}
    <div class="status-line" data-testid="status-line">💾 Saving your score to the leaderboard...</div>
  `;

  if (songsPlayed() > 0) {
    try {
      const result = await apiJson("/api/leaderboard", {
        method: "POST",
        body: JSON.stringify({
          player: state.currentPlayer,
          totalScore: totalScore(),
          songsPlayed: songsPlayed(),
          genre: state.selectedGenre
        })
      });

      if (!result.persistent && result.entry) {
        const local = getLocalLeaderboard();
        local.push(result.entry);
        setLocalLeaderboard(local);
      }
      state.statusMessage = result.message || "Score saved!";
    } catch (error) {
      const local = getLocalLeaderboard();
      local.push(makeLocalLeaderboardEntry());
      setLocalLeaderboard(local);
      state.statusMessage = `${error.message} Saved in this browser.`;
    }
  }

  state.gameActive = false;
  state.gameOver = false;
  state.currentRound = 0;
  state.playerScores = [];
  state.playedSongIds = new Set();
  state.playedSongKeys = new Set();
  state.currentSong = null;
  resetRoundTimer();
  await loadLeaderboard();
  renderWelcome();
}

async function init() {
  await loadConfig();
  await loadLeaderboard();
  renderWelcome();
}

window.__songYearGuesser = {
  state,
  calculateScore,
  submitGuess,
  loadNextSong
};

init();
