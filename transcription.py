import os
from datetime import datetime, timedelta

import pandas as pd
import requests
from youtube_transcript_api import YouTubeTranscriptApi

CHANNEL_IDS = [
    "UCmCylh0ZK5plLdvueo06OYA",
    "UC2QtjeenJ3KtEli0w4vq5vw",
    "UCjDsbbzHgTrGc4Ff26TJtsA",
    "UCe8vRS6vFq5GmAZIj53Iikw",
]
API_KEY = os.environ.get("GOOGLE_API_KEY")


def get_transcription(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t["text"] for t in transcript])
    except:
        print(f"Did not find transcript for {video_id}")


class Transcript:

    def __init__(self, time_frame, channels=None) -> None:
        self.time_frame = time_frame
        if channels is None:
            channels = CHANNEL_IDS

        self.video_ids = [
            vid for channel_id in channel_ids for vid in self._get_videos(channel_id)
        ]
        self.video_ids = pd.DataFrame(self.video_ids)
        self.video_ids = self._filter_time()

    def _get_videos(self, channel_id, num_videos=10, api_key=API_KEY):
        base_url = "https://www.googleapis.com/youtube/v3/search"

        params = {
            "part": "snippet",
            "channelId": channel_id,
            "maxResults": num_videos,
            "order": "date",  # order by date (latest first)
            "type": "video",  # we want only videos, not playlists or channels
            "key": api_key,
        }

        response = requests.get(base_url, params=params)
        assert response.ok, response.content
        data = response.json()

        videos = [
            {
                "vid": item["id"]["videoId"],
                "date": pd.to_datetime(item["snippet"]["publishTime"]).replace(
                    tzinfo=None
                ),
            }
            for item in data["items"]
        ]
        return videos

    def _filter_time(self):
        time_limit = datetime.now() - timedelta(days=self.time_frame)
        return self.video_ids[self.video_ids["date"] > time_limit]

    def get_transcript(self):
        """Returns a dataframe of transcripted videos within the desired time frame for designated channels"""
        transcripts = pd.DataFrame(
            [
                {"text": get_transcription(vid), "vid": vid}
                for vid in self.video_ids["vid"]
            ]
        )
        transcripts = transcripts[transcripts["text"].notna()]
        return transcripts

    def save_transcripts(self, transcripts_df, file_path):
        """Saves the transcripted videos"""
        data_dir = "data/"
        # if the data directory does not exist, create it
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        transcripts_df.to_csv(file_path, index=False)


if __name__ == "__main__":
    time_frame = 1  # in days
    transcrpt = Transcript(time_frame=time_frame)
    transcripts = transcrpt.get_transcript()
    transcrpt.save_transcripts(transcripts, "transcripts")
