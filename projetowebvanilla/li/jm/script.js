const images = ['image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg', 'image5.jpg', 'image6.jpg', 'image7.jpg', 'image8.jpg'];

const memoryGame = document.getElementById('memory-game');

// Shuffle images
const shuffledImages = [...images, ...images].sort(() => Math.random() - 0.5);

shuffledImages.forEach(image => {
    const card = document.createElement('div');
    card.classList.add('memory-card');

    const frontFace = document.createElement('div');
    frontFace.classList.add('front-face');
    frontFace.style.backgroundImage = `url("images/${image}")`;

    const backFace = document.createElement('div');
    backFace.classList.add('back-face');

    card.appendChild(frontFace);
    card.appendChild(backFace);

    card.addEventListener('click', flipCard);

    memoryGame.appendChild(card);
});

let hasFlippedCard = false;
let lockBoard = false;
let firstCard, secondCard;

function flipCard() {
    if (lockBoard) return;
    if (this === firstCard) return;

    this.classList.add('flip');

    if (!hasFlippedCard) {
        hasFlippedCard = true;
        firstCard = this;
        return;
    }

    secondCard = this;
    checkForMatch();
}

function checkForMatch() {
    let isMatch = firstCard.querySelector('.front-face').style.backgroundImage === secondCard.querySelector('.front-face').style.backgroundImage;

    isMatch ? disableCards() : unflipCards();
}

function disableCards() {
    firstCard.removeEventListener('click', flipCard);
    secondCard.removeEventListener('click', flipCard);

    resetBoard();
}

function unflipCards() {
    lockBoard = true;

    setTimeout(() => {
        firstCard.classList.remove('flip');
        secondCard.classList.remove('flip');

        resetBoard();
    }, 1000);
}

function resetBoard() {
    [hasFlippedCard, lockBoard] = [false, false];
    [firstCard, secondCard] = [null, null];
}
