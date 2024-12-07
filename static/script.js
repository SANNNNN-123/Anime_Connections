// Game data
const groups = [
  {
    category: "Protagonists",
    words: ["NARUTO", "LUFFY", "GOKU", "ICHIGO"],
    difficulty: 1
  },
  {
    category: "Studios",
    words: ["MAPPA", "BONES", "UFOTABLE", "MADHOUSE"],
    difficulty: 2
  },
  {
    category: "Genres",
    words: ["SHOUNEN", "MECHA", "ISEKAI", "SLICE"],
    difficulty: 3
  },
  {
    category: "Anime Terms",
    words: ["KAWAII", "SENPAI", "OTAKU", "WAIFU"],
    difficulty: 4
  }
];

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

function showSuccessNotification(category) {
  const notification = document.getElementById('success-notification');
  const categorySpan = document.getElementById('category-name');
  
  categorySpan.textContent = category;
  notification.style.display = 'block';
  
  // Remove any existing animation classes
  notification.classList.remove('slide-out');
  
  // Automatically hide after 3 seconds
  setTimeout(() => {
      notification.style.animation = 'slideOut 0.3s ease-out forwards';
      setTimeout(() => {
          notification.style.display = 'none';
          notification.style.animation = '';
      }, 300);
  }, 3000);
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
  }

  initialize(onUpdate) {
    this.onUpdate = onUpdate;
    this.words = this.shuffleWords();
    this.startTimer();
    this.update();
  }

  shuffleWords() {
    const allWords = groups.flatMap(group => group.words);
    return shuffleArray(allWords);
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

  findGroupForWord(word) {
    return groups.findIndex(group => 
      group.words.includes(word)
    );
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
      if (this.solvedGroups.size === groups.length) {
        this.endGame(true);
      }
    } else {
      this.mistakes--;
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

  endGame(won) {
      clearInterval(this.timer);
      if (won) {
          const timeSpent = 240 - this.timeLeft;
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
          alert('Game Over!');
      }
      this.update();
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
document.getElementById('new-game').addEventListener('click', () => initGame());

function initGame() {
  game.initialize(updateUI);
}

// Start the game when the page loads
document.addEventListener('DOMContentLoaded', initGame);