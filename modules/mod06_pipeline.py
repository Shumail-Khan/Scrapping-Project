# modules/06_pipeline.py
import pandas as pd
from modules.mod01_queries import get_queries
from modules.mod02_news import fetch_news_newsapi, translate_text
# from modules.mod03_twitter import init_twitter, fetch_tweets
from modules.mod03_twitter import load_and_filter_tweets
from modules.mod04_youtube import init_youtube, fetch_youtube
from modules.mod05_normalization import clean_text

def run_pipeline(news_api_key, twitter_bearer, youtube_api_key):
    all_data = []
    queries = get_queries()
    
    # Initialize API clients
    # twitter_client = init_twitter(twitter_bearer)
    youtube_client = init_youtube(youtube_api_key)
    
    for q in queries:
        query_id = q["query_id"]
        query_text = q["query_text"]
        
        # ------------------
        # News
        # ------------------
        news_data = fetch_news_newsapi(query_text, news_api_key)
        for d in news_data:
            d["query_id"] = query_id
            d["text"] = clean_text(d["text"])  # ensure clean text
        all_data.extend(news_data)
        
        # ------------------
        # Twitter
        # ------------------
        # tweets = fetch_tweets(twitter_client, query_text)
        # for d in tweets:
        #     d["query_id"] = query_id
        #     # Translate non-English tweets and clean
        #     d["text"] = clean_text(translate_text(d["text"]))
        # all_data.extend(tweets)
        tweets = load_and_filter_tweets(
            dataset_path='twitter_dataset.csv',      # adjust path if needed
            query_text=query_text,
            max_tweets=50                            # adjust as needed
        )

        for d in tweets:
            d["query_id"] = query_id
            # d["text"] = clean_text(d["text"]) # Text is already cleaned & translated in load_and_filter_tweets
            
        all_data.extend(tweets)
        
        
        # ------------------
        # YouTube
        # ------------------
        videos = fetch_youtube(youtube_client, query_text)
        for d in videos:
            d["query_id"] = query_id
            # Translate combined text if needed
            d["text"] = clean_text(translate_text(d["text"]))
            d["title"] = clean_text(d.get("title", ""))
            d["description"] = clean_text(d.get("description", ""))
            d["transcript"] = clean_text(d.get("transcript", ""))
        all_data.extend(videos)
    
    # ------------------
    # Save to CSV
    # ------------------
    df = pd.DataFrame(all_data)
    df.to_csv("multi_source_data_clean.csv", index=False)
    print("Data saved to multi_source_data_clean.csv")
    return df
