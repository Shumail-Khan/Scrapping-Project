# modules/03_twitter.py
import pandas as pd
import hashlib
import re
from deep_translator import GoogleTranslator  # pip install deep-translator
import emoji  # pip install emoji (optional but recommended)

def hash_username(username):
    """Hash username for privacy using SHA-256"""
    if pd.isna(username) or not username:
        return "anonymous"
    return hashlib.sha256(str(username).encode('utf-8')).hexdigest()


def clean_text(text):
    """
    Clean tweet text - this version combines your pipeline clean_text 
    with additional improvements
    """
    if pd.isna(text) or not text:
        return ""
    
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)          # remove urls
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)                   # remove special chars
    text = emoji.replace_emoji(text, replace='')                 # remove emojis
    text = re.sub(r'\s+', ' ', text).strip()                     # normalize spaces
    
    return text


def translate_text(text, source_lang='auto'):
    """Optional translation to English using deep-translator"""
    if not text:
        return text
    try:
        translator = GoogleTranslator(source=source_lang, target='en')
        translated = translator.translate(text)
        return translated if translated else text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text


def load_and_filter_tweets(dataset_path='twitter_dataset.csv', query_text="", max_tweets=100):
    """
    Load the local twitter dataset and filter tweets relevant to the query
    Returns list of processed tweet dictionaries
    """
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        print(f"Dataset not found: {dataset_path}")
        return []
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []

    if df.empty:
        return []

    # Basic keyword filtering
    if query_text:
        keywords = [k.lower().strip() for k in query_text.split() if k.strip()]
        if keywords:
            # Match if ANY keyword is present
            mask = df['Text'].astype(str).str.lower().apply(
                lambda x: any(kw in x for kw in keywords)
            )
            df = df[mask]

    # Limit results
    df = df.head(max_tweets)

    # Process each tweet
    tweet_list = []
    for _, row in df.iterrows():
        original_text = row['Text']
        
        # Optional: translate (most seem English, so this might not do much)
        cleaned_translated = translate_text(original_text)
        cleaned = clean_text(cleaned_translated)
        
        tweet_data = {
            "source_type": "twitter",
            "source_name": "X",
            "text": cleaned,
            "timestamp": str(row['Timestamp']),
            "author_hash": hash_username(row['Username']),
            "likes": int(row.get('Likes', 0)),
            "retweets": int(row.get('Retweets', 0)),
            "original_text": original_text[:200] + "..." if len(original_text) > 200 else original_text
        }
        tweet_list.append(tweet_data)

    print(f"Loaded & filtered {len(tweet_list)} tweets for query: '{query_text}'")
    return tweet_list

# Api Key Code
# import tweepy

# def init_twitter(bearer_token):
#     client = tweepy.Client(bearer_token=bearer_token)
#     return client

# def fetch_tweets(client, query, max_results=10):  # lower max_results
#     try:
#         tweets = client.search_recent_tweets(query=query, max_results=max_results)
#         tweet_list = []
#         if tweets.data:
#             for tweet in tweets.data:
#                 tweet_list.append({
#                     "source_type": "twitter",
#                     "source_name": "X",
#                     "text": tweet.text,
#                     "timestamp": tweet.created_at
#                 })
#         return tweet_list
#     except Exception as e:
#         print(f"Twitter API error: {e}")
#         return []

