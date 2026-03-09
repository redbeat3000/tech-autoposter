"""Generate a full blog article using Gemini 2.0 Flash (free)."""
import os, json
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def write_article(topic: str, headlines: list[str]) -> dict:
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""You are an expert tech journalist writing for a broad developer audience.

Based on these recent headlines about "{topic}", write a compelling blog article.

HEADLINES:
{chr(10).join(headlines)}

Requirements:
- 700-900 words
- Strong opening hook
- 3-4 sections with ## subheadings
- Include real analysis, not just summaries
- End with a forward-looking conclusion
- Conversational but professional tone

Return ONLY a raw JSON object (no markdown fences, no extra text):
{{
  "title": "Catchy SEO-friendly title",
  "subtitle": "One sentence description",
  "content": "Full article in markdown",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "html_content": "Full article in HTML (use <h2>, <p>, <strong> tags)"
}}"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip().rstrip("```").strip()
    return json.loads(text)
