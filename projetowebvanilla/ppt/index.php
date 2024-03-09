<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pedra, Papel e Tesoura</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
        }

        h1 {
            color: #333;
        }

        #result {
            margin-bottom: 20px;
            font-size: 24px;
            font-weight: bold;
        }

        #player-choice, #computer-choice {
            margin-bottom: 20px;
            font-size: 20px;
            font-weight: bold;
        }

        #choices {
            display: flex;
            justify-content: center;
        }

        .choice-btn {
            padding: 10px 20px;
            margin: 0 10px;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        .choice-btn:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <h1>Pedra, Papel e Tesoura</h1>
    <div id="result"></div>
    <div id="player-choice"></div>
    <div id="computer-choice"></div>
    <div id="choices">
        <button class="choice-btn" onclick="playGame('rock')">Pedra</button>
        <button class="choice-btn" onclick="playGame('paper')">Papel</button>
        <button class="choice-btn" onclick="playGame('scissors')">Tesoura</button>
    </div>

    <script>
        function playGame(playerChoice) {
            const choices = ['rock', 'paper', 'scissors'];
            const computerChoice = choices[Math.floor(Math.random() * 3)];

            document.getElementById('player-choice').innerText = 'Sua escolha: ' + playerChoice;
            document.getElementById('computer-choice').innerText = 'Escolha do computador: ' + computerChoice;

            if (playerChoice === computerChoice) {
                document.getElementById('result').innerText = 'Empate!';
            } else if (
                (playerChoice === 'rock' && computerChoice === 'scissors') ||
                (playerChoice === 'paper' && computerChoice === 'rock') ||
                (playerChoice === 'scissors' && computerChoice === 'paper')
            ) {
                document.getElementById('result').innerText = 'Você ganhou!';
            } else {
                document.getElementById('result').innerText = 'Você perdeu!';
            }
        }
    </script>
</body>
</html>
