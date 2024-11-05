import requests

BASE = "http://127.0.0.1:5000/"

response1 = requests.get(BASE + "driver/Hamilton")

response2 = requests.get(BASE + "constructor/" + response1.json().get("driver").get("team"))

print(response1.json())
print(response2.json())

