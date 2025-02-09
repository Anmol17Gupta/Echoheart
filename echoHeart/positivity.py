import requests

def get_motivational_quote():
    """Fetch a motivational quote from ZenQuotes API."""
    url = "https://zenquotes.io/api/random"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"{data[0]['q']} - {data[0]['a']}"
    else:
        return "Keep going, you are doing great! 😊"

def get_affirmation():
    """Fetch a positive affirmation from Affirmations API."""
    url = "https://www.affirmations.dev"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['affirmation']
    else:
        return "You are capable of amazing things! 💪"

def get_positivity(sentiment):
    """Return an affirmation for sad sentiment, otherwise return a motivational quote."""
    if sentiment == "sad":
        return get_affirmation()
    else:
        return get_motivational_quote()
