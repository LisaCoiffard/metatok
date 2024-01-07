import pandas as pd
import vertexai
from transcription import Transcript
from tts import create_mp3
from vertexai.preview.language_models import ChatModel, TextGenerationModel
from openai import OpenAI


def get_global_summary(text_list):
    text = "\n".join(text_list)
    chat_model = ChatModel.from_pretrained("chat-bison-32k")
    chat = chat_model.start_chat(
        context="""
        You are Oprah and are talking about the gossip with celebreties.
    """
    )
    #         News concerning the same people should be grouped together into a single sentence.
    response = chat.send_message(
        f"""
        Summarize the previous bullet points.
        The length of the summary should be around 4 paragraphs.
        Extract only the most outrageous stuff and cluster it into topics. Give me all the itti bitti details and the juicy stuff. Talk like oprah winfrey but you are not oprah just the style! \n
        Just write the content do not write that you are writing a summary!!!
        {text}
        """
    ).candidates[0]
    return str(response)


def summarize_video(text):

    chat_model = ChatModel.from_pretrained("chat-bison-32k")
    context = "You are Oprah and are talking about the gossip with celebrities. Talk like oprah winfrey but you are not oprah just the style! "
    chat = chat_model.start_chat(context=context)
    response = chat.send_message(
        f"""
        Summarize the following text in qoutes.Write a 15 word summary if the text focuses of a single story put all this text into one line not multiple lines. Otherwise, if the text has separate news points, write a short summary of each news topic in the text (also in one line) and separate
        these with an extra line.
        {text}
        Just write the content do not write that you are writing a summary!!!
        Summary:
    """
    ).candidates[0]
    return str(response)


client = OpenAI()


vertexai.init(project="merantix-genai23ber-9504", location="us-central1")


def summarize_video_oai(text) -> str:
    content_text = "You are Oprah and are talking about the gossip with celebrities. Talk like oprah winfrey but you are not oprah just the style! "
    text = text[:3900]
    instruction = f"""
        Summarize the following text in qoutes.Write a 15 word summary if the text focuses of a single story put all this text into one line not multiple lines. Otherwise, if the text has separate news points, write a short summary of each news topic in the text (also in one line) and separate these with an extra line. {text} Just write the content do not write that you are writing a summary!!!
    """

    return make_request(instruction, content_text)


def make_request(instruction, context) -> str:
    return str(
        client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": instruction},
            ],
        )
        .choices[0]
        .message.content
    )


def get_global_summary_open_ai(text_list) -> str:
    context_text = "You are Oprah and are talking about the gossip with celebreties. "
    text = "\n".join(text_list)
    instruction = f"""
        Summarize the previous bullet points.
        The length of the summary should be around 4 paragraphs.
        Extract only the most outrageous stuff and cluster it into topics. Give me all the itti bitti details and the juicy stuff. Talk like oprah winfrey but you are not oprah just the style! \n
        Just write the content do not write that you are writing a summary!!!
        {text}
        """
    return make_request(instruction, context_text)


def get_data(path):
    return pd.read_csv(path)


current_date = str(pd.Timestamp.now()).split(" ")[0]


def get_summary(generated_path: str, path=None, generate_summary=True):
    if generate_summary:
        df = get_data(path)
        df["summary"] = df["text"].apply(summarize_video_oai)
    else:
        df = pd.read_csv("data/summary.csv")
    summary = get_global_summary_open_ai(df["summary"].tolist())

    with open(generated_path, "w") as f:
        f.write(summary)


def youtube_channels_to_summary_mpr(
    channels=None, generate_summary=True, download_transcript=True
):
    transcription_path = "data/transcripts.csv"
    generated_path = f"data/summaries_of_summary_openai{current_date}.txt"
    if download_transcript:
        time_frame = 1  # in days
        transcrpt = Transcript(time_frame=time_frame, channel_ids=channels)
        transcripts = transcrpt.get_transcript()
        transcrpt.save_transcripts(transcripts, transcription_path)
    if generate_summary:
        get_summary(
            generated_path=generated_path,
            path=transcription_path,
            generate_summary=generate_summary,
        )
    create_mp3(generated_path)


import fire

if __name__ == "__main__":
    fire.Fire(youtube_channels_to_summary_mpr)
    # youtube_channels_to_summary_mpr(
    #     None, generate_summary=True, download_transcript=False
    # )
