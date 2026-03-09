"""Post article to Blogger via Google API."""
import os, requests

BLOGGER_TOKEN  = os.environ.get("BLOGGER_TOKEN")   # OAuth2 access token
BLOGGER_BLOG_ID = os.environ.get("BLOGGER_BLOG_ID") # Your blog ID from Blogger settings

def post_blogger(article: dict) -> str:
    res = requests.post(
        f"https://www.googleapis.com/blogger/v3/blogs/{BLOGGER_BLOG_ID}/posts",
        headers={"Authorization": f"Bearer {BLOGGER_TOKEN}", "Content-Type": "application/json"},
        json={
            "title": article["title"],
            "content": article.get("html_content", f"<p>{article['content']}</p>"),
            "labels": article.get("tags", ["Technology"]),
        },
        timeout=15,
    )
    res.raise_for_status()
    return res.json().get("url", "posted")
