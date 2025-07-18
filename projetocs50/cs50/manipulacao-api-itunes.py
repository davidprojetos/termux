import requests
import json

# Defina o número desejado de resultados no parâmetro 'limit'
limit = 5
search = str(input("Digite algo para ser pesquisado no itunes: "))
response = requests.get(f"https://itunes.apple.com/search?entity=song&limit={limit}&term={search}")

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    # Converte a resposta para um objeto Python
    data = json.loads(response.text)

    # Acesse os dados específicos conforme necessário
    if 'results' in data and data['results']:
        for result in data['results']:
            track_name = result.get('trackName', 'N/A')
            artist_name = result.get('artistName', 'N/A')
            artwork_url = result.get('artworkUrl100')  # URL da arte do álbum
            preview_url = result.get('previewUrl')  # URL do trailer da música

            print(f"Nome da música: {track_name}")
            print(f"Nome do artista: {artist_name}")
            print(f"Link da arte do álbum: {artwork_url}")
            print(f"Link do trailer da música: {preview_url}")
            print("------")
    else:
        print("Nenhum resultado encontrado.")
else:
    print(f"Erro na requisição: {response.status_code}")