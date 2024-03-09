import requests

response = requests.get("http://0.0.0.0:8000/")
print(response.json())
