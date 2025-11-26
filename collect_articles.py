import requests
import time
import csv
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
ALT_KEY = os.getenv("ALT_KEY")
URL = "https://newsdata.io/api/1/latest"
QUERY = "Trump"
MAX_ARTICLES = 500
OUTPUT_FILE = "data.csv"


def fetch_articles(api_key=ALT_KEY, querie=QUERY, max_articles=MAX_ARTICLES):
    articles = []
    seen = set()
    for query in queries:
        next_page = None
        while len(articles) < max_articles:
            params = {"apikey": api_key, "q": query, "language": "en"}
            if next_page:
                params["page"] = next_page
            try:
                response = requests.get(URL, params=params)
                response.raise_for_status()
                data = response.json()
                results = data.get("results", [])
                if not results:
                    break
                for result in results:
                    if len(articles) >= max_articles:
                        break
                    title = result.get("title", "")
                    if title in seen:
                        continue
                    seen.add(title)
                    articles.append(
                        {"title": title, "description": result.get("description", "")}
                    )
                print(f"Query '{query}': fetched total unique: {len(articles)}")
                next_page = data.get("nextPage")
                if not next_page:
                    break
                time.sleep(1)
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                break
    return articles


def save_data(articles, filename):
    if not articles:
        return
    with open(filename, "w", encoding="utf8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "description"])
        writer.writeheader()
        writer.writerows(articles)


def main():
    articles = fetch_articles()
    if articles:
        save_data(articles, OUTPUT_FILE)


if __name__ == "__main__":
    main()
