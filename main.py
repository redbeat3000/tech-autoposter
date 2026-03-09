"""
Multi-Platform Auto-Poster
Posts full articles to: Dev.to, Hashnode, WordPress.com, Blogger, Tumblr
3x daily via GitHub Actions | Powered by Gemini 1.5 Flash (free)
"""

import os, json, sys
from datetime import datetime
from utils.news import fetch_news
from utils.writer import write_article
from publishers.devto import post_devto
from publishers.hashnode import post_hashnode
from publishers.wordpress import post_wordpress
from publishers.blogger import post_blogger
from publishers.tumblr import post_tumblr

# ── Topic rotation (3 posts/day = morning, afternoon, evening) ───────────────
TOPICS = [
    "artificial intelligence breakthroughs",
    "cybersecurity and hacking news",
    "Web3 and blockchain developments",
    "cloud computing and DevOps",
    "open source software releases",
    "IoT and embedded systems",
    "developer tools and frameworks",
    "tech startup and funding news",
    "quantum computing research",
    "semiconductor and chip industry",
    "machine learning and data science",
    "mobile and app development",
    "AR VR and spatial computing",
    "robotics and automation",
    "green tech and sustainable computing",
]

SLOTS = {0: "morning", 1: "afternoon", 2: "evening"}

def pick_topic(slot: int) -> str:
    day = datetime.now().timetuple().tm_yday
    return TOPICS[(day * 3 + slot) % len(TOPICS)]

def run(slot: int = 0):
    topic = pick_topic(slot)
    label = SLOTS.get(slot, "post")

    print(f"\n{'='*55}")
    print(f" Auto-Poster | {datetime.now().strftime('%Y-%m-%d %H:%M')} | {label.upper()}")
    print(f" Topic: {topic}")
    print(f"{'='*55}\n")

    # 1. Fetch news
    news = fetch_news(topic)
    print(f"[news]      {len(news)} headlines fetched")

    # 2. Write article
    article = write_article(topic, news)
    print(f"[gemini]    Article: '{article['title']}'")

    # 3. Post to all platforms
    results = {}

    try:
        url = post_devto(article)
        results["Dev.to"] = url
        print(f"[dev.to]    {url}")
    except Exception as e:
        results["Dev.to"] = f"FAILED: {e}"
        print(f"[dev.to]    FAILED: {e}")

    try:
        url = post_hashnode(article)
        results["Hashnode"] = url
        print(f"[hashnode]  {url}")
    except Exception as e:
        results["Hashnode"] = f"FAILED: {e}"
        print(f"[hashnode]  FAILED: {e}")

    try:
        url = post_wordpress(article)
        results["WordPress"] = url
        print(f"[wordpress] {url}")
    except Exception as e:
        results["WordPress"] = f"FAILED: {e}"
        print(f"[wordpress] FAILED: {e}")

    try:
        url = post_blogger(article)
        results["Blogger"] = url
        print(f"[blogger]   {url}")
    except Exception as e:
        results["Blogger"] = f"FAILED: {e}"
        print(f"[blogger]   FAILED: {e}")

    try:
        url = post_tumblr(article)
        results["Tumblr"] = url
        print(f"[tumblr]    {url}")
    except Exception as e:
        results["Tumblr"] = f"FAILED: {e}"
        print(f"[tumblr]    FAILED: {e}")

    # Summary
    success = sum(1 for v in results.values() if not v.startswith("FAILED"))
    print(f"\n Done: {success}/5 platforms posted successfully.\n")
    return results

if __name__ == "__main__":
    slot = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    run(slot)
