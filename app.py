from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random
import urllib.parse

app = Flask(__name__)
CORS(app)

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
]

def get_headers():
    return {
        "User-Agent": random.choice(user_agents)
    }

def fetch_keywords(seed):
    try:
        url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={urllib.parse.quote(seed)}"
        res = requests.get(url, headers=get_headers(), timeout=5)
        data = res.json()
        return data[1][:100]
    except Exception as e:
        return [f"Error: {str(e)}"]

@app.route('/get_keywords', methods=['GET'])
def get_keywords():
    country = request.args.get('country', '')
    base_keywords = {
        "denmark": "bedste metode",
        "usa": "best way to",
        "germany": "beste tipps",
        "poland": "najlepszy sposób",
        "portugal": "melhor maneira",
        "netherlands": "beste manier",
        "spain": "mejor manera",
        "turkey": "en iyi yol",
        "finland": "paras tapa",
        "romania": "cea mai bună metodă",
        "czech republic": "nejlepší způsob",
        "bulgaria": "най-добрият начин",
        "norway": "beste måte",
        "australia": "best way to",
        "uk": "best way to",
        "slovenia": "najboljši način"
    }
    seed = base_keywords.get(country.lower(), "best method")
    keywords = fetch_keywords(seed)
    return jsonify({"country": country, "keywords": keywords})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
