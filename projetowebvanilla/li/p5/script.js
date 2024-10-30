const words = ['javascript', 'html', 'css', 'react', 'nodejs', 'jquery', 'angular', 'vue'];
let selectedWord = words[Math.floor(Math.random() * words.length)];
let guessedWord = Array(selectedWord.length).fill('_');

let wrongAttempts = 0;
const maxWrongAttempts = 6;

const hangmanContainer = document.getElementById('hangman-container');

function updateWordDisplay() {
    hangmanContainer.innerHTML = guessedWord.join(' ');
}

function drawHangman() {
    // Desenhar a forca
    // Aqui você pode usar HTML/CSS para desenhar o enforcado
}

function checkGameOver() {
    if (wrongAttempts === maxWrongAttempts) {
        alert('Você perdeu! A palavra era: ' + selectedWord);
        resetGame();
    } else if (guessedWord.join('') === selectedWord) {
        alert('Parabéns! Você ganhou!');
        resetGame();
    }
}

function resetGame() {
    selectedWord = words[Math.floor(Math.random() * words.length)];
    guessedWord = Array(selectedWord.length).fill('_');
    wrongAttempts = 0;
    updateWordDisplay();
}

updateWordDisplay();

document.addEventListener('keydown', event => {
    const letter = event.key.toLowerCase();
    if (guessedWord.indexOf(letter) === -1) {
        if (selectedWord.includes(letter)) {
            for (let i = 0; i < selectedWord.length; i++) {
                if (selectedWord[i] === letter) {
                    guessedWord[i] = letter;
                }
            }
        } else {
            wrongAttempts++;
            drawHangman();
        }

        updateWordDisplay();
        checkGameOver();
    }
});
