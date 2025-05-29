from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from elasticsearch import Elasticsearch
from datetime import datetime
es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "elastic"))

analyzer = SentimentIntensityAnalyzer()

with open("log.txt", "r") as file:
    for line in file:
        sentiment = analyzer.polarity_scores(line)

        if sentiment["compound"] > 0.05:
            label = "positive"
        elif sentiment["compound"] < -0.05:
            label = "negative"
        else:
            label = "neutral"

        doc = {
            "message": line.strip(),
            "sentiment_score": sentiment["compound"],
            "sentiment_label": label,
            "@timestamp": datetime.now().isoformat() 
        }

        es.index(index="sentiment-logs", document=doc)
        
