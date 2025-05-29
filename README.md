# sentiment-elk-project

# 📊 ELK Stack + Sentiment Analysis Integration

Ce projet montre comment installer et configurer la stack **ELK (Elasticsearch, Logstash, Kibana)** sur une VM Linux, intégrer une **API d’analyse de sentiment** en anglais avec **FastAPI** et **VADER**, et envoyer les résultats à **Elasticsearch**, avec visualisation via **Kibana**.

---

# 📊 Intégration ELK Stack avec Analyse de Sentiment (VADER)

Ce projet montre comment :

- Installer la stack ELK (Elasticsearch, Logstash, Kibana) sur une VM Linux.
- Sécuriser Kibana par authentification (login/pwd) .
- Analyser le sentiment d’un texte en anglais via VADER et Fast Api.
- Intégrer les résultats dans Elasticsearch.
- Visualiser les résultats avec Kibana.

---

## ⚙️ Étapes d'installation ELK sur une VM Linux

### 🖥️ 1. Créer une VM Linux

- Installer **VirtualBox**
- Télécharger Ubuntu 
- Créer une machine virtuelle avec 8Go RAM minimum et accès internet

### 📥 2. Installer Java

sudo apt update
sudo apt install openjdk-17-jdk -y

### 📥 3. Installer ,Configurer et Lancer Elasticsarch

wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.13.4-amd64.deb
sudo dpkg -i elasticsearch-8.13.4-amd64.deb

network.host: 0.0.0.0
xpack.security.enabled: true

sudo systemctl start elasticsearch
sudo systemctl enable elasticsearch
Créer les mots de passe :
sudo /usr/share/elasticsearch/bin/elasticsearch-setup-passwords interactive

### 📥 4. Installer ,Configurer et Lancer Kibana
wget https://artifacts.elastic.co/downloads/kibana/kibana-8.13.4-amd64.deb
sudo dpkg -i kibana-8.13.4-amd64.deb
server.host: "0.0.0.0"

elasticsearch.username: "*****"
elasticsearch.password: "*****"


sudo systemctl start kibana
sudo systemctl enable kibana

### 📥 5. Integration de fonctionnalité de classification des sentiments en anglais 


💬 Méthode 1 : Traitement de sentiment via fichier texte
📄 Fichier : sentiment_logger.py
Ce script lit un fichier texte (log.txt), analyse chaque ligne avec VADER, puis envoie chaque résultat vers Elasticsearch dans l’index sentiment-logs.

🔧 Comment ça fonctionne
Charge le modèle SentimentIntensityAnalyzer de VADER.

Parcourt chaque ligne du fichier.

Calcule le score compound (entre -1 et 1).

Classe le texte comme :

positive si score > 0.05

negative si score < -0.05

neutral sinon

Formate un document JSON avec :

le texte original

le score

le label (sentiment)

un timestamp

Envoie le document à Elasticsearch via la bibliothèque elasticsearch.

python sentiment_logger.py

🚀 Méthode 2 : Traitement de sentiment via API FastAPI

🧠 1. API de classification
📁 Fichier : sentiment-logger-api.py
Cette API FastAPI expose une route POST /analyze qui reçoit un texte, l’analyse avec VADER et retourne le sentiment.

uvicorn sentiment-logger-api:app --reload

POST /analyze
{
  "text": "I love this product!"
}

Réponse :

{
  "text": "I love this product!",
  "sentiment": "positive",
  "scores": {
    "neg": 0.0,
    "neu": 0.45,
    "pos": 0.55,
    "compound": 0.6369
  }
}

✉️ 2. Envoi des résultats vers ELK
📁 Fichier : send-to-elk.py
Ce script envoie une liste de textes vers l’API FastAPI pour analyse, puis publie les résultats vers Elasticsearch dans l’index sentiment-logs.

🔧 Étapes :
Pour chaque texte :

Envoie à localhost:8000/analyze

Récupère la réponse JSON

Ajoute un champ @timestamp

Envoie vers Elasticsearch avec auth=(elastic, mot_de_passe)
python send-to-elk.py

📈 Visualisation dans Kibana
http://localhost:5601






