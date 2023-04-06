from transformers import pipeline
from fastapi import FastAPI, Request

app = FastAPI()

# Load sentiment analysis model
sentiment_classifier = pipeline(
    "sentiment-analysis",
    model="curiousily/alpaca-bitcoin-tweets-sentiment"
)
@app.post("/sentiment")
async def analyze_sentiment(request: Request):
    data = await request.json()
    title = data.get("title")
    text = data.get("text")
    id = data.get("id")
    ccsentiment = data.get("ccsentiment")
    result = sentiment_classifier("Title: " + title + " Text: " + text)[0]

    label = result["label"]
    if label == "NEGATIVE":
        score = -result["score"]
    else:
        score = result["score"]
    if label == "POSITIVE" and score < 0.5:
        label = "NEUTRAL"
    return {
        "label": label,
        "score": result["score"],
        "id": id,
        "ccsentiment": ccsentiment,
        "text": "Title: " + title + " Text: " + text
    }

