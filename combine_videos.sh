#!/bin/bash
rm looped_video1.mp4 looped_video2.mp4 looped_video3.mp4 list.txt combined_looped.mp4

# Define the video files
VIDEO1="data/kanye.mp4"
VIDEO3="data/larry.mp4"
VIDEO2="data/drake.mp4"
AUDIO_FILE="data/podcast_output.mp3"

# Loop each video 5 times
cp data/kanye.mp4 looped_video1.mp4
ffmpeg -stream_loop 2 -i $VIDEO2 -c copy looped_video2.mp4
ffmpeg -stream_loop 2 -i $VIDEO3 -c copy looped_video3.mp4

# Combine the looped videos
echo "file 'looped_video1.mp4'" > list.txt
echo "file 'looped_video2.mp4'" >> list.txt
echo "file 'looped_video3.mp4'" >> list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy combined_looped.mp4

# Get the duration of the combined video in seconds
#DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 combined_looped.mp4)

# Stretch the combined video to 2.11 minutes
ffmpeg -i combined_looped.mp4 -vf "setpts=3*PTS" -an stretched.mp4

# Overlay the MP3 audio
ffmpeg -i stretched.mp4 -i $AUDIO_FILE -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 data/final_output.mp4

# Clean up temporary files
rm looped_video1.mp4 looped_video2.mp4 looped_video3.mp4 list.txt combined_looped.mp4
