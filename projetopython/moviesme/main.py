import requests

url = "https://api.themoviedb.org/3/genre/movie/list"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiYWZjNTRmZjdjZTM3YzA3ODg0M2ExZDE1YTBlOGFkOCIsIm5iZiI6MTczMDYwMTE4My43NzM4MTEsInN1YiI6IjY3MjZkZWNlMTdkNzgyMjFlZGQ4OTU3YSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.zcg18ZPiBrsry3JPS7VmuFRVpduMr2d_cvcahyGMD8I"
}

response = requests.get(url, headers=headers)

print(response.text)

