import requests
import datetime

FASTAPI_URL = "http://localhost:8000/analyze"
ELASTIC_URL = "http://localhost:9200/sentiment-logs/_doc"

def analyze_and_send(text):
    # 1. Appel à l'API FastAPI
    response = requests.post(FASTAPI_URL, json={"text": text})
    result = response.json()

    # 2. Ajouter un timestamp @timestamp en UTC ISO format
    result["@timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"

    # 3. Envoi à Elasticsearch avec authentification (modifie le mdp)
    es_response = requests.post(
        ELASTIC_URL,
        json=result,
        auth=('elastic', 'elastic')
    )
    
    print(f"Sent to Elasticsearch: {es_response.status_code} - {es_response.text}")

if __name__ == "__main__":
    texts = [
        "I love the new design!",
        "This is terrible.",
        "I think it's okay, not great, not bad."
    ]

    for text in texts:
        analyze_and_send(text)
