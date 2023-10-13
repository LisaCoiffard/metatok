import pandas as pd
import vertexai
from tiktok_popnews.transcription import Transcript
from tiktok_popnews.tts import create_mp3
from vertexai.preview.language_models import ChatModel, TextGenerationModel

vertexai.init(project="merantix-genai23ber-9504", location="us-central1")
def summarize_video(text):

    chat_model = ChatModel.from_pretrained("chat-bison-32k")
    context = "You are Oprah and are talking about the gossip with celebrities. Talk like oprah winfrey but you are not oprah just the style! "
    chat = chat_model.start_chat(
        context=context
    )
    response = chat.send_message(f"""
        Summarize the following text in qoutes.Write a 15 word summary if the text focuses of a single story put all this text into one line not multiple lines. Otherwise, if the text has separate news points, write a short summary of each news topic in the text (also in one line) and separate 
        these with an extra line. 
        {text}
        Just write the content do not write that you are writing a summary!!!
        Summary:
    """).candidates[0]
    print("response \n",response)
    return str(response)


def get_global_summary(text_list):
    text = "\n".join(text_list)
    chat_model = ChatModel.from_pretrained("chat-bison-32k")
    chat = chat_model.start_chat(
        context="""
        You are Oprah and are talking about the gossip with celebreties.
    """)
    #         News concerning the same people should be grouped together into a single sentence.
    response =  chat.send_message(f"""
        Summarize the previous bullet points. 
        The length of the summary should be around 4 paragraphs.
        Extract only the most outrageous stuff and cluster it into topics. Give me all the itti bitti details and the juicy stuff. Talk like oprah winfrey but you are not oprah just the style! \n
        Just write the content do not write that you are writing a summary!!!
        {text}
        """).candidates[0]
    return str(response)
def get_data(path):
    return pd.read_csv(path)
def get_summary(path="data/transcription.csv", load_summary=True):
    if load_summary:
        df = pd.read_csv("data/summary.csv")
    else:
        df = get_data(path)
        df["summary"] = df["text"].apply(summarize_video)
    summary = get_global_summary(df["summary"].tolist())

    with open("data/summaries_of_summary.txt", "w") as f:
        f.write(summary)


def youtube_channels_to_summary_mpr(channels, load_summary=True, time_frame = 1):
    if not load_summary:
        transcrpt = Transcript(time_frame=time_frame, channels=channels)
        transcripts = transcrpt.get_transcript()
        transcrpt.save_transcripts(transcripts, "transcripts")
    get_summary(load_summary=load_summary)
    create_mp3("data/summaries_of_summary.txt")

if __name__=="__main__":
    youtube_channels_to_summary_mpr(None)

