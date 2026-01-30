# modules/03_twitter.py
import pandas as pd
import hashlib
import re
from deep_translator import GoogleTranslator
import emoji
import tweepy

# ------------------------
# Utility Functions
# ------------------------

def hash_username(username):
    if pd.isna(username) or not username:
        return "anonymous"
    return hashlib.sha256(str(username).encode('utf-8')).hexdigest()


def clean_text(text):
    if pd.isna(text) or not text:
        return ""

    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = emoji.replace_emoji(text, replace='')
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def translate_text(text, source_lang='auto'):
    if not text:
        return text
    try:
        translator = GoogleTranslator(source=source_lang, target='en')
        return translator.translate(text)
    except Exception:
        return text

# ------------------------
# Twitter API Functions
# ------------------------

def init_twitter(bearer_token):
    return tweepy.Client(bearer_token=bearer_token)


def fetch_tweets(client, query, max_results=20):
    try:
        response = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=["created_at"]
        )

        tweet_list = []
        if response.data:
            for tweet in response.data:
                cleaned = clean_text(translate_text(tweet.text))
                tweet_list.append({
                    "source_type": "twitter",
                    "source_name": "X",
                    "text": cleaned,
                    "timestamp": str(tweet.created_at),
                    "author_hash": "api_user",
                    "likes": 0,
                    "retweets": 0,
                    "original_text": tweet.text[:200]
                })

        return tweet_list

    except Exception as e:
        print(f"[Twitter API Error] {e}")
        return []

# ------------------------
# Dataset Fallback
# ------------------------

def load_and_filter_tweets(dataset_path, query_text="", max_tweets=100):
    try:
        df = pd.read_csv(dataset_path)
    except Exception as e:
        print(f"Dataset load error: {e}")
        return []

    if query_text:
        keywords = query_text.lower().split()
        df = df[df['Text'].astype(str).str.lower().apply(
            lambda x: any(k in x for k in keywords)
        )]

    df = df.head(max_tweets)
    tweets = []

    for _, row in df.iterrows():
        cleaned = clean_text(translate_text(row['Text']))
        tweets.append({
            "source_type": "twitter",
            "source_name": "X",
            "text": cleaned,
            "timestamp": str(row.get('Timestamp', '')),
            "author_hash": hash_username(row.get('Username')),
            "likes": int(row.get('Likes', 0)),
            "retweets": int(row.get('Retweets', 0)),
            "original_text": row['Text'][:200]
        })

    return tweets

# ------------------------
# Unified Access Point
# ------------------------

def get_twitter_data(
    query_text,
    bearer_token=None,
    dataset_path='twitter_dataset.csv',
    max_api_results=20,
    max_dataset_results=50
):
    """
    Try Twitter API first.
    If API fails or returns no data → fallback to dataset.
    """

    tweets = []

    if bearer_token:
        print("Trying Twitter API...")
        client = init_twitter(bearer_token)
        tweets = fetch_tweets(client, query_text, max_api_results)

    if not tweets:
        print("Falling back to local Twitter dataset...")
        tweets = load_and_filter_tweets(
            dataset_path=dataset_path,
            query_text=query_text,
            max_tweets=max_dataset_results
        )

    return tweets
