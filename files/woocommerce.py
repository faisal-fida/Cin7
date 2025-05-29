import requests
from requests.auth import HTTPBasicAuth

consumer_key = ""
consumer_secret = ""

url = "https://computia.me/wp-json/wc/v3/orders"

response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

print(response.json()[0])
