const words = ['javascript', 'html', 'css', 'python', 'java', 'ruby', 'php', 'csharp', 'swift', 'typescript'];

let chosenWord = words[Math.floor(Math.random() * words.length)];
let guessedWord = '';
let attemptsLeft = 6;
let usedLetters = '';

// Inicializa a palavra a ser adivinhada com underscores
for (let i = 0; i < chosenWord.length; i++) {
    guessedWord += '_';
}

document.getElementById('wordDisplay').textContent = guessedWord;

function checkGuess() {
    const guess = document.getElementById('guessInput').value.toLowerCase();
    const message = document.getElementById('message');
    
    if (guess.length !== 1 || !(/[a-z]/.test(guess))) {
        message.textContent = 'Por favor, insira apenas uma letra válida.';
        return;
    }
    
    if (usedLetters.includes(guess)) {
        message.textContent = 'Você já usou essa letra. Tente outra.';
        return;
    }
    
    usedLetters += guess + ' ';
    document.getElementById('usedLetters').textContent = usedLetters;
    
    let letterFound = false;
    for (let i = 0; i < chosenWord.length; i++) {
        if (chosenWord[i] === guess) {
            guessedWord = guessedWord.substring(0, i) + guess + guessedWord.substring(i + 1);
            letterFound = true;
        }
    }
    
    if (!letterFound) {
        attemptsLeft--;
        document.getElementById('attempts').textContent = attemptsLeft;
    }
    
    document.getElementById('wordDisplay').textContent = guessedWord;
    
    if (guessedWord === chosenWord) {
        message.textContent = 'Parabéns! Você ganhou!';
        document.getElementById('guessInput').disabled = true;
    } else if (attemptsLeft === 0) {
        message.textContent = `Você perdeu! A palavra era "${chosenWord}".`;
        document.getElementById('guessInput').disabled = true;
    }
}
