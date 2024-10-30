// Gerar um número aleatório entre 1 e 100
const randomNumber = Math.floor(Math.random() * 100) + 1;

// Contador de tentativas
let attempts = 0;

// Função para verificar o palpite do jogador
function checkGuess() {
    const guess = parseInt(document.getElementById('guessInput').value);
    const message = document.getElementById('message');

    if (isNaN(guess) || guess < 1 || guess > 100) {
        message.textContent = 'Por favor, insira um número válido entre 1 e 100.';
        return;
    }

    attempts++;

    if (guess === randomNumber) {
        message.textContent = `Parabéns! Você acertou o número em ${attempts} tentativas.`;
    } else if (guess < randomNumber) {
        message.textContent = 'O número é maior. Tente novamente.';
    } else {
        message.textContent = 'O número é menor. Tente novamente.';
    }
}
