from dotenv import load_dotenv
import os

load_dotenv()
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

def get_technology_news():
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': NEWS_API_KEY,
        'category': 'technology',
        'language': 'en',
        'pageSize': 2  # Get the top 2 news stories
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error fetching news: {response.status_code}")
        print(response.text)
        return None

    data = response.json()
    if data['articles']:
        news_texts = []
        for article in data['articles']:
            news_texts.append(f"Title: {article['title']}\nDescription: {article['description']}")
        return " ".join(news_texts)
    else:
        print("No news found.")
        return None