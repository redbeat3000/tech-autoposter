"""Fetch trending tech headlines from NewsAPI."""
import os, requests

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

def fetch_news(topic: str) -> list[str]:
    res = requests.get("https://newsapi.org/v2/everything", params={
        "q": topic,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 6,
        "apiKey": NEWS_API_KEY,
    }, timeout=10)
    res.raise_for_status()
    articles = res.json().get("articles", [])
    return [
        f"- {a['title']} | {a['source']['name']} | {a.get('description', '')}"
        for a in articles if a.get("title")
    ]
