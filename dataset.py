import requests
import pandas as pd

CHANNEL_IDS = ["UCmCylh0ZK5plLdvueo06OYA", "UC2QtjeenJ3KtEli0w4vq5vw", "UCjDsbbzHgTrGc4Ff26TJtsA", "UCe8vRS6vFq5GmAZIj53Iikw"]


def get_video_ids_from_channel(channel_id, api_key):
    base_url = "https://www.googleapis.com/youtube/v3/search"
    
    params = {
        'part': 'snippet',
        'channelId': channel_id,
        'maxResults': 10,  # get the last 3 videos
        'order': 'date',  # order by date (latest first)
        'type': 'video',  # we want only videos, not playlists or channels
        'key': api_key
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    videos = [{"vid":item['id']['videoId'], "date":pd.to_datetime(item["snippet"]["publishTime"]).replace(tzinfo=None)} for item in data['items']]  
    return videos


if __name__ == "__main__":
    pass