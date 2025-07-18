import requests, json

term = str(input("Digite sua busca musical: ").strip())
response = requests.get("https://itunes.apple.com/search?entity=song&limit=1&term=" + "{term}")
response = json.dumps(response.json())
print(response)