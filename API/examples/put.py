import requests


BASE = "https://127.0.0.1:5000/" # Base URL of the api.


response = requests.put(BASE_URL + "search/" + "26", {"id": 26,"reason":"26 is such a little troller smh"})
# ^ Data ^

print(response.json()) # Prints the response