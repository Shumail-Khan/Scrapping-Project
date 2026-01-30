# modules/02_news.py
import requests
from deep_translator import GoogleTranslator
from modules.mod05_normalization import clean_text

def fetch_news_newsapi(query, api_key, max_articles=10):
    """
    Fetch news articles using NewsAPI for a given query.
    Extracts:
        - Headline
        - Article body
        - Source name
        - Timestamp
        - Language
    Returns a list of dictionaries.
    """
    url = f'https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&pageSize={max_articles}&apiKey={api_key}'
    response = requests.get(url).json()
    articles = []

    for article in response.get("articles", []):
        headline = article.get("title", "")
        body = article.get("description", "") or ""
        lang = article.get("language", "en")  # default to English if not available

        # Combine headline + body
        text_raw = f"{headline} {body}".strip()

        # Translate if not English
        if lang != "en":
            text_translated = translate_text(text_raw)
        else:
            text_translated = text_raw

        # Clean text
        text_cleaned = clean_text(text_translated)

        articles.append({
            "source_type": "news",
            "source_name": article["source"]["name"],
            "headline": clean_text(headline),
            "body": clean_text(body),
            "text": text_cleaned,   # combined cleaned text
            "timestamp": article.get("publishedAt"),
            "language": lang
        })

    return articles

def translate_text(text, src_lang='auto', target_lang='en'):
    """
    Translate text to English using Deep Translator
    """
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text
