import requests
from requests.auth import HTTPBasicAuth

consumer_key = "ck_2aa5a27ace2c00b3ca3878b26782c4348bfe10c1"
consumer_secret = "cs_78ab0cd475b274782f1f6f76fa90bd134417ff75"

url = "https://computia.me/wp-json/wc/v3/orders"

response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

print(response.json()[0])
