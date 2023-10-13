from transcription import Transcript
from summary import summarize_video, get_global_summary
import vertexai

vertexai.init(project="merantix-genai23ber-9504", location="us-central1")

if __name__=="__main__":
    # ask for user input
    time_frame_str = input("Enter your time frame in number of days: ")
    time_frame = int(time_frame_str)
    # UCmCylh0ZK5plLdvueo06OYA, UC2QtjeenJ3KtEli0w4vq5vw, UCjDsbbzHgTrGc4Ff26TJtsA, UCe8vRS6vFq5GmAZIj53Iikw

    # user enters youtube channels as strings that are converted to a list of strings
    channels_str = input("Enter your youtube channels separated by commas: ")
    channels = channels_str.split(", ")
    print(channels)
    assert channels == ['UCmCylh0ZK5plLdvueo06OYA', 'UC2QtjeenJ3KtEli0w4vq5vw', 'UCjDsbbzHgTrGc4Ff26TJtsA', 'UCe8vRS6vFq5GmAZIj53Iikw']

    trscpt = Transcript(time_frame=time_frame, channels=channels)
    transcripts = trscpt.get_transcript()
    transcripts["summary"] = transcripts["text"].apply(summarize_video)
    summary = get_global_summary(transcripts["summary"].tolist())
    print(f"Summary of news of {time_frame} days: \n {summary}")

