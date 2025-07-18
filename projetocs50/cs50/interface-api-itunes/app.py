from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

def buscar_musicas(termo):
    limit = 10
    response = requests.get(f"https://itunes.apple.com/search?entity=song&limit={limit}&term={termo}")

    if response.status_code == 200:
        data = json.loads(response.text)
        return data.get('results', [])
    else:
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = []

    if request.method == 'POST':
        termo_de_pesquisa = request.form['termo']
        resultados = buscar_musicas(termo_de_pesquisa)
    
    return render_template('index.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)
