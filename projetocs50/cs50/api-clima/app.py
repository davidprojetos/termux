from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def weather_report():
    api_key = 'de10756b59947be0915623ac7f0236fc'
    city = request.args.get('city', 'Londres')  # Obter o nome da cidade da query string ou usar 'Londres' como padrão
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=pt&units=metric'  # Adiciona 'lang=pt' para exibir as informações em português e 'units=metric' para obter a temperatura em Celsius
    
    response = requests.get(url)
    data = response.json()
    
    # Verifica se a chave 'main' está presente no JSON
    if 'main' not in data:
        error_message = f"Não foi possível obter informações para a cidade {city}. Por favor, verifique o nome da cidade e tente novamente."
        return render_template('error.html', error_message=error_message)
    
    # Extrai os dados relevantes do JSON
    weather_data = {
        'city': city,
        'temperature': data['main']['temp'],
        'temp_max': data['main']['temp_max'],
        'temp_min': data['main']['temp_min'],
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed'],
        'pressure': data['main']['pressure'],
        'description': data['weather'][0]['description']
    }

    return render_template('weather_report.html', **weather_data)

if __name__ == '__main__':
    app.run(debug=True)
