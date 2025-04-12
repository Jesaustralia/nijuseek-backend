from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import random
import urllib.parse

app = Flask(__name__)
CORS(app)

# Simulated user agents for scraping
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
]

# Headers to use in scraping
def get_headers():
    return {
        "User-Agent": random.choice(user_agents)
    }

# Basic keyword seed per country (can be enhanced)
country_seeds = {
    "germany": "beste tipps", 
    "poland": "najlepszy sposób", 
    "portugal": "melhor maneira", 
    "denmark": "bedste metode", 
    "usa": "best way to", 
    "netherlands": "beste manier"
}

def generate_keywords_from_seed(seed):
    try:
        query = urllib.parse.quote(seed)
        url = f"https://www.google.com/search?q={query}&hl=en"
        res = requests.get(url, headers=get_headers(), timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        suggestions = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')
        keywords = [s.text for s in suggestions if len(s.text.split()) > 2 and not s.text.startswith("https")]
        unique_keywords = list(dict.fromkeys(keywords))
        return unique_keywords[:10] if unique_keywords else ["No keywords found."]
    except Exception as e:
        return [f"Error: {str(e)}"]

@app.route('/get_keywords', methods=['GET'])
def get_keywords():
    country = request.args.get('country', '').lower()
    seed = country_seeds.get(country, 'popular search')
    keywords = generate_keywords_from_seed(seed)
    random.shuffle(keywords)
    return jsonify({"country": country, "keywords": keywords})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)