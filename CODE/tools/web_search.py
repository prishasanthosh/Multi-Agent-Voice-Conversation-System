import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

class WebSearchTool:
    def search_serper(self, query: str) -> str:
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": SERPER_API_KEY}
        payload = {"q": query}
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=10)
            res.raise_for_status()
            results = res.json().get("organic", [])
            return "\n".join(f"- {r['title']}: {r['link']}" for r in results[:3]) or "No results found."
        except Exception as e:
            return f"[Serper error] {e}"

    def search_newsapi(self, query: str) -> str:
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            articles = res.json().get("articles", [])
            return "\n".join(f"- {a['title']} ({a['source']['name']})" for a in articles[:3]) or "No news found."
        except Exception as e:
            return f"[NewsAPI error] {e}"

    def invoke(self, query: str, source: str = "serper") -> str:
        if source == "news":
            return self.search_newsapi(query)
        return self.search_serper(query)
