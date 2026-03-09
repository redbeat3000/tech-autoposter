"""Post article to Tumblr via REST API v2."""
import os, requests
from requests_oauthlib import OAuth1

TUMBLR_BLOG       = os.environ.get("TUMBLR_BLOG")          # yourblog.tumblr.com
TUMBLR_CONSUMER_KEY    = os.environ.get("TUMBLR_CONSUMER_KEY")
TUMBLR_CONSUMER_SECRET = os.environ.get("TUMBLR_CONSUMER_SECRET")
TUMBLR_TOKEN      = os.environ.get("TUMBLR_TOKEN")
TUMBLR_TOKEN_SECRET    = os.environ.get("TUMBLR_TOKEN_SECRET")

def post_tumblr(article: dict) -> str:
    auth = OAuth1(
        TUMBLR_CONSUMER_KEY, TUMBLR_CONSUMER_SECRET,
        TUMBLR_TOKEN, TUMBLR_TOKEN_SECRET
    )

    body = article.get("html_content", article["content"])
    full_html = f"<h2>{article.get('subtitle', '')}</h2>{body}"

    res = requests.post(
        f"https://api.tumblr.com/v2/blog/{TUMBLR_BLOG}/post",
        auth=auth,
        json={
            "type": "text",
            "title": article["title"],
            "body": full_html,
            "tags": article.get("tags", ["technology"]),
            "format": "html",
            "state": "published",
        },
        timeout=15,
    )
    res.raise_for_status()
    post_id = res.json().get("response", {}).get("id_string", "")
    return f"https://{TUMBLR_BLOG}/post/{post_id}"
