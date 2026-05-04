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

API_KEY = "4234ada308d3402884a1f83608eec617"

# 🔥 simple sentiment function
def get_sentiment(text):
    text = text.lower()

    positive_words = ["gain", "growth", "profit", "rise", "surge", "up", "bull", "record"]
    negative_words = ["loss", "drop", "fall", "decline", "down", "bear", "crash"]

    score = 0

    for word in positive_words:
        if word in text:
            score += 1

    for word in negative_words:
        if word in text:
            score -= 1

    if score > 0:
        return "Bullish"
    elif score < 0:
        return "Bearish"
    else:
        return "Neutral"

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
        title = article.get("title", "")
        description = article.get("description", "") or ""

        full_text = f"{title} {description}"

        sentiment = get_sentiment(full_text)

        results.append({
            "title": title,
            "description": description,
            "source": article["source"]["name"],
            "url": article["url"],
            "sentiment": sentiment
        })

    return {"results": results}