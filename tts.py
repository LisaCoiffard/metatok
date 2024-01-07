import os

import requests


def get_speach_stream(text):
    rachel_voice_id = "21m00Tcm4TlvDq8ikWAM"
    "21m00Tcm4TlvDq8ikWAM"
    old_voice_id = "jBpfuIE2acCO8z3wKNLl"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{rachel_voice_id}"
    # get api key from environment variable

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{old_voice_id}"
    texts = text.split("\n")
    texts = [t for t in texts if len(t) > 0]
    breakpoint()

    payload = {
        "model_id": "eleven_monolingual_v1",
        "text": text,
        "voice_settings": {
            "similarity_boost": 0.75,
            "stability": 0.5,
            "use_speaker_boost": True,
        },
    }
    headers = {"Content-Type": "application/json"}
    print(len(text))

    response = requests.request("POST", url, json=payload, headers=headers)

    assert response.status_code == 200
    return response


def create_mp3(path):
    # load summary
    with open(path, "r") as f:
        summary = f.read()

    CHUNK_SIZE = 1024
    audio_filename = "data/podcast_output.mp3"
    for i in range(len(summary) // 2400):
        response = get_speach_stream(summary[i * 2400 : (i + 1) * 2400])
        with open(audio_filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)


if __name__ == "__main__":
    create_mp3("data/summaries_of_summary.txt")

    print("MP3 generation finished")
# import requests
#
# url = "https://api.elevenlabs.io/v1/voices"
#
# headers = {
#   "Accept": "application/json",
#   "xi-api-key": "7c2067adce7482a413e2856aadf56349"
# }
#
# response = requests.get(url, headers=headers)
#
# print(response.text)
