# Multi-Platform Auto-Poster

Posts 3 full tech articles per day across 5 platforms simultaneously.
**15 articles published daily. 100% free.**

---

## Platforms
| Platform | What gets posted |
|---|---|
| Dev.to | Full article (markdown) |
| Hashnode | Full article (markdown) |
| WordPress.com | Full article (HTML) |
| Blogger | Full article (HTML) |
| Tumblr | Full article (HTML) |

## Schedule (EAT)
- 8:00 AM — morning post
- 1:00 PM — afternoon post
- 7:00 PM — evening post

---

## Setup

### Step 1 — Get your free API keys

**Gemini (AI writer)**
→ aistudio.google.com → Get API Key → free, no billing

**NewsAPI (news source)**
→ newsapi.org → Register → free tier (100 req/day, you use 9)

**Dev.to**
→ dev.to/settings/extensions → "DEV Community API Keys" → New Key

**Hashnode**
→ hashnode.com → top-right avatar → Account Settings → Developer → Personal Access Token
→ Also note your Publication ID from your blog's dashboard URL

**WordPress.com**
→ developer.wordpress.com/apps → Create new app → OAuth2 token
→ Your site ID = yourblog.wordpress.com (or find numeric ID in settings)

**Blogger**
→ console.cloud.google.com → Create project → Enable Blogger API
→ OAuth2 credentials → get access token
→ Blogger blog ID = the number in your Blogger dashboard URL

**Tumblr**
→ api.tumblr.com/console/calls/user/info → Register app
→ You need: consumer key, consumer secret, OAuth token, OAuth token secret

---

### Step 2 — Push to GitHub

```bash
git init
git add .
git commit -m "init"
git remote add origin https://github.com/YOUR_USERNAME/autoposter
git push -u origin main
```

### Step 3 — Add GitHub Secrets

Go to repo → Settings → Secrets and variables → Actions → New repository secret

Add all of these:

```
GEMINI_API_KEY
NEWS_API_KEY
DEVTO_API_KEY
HASHNODE_TOKEN
HASHNODE_PUB_ID
WP_TOKEN
WP_SITE_ID
BLOGGER_TOKEN
BLOGGER_BLOG_ID
TUMBLR_BLOG             (e.g. yourblog.tumblr.com)
TUMBLR_CONSUMER_KEY
TUMBLR_CONSUMER_SECRET
TUMBLR_TOKEN
TUMBLR_TOKEN_SECRET
```

### Step 4 — Done
GitHub Actions runs automatically 3x daily. You can also trigger manually
from the Actions tab → "Multi-Platform Auto-Poster" → Run workflow.

---

## Test Locally

```bash
pip install -r requirements.txt

# Set all env vars then:
python main.py 0   # morning
python main.py 1   # afternoon
python main.py 2   # evening
```

## File Structure

```
autoposter/
├── main.py                          # Orchestrator
├── requirements.txt
├── utils/
│   ├── news.py                      # NewsAPI fetcher
│   └── writer.py                    # Gemini article writer
├── publishers/
│   ├── devto.py
│   ├── hashnode.py
│   ├── wordpress.py
│   ├── blogger.py
│   └── tumblr.py
└── .github/workflows/
    └── post.yml                     # 3x daily scheduler
```

## Notes
- Blogger and WordPress tokens expire. For long-term use, set up a refresh token flow.
- Tumblr is the most complex to set up (4 OAuth credentials) but works reliably once connected.
- Dev.to and Hashnode are the easiest — single token, never expires.
- If a platform fails, the others still post. Failures are logged in GitHub Actions.
