from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route('/news', methods=['POST'])
def get_news():
    data = request.json
    topics = data.get('topics', [])
    articles = fetch_articles(topics)
    return jsonify(articles)

def fetch_articles(topics):
    articles = []
    for topic in topics:
        url = f"https://news.google.com/search?q={topic}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for item in soup.find_all('article'):
            title = item.find('h3').text if item.find('h3') else 'No title'
            link = item.find('a')['href'] if item.find('a') else 'No link'
            sentiment = analyze_sentiment(title)
            articles.append({'title': title, 'link': link, 'sentiment': sentiment})
    return articles

def analyze_sentiment(text):
    doc = nlp(text)
    sentiment = doc.sentiment
    return sentiment

if __name__ == '__main__':
    app.run(debug=True)
