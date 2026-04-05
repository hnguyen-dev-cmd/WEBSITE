import requests
from bs4 import BeautifulSoup

def get_tcg_news():
    url = "https://www.pokebeach.com/"
    # We pretend to be a browser so we don't get blocked
    headers = {'User-Agent': 'Mozilla/5.0'} 
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This finds the titles of the latest posts
        news_items = []
        for post in soup.find_all('h2', limit=5):
            news_items.append(post.text.strip())
        
        return news_items
    except:
        return ["Error: Could not reach source."]

# Test it
print("Hunting for news...")
print(get_tcg_news())