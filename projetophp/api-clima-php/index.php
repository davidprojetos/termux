<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório do Tempo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f2f2f2;
        }

        .container {
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        h1 {
            text-align: center;
            color: #333;
        }

        form {
            text-align: center;
            margin-bottom: 20px;
        }

        label {
            font-weight: bold;
        }

        input[type="text"] {
            padding: 8px;
            margin: 0 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }

        button {
            padding: 8px 16px;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        button:hover {
            background-color: #0056b3;
        }

        p {
            margin-bottom: 10px;
        }

        strong {
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Relatório do Tempo para <?php echo isset($_GET['city']) ? $_GET['city'] : 'Londres'; ?></h1>
        <form action="" method="GET">
            <label for="city">Digite o nome da cidade:</label>
            <input type="text" id="city" name="city" value="<?php echo isset($_GET['city']) ? $_GET['city'] : 'Londres'; ?>" required>
            <button type="submit">Enviar</button>
        </form>
        <?php
        if (isset($_GET['city'])) {
            $city = $_GET['city'];
            $api_key = 'de10756b59947be0915623ac7f0236fc';
            $url = "http://api.openweathermap.org/data/2.5/weather?q=$city&appid=$api_key&lang=pt&units=metric";
            $response = file_get_contents($url);
            $data = json_decode($response, true);

            if (isset($data['main'])) {
                $temperature = $data['main']['temp'];
                $temp_max = $data['main']['temp_max'];
                $temp_min = $data['main']['temp_min'];
                $humidity = $data['main']['humidity'];
                $wind_speed = $data['wind']['speed'];
                $pressure = $data['main']['pressure'];
                $description = $data['weather'][0]['description'];
        ?>
                <p><strong>Temperatura Atual:</strong> <?php echo $temperature; ?> °C</p>
                <p><strong>Temperatura Máxima:</strong> <?php echo $temp_max; ?> °C</p>
                <p><strong>Temperatura Mínima:</strong> <?php echo $temp_min; ?> °C</p>
                <p><strong>Umidade:</strong> <?php echo $humidity; ?>%</p>
                <p><strong>Velocidade do Vento:</strong> <?php echo $wind_speed; ?> m/s</p>
                <p><strong>Pressão Atmosférica:</strong> <?php echo $pressure; ?> hPa</p>
                <p><strong>Descrição:</strong> <?php echo $description; ?></p>
        <?php
            } else {
                echo "<p>Não foi possível obter informações para a cidade $city. Por favor, verifique o nome da cidade e tente novamente.</p>";
            }
        }
        ?>
    </div>
</body>
</html>

