# main.py
from modules.mod06_pipeline import run_pipeline
from dotenv import load_dotenv
import os

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TWITTER_BEARER = os.getenv("TWITTER_BEARER")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

df = run_pipeline(NEWS_API_KEY, TWITTER_BEARER, YOUTUBE_API_KEY)
print(df.head())
