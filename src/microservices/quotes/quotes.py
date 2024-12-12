import requests
from flask import Flask, jsonify
from random import choice

app = Flask(__name__)

# API configuration
API_URL = "https://the-one-api.dev/v2"
API_HEADERS = {"Authorization": "Bearer ZDkfuPdJGtH3Tg9AZNQK"}

def fetch_random_quote():
    """
    Fetches a random quote from the-one-api.dev and the character who said it.
    Returns a dictionary ['quote': 'character'].
    """
    try:
        # Fetch quotes
        quote_response = requests.get(
            f"{API_URL}/quote",
            headers=API_HEADERS
        )
        
        quotes = quote_response.json()["docs"]
            
        # Select a random quote from the list
        quote = choice(quotes)
            
        # Fetch character details
        character_response = requests.get(
            f"{API_URL}/character/{quote['character']}",
            headers=API_HEADERS
        )

        character = character_response.json()["docs"][0]["name"]
        
        return {
            "quote": quote["dialog"],
            "character": character
        }
        
    except Exception as e:
        return {
            "quote": "There's some good in this world, Mr. Frodo, and it's worth fighting for.",
            "character": "Samwise Gamgee (fallback)"
        }

@app.route("/lotrQuote")
def get_quote():
    """API endpoint that returns a random LOTR quote with the character who said it."""
    quote = fetch_random_quote()
    print(f"{quote}")
    return jsonify(quote)

if __name__ == "__main__":
    app.run(port=2001)
