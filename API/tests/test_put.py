import requests


BASE_URL = "http://127.0.0.1:5000/"


response = requests.put(BASE_URL + "search/" + "26", {"id": 26,"reason":"26 is such a little troller smh"})
print(response.json())