"""Post article to WordPress.com via REST API."""
import os, requests

WP_TOKEN   = os.environ.get("WP_TOKEN")    # OAuth token from developer.wordpress.com
WP_SITE_ID = os.environ.get("WP_SITE_ID")  # Your site ID or domain e.g. yourblog.wordpress.com

def post_wordpress(article: dict) -> str:
    res = requests.post(
        f"https://public-api.wordpress.com/rest/v1.1/sites/{WP_SITE_ID}/posts/new",
        headers={"Authorization": f"Bearer {WP_TOKEN}", "Content-Type": "application/json"},
        json={
            "title": article["title"],
            "content": article.get("html_content", article["content"]),
            "excerpt": article.get("subtitle", ""),
            "tags": ",".join(article.get("tags", ["technology"])),
            "status": "publish",
            "format": "standard",
        },
        timeout=15,
    )
    res.raise_for_status()
    return res.json().get("URL", "posted")
