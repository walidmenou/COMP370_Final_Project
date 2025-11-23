import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://api.thenewsapi.com/v1/news/all"
api_key = os.getenv("API_KEY")
params = {"api_token": api_key, "search": "Zohran Mamdani", "language": "en"}

response = requests.get(url, params=params)
response.raise_for_status()
print(response.text)
