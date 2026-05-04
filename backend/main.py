from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "YOUR_API_KEY_HERE"  # replace if needed

@app.get("/")
def home():
    return {"status": "working"}

@app.get("/search")
def search_news(query: str):

    from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    url = f"https://newsapi.org/v2/everything?q={query}&language=en&from={from_date}&sortBy=publishedAt&apiKey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    articles = data.get("articles", [])[:10]

    results = []

    for article in articles:
        results.append({
            "title": article.get("title", ""),
            "description": article.get("description", "") or "",
            "source": article["source"]["name"],
            "url": article["url"],
            "sentiment": "Neutral"
        })

    return {"results": results}