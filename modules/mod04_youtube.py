# modules/04_youtube.py
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from modules.mod05_normalization import clean_text

def init_youtube(api_key):
    """Initialize YouTube API client."""
    return build("youtube", "v3", developerKey=api_key)

def fetch_youtube(youtube, query, max_results=5):
    """Fetch YouTube videos for a query including title, description, and transcript."""
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results
    )
    response = request.execute()
    videos = []

    for item in response.get("items", []):
        video_id = item["id"]["videoId"]

        # Fetch transcript if available
        transcript_text = ""
        try:
            # Try old style get_transcript (works on older versions)
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = " ".join([t['text'] for t in transcript_list])
        except (TranscriptsDisabled, NoTranscriptFound):
            transcript_text = ""
        except AttributeError:
            # If get_transcript not available, skip transcript
            transcript_text = ""

        # Combine title, description, and transcript
        full_text = item["snippet"]["title"] + " " + item["snippet"]["description"] + " " + transcript_text
        full_text_cleaned = clean_text(full_text)

        videos.append({
            "source_type": "youtube",
            "source_name": item["snippet"]["channelTitle"],
            "text": full_text_cleaned,
            "timestamp": item["snippet"]["publishedAt"]
        })

    return videos
