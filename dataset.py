from datetime import datetime, timedelta

import pandas as pd
import requests
from youtube_transcript_api import YouTubeTranscriptApi

CHANNEL_IDS = ["UCmCylh0ZK5plLdvueo06OYA", "UC2QtjeenJ3KtEli0w4vq5vw", "UCjDsbbzHgTrGc4Ff26TJtsA", "UCe8vRS6vFq5GmAZIj53Iikw"]


def get_video_ids(channel_id, num_videos, api_key):
    base_url = "https://www.googleapis.com/youtube/v3/search"
    
    params = {
        'part': 'snippet',
        'channelId': channel_id,
        'maxResults': num_videos, 
        'order': 'date',  # order by date (latest first)
        'type': 'video',  # we want only videos, not playlists or channels
        'key': api_key
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    videos = [{"vid":item['id']['videoId'], "date":pd.to_datetime(item["snippet"]["publishTime"]).replace(tzinfo=None)} for item in data['items']]  
    return videos


def filter_time(videos, time_range):
    time_limit = datetime.now() - timedelta(days=time_range)
    return videos[videos["date"] > time_limit]


def get_transcription(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t["text"] for t in transcript])
    except:
        print(f"Did not find transcript for {video_id}")
    return transcript

def get_transcript_csv(video_ids):
    transcripts = pd.DataFrame([{"text": get_transcription(vid), "vid": vid} for vid in video_ids])
    # postprocessing
    transcripts = transcripts[transcripts["text"].notna()]
    transcripts.to_csv("data/transcription.csv", index=False)

if __name__ == "__main__":
    pass