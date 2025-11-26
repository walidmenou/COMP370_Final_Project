import requests
import time
import csv
import os
from dotenv import load_dotenv

load_dotenv()

API_KEYS = [os.getenv("KEY1"), os.getenv("KEY2")]
URL = "https://newsdata.io/api/1/latest"
QUERY = "Trump"
MAX_ARTICLES = 500
OUTPUT_FILE = "data.csv"


def get_unique_articles(seen, results):
    articles = []
    for result in results:
        title = result.get("title", "")
        if title in seen:
            continue
        seen.add(title)

        articles.append({"title": title, "description": result.get("description", "")})

    return articles


def fetch_articles(api_keys=API_KEYS, query=QUERY, max_articles=MAX_ARTICLES):
    articles = []
    seen = set()
    key_index = 0
    next_page = None

    while len(articles) < max_articles:
        params = {"apikey": api_keys[key_index], "q": query, "language": "en"}
        if next_page:
            params["page"] = next_page
        try:
            response = requests.get(URL, params=params)

            if response.status_code == 429 and key_index < len(api_keys) - 1:
                key_index += 1
                params["apikey"] = api_keys[key_index]
                response = requests.get(URL, params=params)

            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])

            if not results:
                break

            unique_articles = get_unique_articles(seen, results)
            articles.extend(unique_articles[: max_articles - len(articles)])

            print(f"Total : {len(articles)}")

            next_page = data.get("nextPage")
            if not next_page:
                break

            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            break
        except Exception as e:
            print(f"Unknown error: {e}")

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
