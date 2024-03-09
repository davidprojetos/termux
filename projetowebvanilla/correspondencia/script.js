const icons = ['🎁', '🎈', '🎉', '🎂', '🍰', '🍭', '🍬', '🍦'];

let cards = [];
let firstCard = null;
let secondCard = null;
let matches = 0;

function createCards() {
    const gameBoard = document.getElementById('gameBoard');
    cards = [];
    matches = 0;
    gameBoard.innerHTML = '';

    // Duplicate and shuffle icons
    const shuffledIcons = icons.concat(icons).sort(() => Math.random() - 0.5);

    shuffledIcons.forEach(icon => {
        const card = document.createElement('div');
        card.classList.add('card');
        card.textContent = icon;
        card.addEventListener('click', () => flipCard(card));
        gameBoard.appendChild(card);
        cards.push({ element: card, icon: icon, matched: false });
    });
}

function flipCard(card) {
    if (card === firstCard || card === secondCard || cardMatched(card)) {
        return;
    }

    card.textContent = card.dataset.icon;
    if (!firstCard) {
        firstCard = card;
    } else if (!secondCard) {
        secondCard = card;
        setTimeout(checkMatch, 1000);
    }
}

function checkMatch() {
    if (firstCard.dataset.icon === secondCard.dataset.icon) {
        firstCard.removeEventListener('click', () => flipCard(firstCard));
        secondCard.removeEventListener('click', () => flipCard(secondCard));
        firstCard.classList.add('matched');
        secondCard.classList.add('matched');
        matches++;

        if (matches === icons.length) {
            setTimeout(() => {
                alert('Parabéns! Você venceu!');
                resetGame();
            }, 500);
        }
    } else {
        firstCard.textContent = '';
        secondCard.textContent = '';
    }

    firstCard = null;
    secondCard = null;
}

function cardMatched(card) {
    return card.classList.contains('matched');
}

function resetGame() {
    createCards();
}

createCards();
