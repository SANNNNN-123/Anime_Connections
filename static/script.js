// Game data for different difficulty levels

const DIFFICULTY_TIMES = {
  easy: 90,    // 1:30 minutes, 90
  medium: 180, // 3:00 minutes, 180
  hard: 300    // 8:00 minutes, 300
};

// Initialize game data
let difficultyLevels = {
  easy: { time: DIFFICULTY_TIMES.easy, groups: [] },
  medium: { time: DIFFICULTY_TIMES.medium, groups: [] },
  hard: { time: DIFFICULTY_TIMES.hard, groups: [] }
};

// Load initial data
// Function to fetch data from the server
async function fetchOnePieceData(difficulty) {
  showLoading();
  try {
    const response = await fetch(`/api/onepiece-data?difficulty=${difficulty}`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching One Piece data:', error);
    return [];
  } finally {
    hideLoading(); 
  }
}

//loading animation
function showLoading() {
  const loadingElement = document.querySelector('.loading-container');
  if (!loadingElement) {
    const loading = document.createElement('div');
    loading.className = 'loading-container';
    loading.innerHTML = `
      <div class="loading-spinner"></div>
      <div class="loading-text">Loading...</div>
    `;
    document.body.appendChild(loading);
  }
}

function hideLoading() {
  const loadingElement = document.querySelector('.loading-container');
  if (loadingElement) {
    loadingElement.remove();
  }
}


// Load initial data
async function loadInitialData() {
  showLoading();
  for (const difficulty of ['easy', 'medium', 'hard']) {
    const data = await fetchOnePieceData(difficulty);
    difficultyLevels[difficulty].groups = data.map(item => ({
      category: item.category,
      words: item.words,
      difficulty: difficulty === 'easy' ? 1 : difficulty === 'medium' ? 2 : 3
    }));
  }
  hideLoading();
  // Start the game after data is loaded
  game.initialize(updateUI, 'easy');
}

// Utility functions
function shuffleArray(array) {
  const newArray = [...array];
  for (let i = newArray.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
  }
  return newArray;
}

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

function showNotification(type, category = '', difficulty = '') {
  // Remove any existing notifications
  const existingNotification = document.querySelector('.game-notification');
  if (existingNotification) {
    existingNotification.remove();
  }

  const notification = document.createElement('div');
  notification.className = `game-notification ${type} ${difficulty}`;
  
  let icon, title, message;
  if (type === 'correct') {
    icon = '✓';
    title = 'Correct!';
    message = `Category: ${category}`;
  } else if (type === 'wrong') {
    icon = '✕';
    title = 'Wrong!';
    message = 'Try again';
  } else if (type === 'time') {
    icon = '⏳';
    title = 'Time\'s Up!';
    message = 'Loading new data...';
  }
  
  notification.innerHTML = `
    <div class="notification-content">
      <div class="notification-icon">${icon}</div>
      <div class="notification-message">
        <h3>${title}</h3>
        <p>${message}</p>
      </div>
    </div>
  `;
  
  document.body.appendChild(notification);
  
  // Trigger animation
  setTimeout(() => {
    notification.classList.add('show');
    setTimeout(() => {
      notification.classList.remove('show');
      setTimeout(() => {
        notification.remove();
      }, 300);
    }, 2000);
  }, 100);
}

function initGame(difficulty) {
  game.initialize(updateUI, difficulty);
}

// Game class
class Game {
  constructor() {
    this.words = [];
    this.selectedWords = new Set();
    this.mistakes = 4;
    this.solvedGroups = new Set();
    this.timeLeft = 240;
    this.timer = null;
    this.onUpdate = null;
    this.currentDifficulty = 'easy';
  }

  initialize(onUpdate,difficulty = 'easy') {
    // Check if difficulty is an event object
    if (difficulty && typeof difficulty === 'object') {
      // Try multiple ways to extract difficulty
      difficulty = difficulty.target?.dataset?.difficulty 
                || difficulty.currentTarget?.dataset?.difficulty
                || difficulty.difficulty 
                || 'easy';
    }

    showLoading();
    this.update();

    // Rest of your initialization method
    if (!difficultyLevels[difficulty]) {
      console.error(`Invalid difficulty level: ${difficulty}`);
      difficulty = 'easy';
    }

    this.currentDifficulty = difficulty;
    // Clear previous game state
    this.selectedWords.clear();
    this.solvedGroups.clear();
    this.mistakes = 4;
    this.timeLeft = difficultyLevels[difficulty]?.time

    if (this.timer) {
      clearInterval(this.timer);
    }
   
    this.onUpdate = onUpdate;
    this.words = this.shuffleWords();
    this.startTimer();
    hideLoading();
    this.update();
  }

  shuffleWords() {
    const allWords = difficultyLevels[this.currentDifficulty].groups.flatMap(group => group.words);
    return shuffleArray(allWords);
  }

  findGroupForWord(word) {
    return difficultyLevels[this.currentDifficulty].groups.findIndex(group => 
      group.words.includes(word)
    );
  }

  toggleWord(word) {
    if (this.solvedGroups.has(this.findGroupForWord(word))) return;
    
    if (this.selectedWords.has(word)) {
      this.selectedWords.delete(word);
    } else if (this.selectedWords.size < 4) {
      this.selectedWords.add(word);
    }
    this.update();
  }

  submitGuess() {
    if (this.selectedWords.size !== 4) return;

    const selectedArray = Array.from(this.selectedWords);
    const groupIndex = this.findGroupForWord(selectedArray[0]);
    const isCorrect = selectedArray.every(word => 
      this.findGroupForWord(word) === groupIndex
    );

    if (isCorrect) {
      this.solvedGroups.add(groupIndex);
      this.selectedWords.clear();
      if (this.solvedGroups.size === difficultyLevels[this.currentDifficulty].groups.length) {
        this.endGame(true);
      }
      showNotification('correct', difficultyLevels[this.currentDifficulty].groups[groupIndex].category);
    } else {
      this.mistakes--;
      showNotification('wrong');
      if (this.mistakes === 0) {
        this.endGame(false);
      }
    }
    this.update();
  }

  deselectAll() {
    this.selectedWords.clear();
    this.update();
  }

  startTimer() {
    this.timer = setInterval(() => {
      this.timeLeft--;
      if (this.timeLeft === 0) {
        this.endGame(false);
      }
      this.update();
    }, 1000);
  }

  async endGame(won) {
    clearInterval(this.timer);
    if (won) {
      const timeSpent = difficultyLevels[this.currentDifficulty].time - this.timeLeft;
          
      const modal = document.getElementById('score-modal');
      const finalTime = document.getElementById('final-time');
      finalTime.textContent = formatTime(timeSpent);
      modal.style.display = 'flex';
          
      // Handle score submission
      const submitButton = document.getElementById('submit-score');
      submitButton.onclick = async () => {
          const playerName = document.getElementById('player-name').value;
          if (!playerName) return;
              
          try {
              const response = await fetch('/submit-score', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({
                      name: playerName,
                      time: formatTime(timeSpent)
                  })
              });
                  
              if (response.ok) {
                  // Refresh the page to update leaderboard
                  window.location.reload();
              }
          } catch (error) {
              console.error('Error submitting score:', error);
          }
      };
    } else {
      hideLoading();
      showNotification('time', 'Time\'s Up!', this.currentDifficulty);
      await this.loadNewData();
    }
    this.update();
  }

  async loadNewData() {
    showLoading();
    try {
      const response = await fetch(`/api/new-onepiece-data?difficulty=${this.currentDifficulty}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      difficultyLevels[this.currentDifficulty].groups = data.map(item => ({
        category: item.category,
        words: item.words,
        difficulty: this.currentDifficulty === 'easy' ? 1 : this.currentDifficulty === 'medium' ? 2 : 3
      }));
      this.initialize(this.onUpdate, this.currentDifficulty);
    } catch (error) {
      console.error('Error fetching new One Piece data:', error);
    } finally {
      hideLoading();
    }
  }

  update() {
    if (this.onUpdate) {
      this.onUpdate({
        words: this.words,
        selectedWords: this.selectedWords,
        mistakes: this.mistakes,
        solvedGroups: this.solvedGroups,
        timeLeft: this.timeLeft
      });
    }
  }
}

// Game initialization and UI updates
const game = new Game();

function updateUI(gameState) {
  const { words, selectedWords, mistakes, solvedGroups, timeLeft } = gameState;
  
  document.getElementById('mistakes').textContent = mistakes;
  document.getElementById('timer').textContent = formatTime(timeLeft);

  const grid = document.getElementById('grid');
  grid.innerHTML = '';
  
  words.forEach(word => {
    const tile = document.createElement('div');
    tile.className = 'word-tile';
    if (selectedWords.has(word)) tile.classList.add('selected');
    if (solvedGroups.has(game.findGroupForWord(word))) tile.classList.add('solved');
    tile.textContent = word;
    tile.addEventListener('click', () => game.toggleWord(word));
    grid.appendChild(tile);
  });
}

// Event listeners
document.getElementById('submit').addEventListener('click', () => game.submitGuess());
document.getElementById('deselect').addEventListener('click', () => game.deselectAll());
document.getElementById('new-game').addEventListener('click', () => initGame('easy'));
document.getElementById('easy-game').addEventListener('click', () => initGame('easy'));
document.getElementById('medium-game').addEventListener('click', () => initGame('medium'));
document.getElementById('hard-game').addEventListener('click', () => initGame('hard'));

function initGame(difficulty) {
  game.initialize(updateUI, difficulty);
}

// Start the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
  // Load initial data for all difficulties
  loadInitialData();
});