"""Post article to Hashnode via GraphQL API."""
import os, requests

HASHNODE_TOKEN = os.environ.get("HASHNODE_TOKEN")
HASHNODE_PUB_ID = os.environ.get("HASHNODE_PUB_ID")  # Your publication/blog ID

def post_hashnode(article: dict) -> str:
    query = """
    mutation PublishPost($input: PublishPostInput!) {
      publishPost(input: $input) {
        post { url }
      }
    }"""

    variables = {
        "input": {
            "title": article["title"],
            "subtitle": article.get("subtitle", ""),
            "contentMarkdown": article["content"],
            "tags": [{"name": t, "slug": t.lower().replace(" ", "-")}
                     for t in article.get("tags", ["technology"])[:5]],
            "publicationId": HASHNODE_PUB_ID,
        }
    }

    res = requests.post(
        "https://gql.hashnode.com",
        headers={"Authorization": HASHNODE_TOKEN, "Content-Type": "application/json"},
        json={"query": query, "variables": variables},
        timeout=15,
    )
    res.raise_for_status()
    data = res.json()

    if "errors" in data:
        raise Exception(data["errors"][0]["message"])

    return data["data"]["publishPost"]["post"]["url"]
