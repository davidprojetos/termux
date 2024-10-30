document.addEventListener('DOMContentLoaded', function() {
    const API_URL = 'https://opentdb.com/api.php?amount=10&type=multiple';
    const questionContainer = document.getElementById('question-container');
    const questionElement = document.getElementById('question');
    const optionsElement = document.getElementById('options');
    const scoreElement = document.getElementById('score-value');
    const startButton = document.getElementById('start-btn');
    const nextButton = document.getElementById('next-btn');

    let questions = [];
    let currentQuestionIndex = 0;
    let score = 0;

    startButton.addEventListener('click', startGame);

    function startGame() {
        startButton.style.display = 'none';
        score = 0;
        scoreElement.textContent = score;
        fetchQuestions();
    }

    async function fetchQuestions() {
        try {
            const response = await fetch(API_URL);
            const data = await response.json();
            questions = data.results;
            nextQuestion();
        } catch (error) {
            console.error('Erro ao obter perguntas:', error);
        }
    }

    function nextQuestion() {
        resetOptions();
        if (currentQuestionIndex < questions.length) {
            const question = questions[currentQuestionIndex];
            showQuestion(question);
        } else {
            endGame();
        }
    }

    function showQuestion(question) {
        questionElement.textContent = question.question;
        const options = shuffleArray([...question.incorrect_answers, question.correct_answer]);
        options.forEach(option => {
            const li = document.createElement('li');
            const button = document.createElement('button');
            button.textContent = option;
            button.addEventListener('click', () => checkAnswer(option, question.correct_answer));
            li.appendChild(button);
            optionsElement.appendChild(li);
        });
    }

    function resetOptions() {
        questionElement.textContent = '';
        optionsElement.innerHTML = '';
    }

    function checkAnswer(selectedAnswer, correctAnswer) {
        if (selectedAnswer === correctAnswer) {
            score++;
            scoreElement.textContent = score;
        }
        currentQuestionIndex++;
        nextQuestion();
    }

    function endGame() {
        questionContainer.innerHTML = `<h2>Fim do Jogo!</h2><p>Pontuação Final: ${score}</p>`;
        nextButton.style.display = 'none';
    }

    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }
});
