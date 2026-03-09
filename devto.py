"""Post article to Dev.to via REST API."""
import os, requests

DEVTO_API_KEY = os.environ.get("DEVTO_API_KEY")

def post_devto(article: dict) -> str:
    res = requests.post(
        "https://dev.to/api/articles",
        headers={"api-key": DEVTO_API_KEY, "Content-Type": "application/json"},
        json={
            "article": {
                "title": article["title"],
                "body_markdown": f"*{article.get('subtitle', '')}*\n\n{article['content']}",
                "tags": article.get("tags", ["technology"])[:4],
                "published": True,
            }
        },
        timeout=15,
    )
    res.raise_for_status()
    return res.json().get("url", "posted")
