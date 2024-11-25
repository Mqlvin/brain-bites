from dotenv import load_dotenv
import os

from process.match import find_subtext
from video.download import download_transcript
from video.webvtt import WebVTT
from api.openai_client import OpenAIWrapper, OpenAIModel, unwrap_response

runtime_dir = ""


# loads and handles init of environment variables
def init_env():
    # Loads the dotenv file
    load_dotenv()

    # Handle dotenv inputs
    openai_key = os.getenv("OPENAI_KEY")
    if not openai_key:
        print("[ERROR] No OpenAI key provided. Check https://github.com/Mqlvin/brain-bites/ for usage instructions.")
        exit(1)

    runtime_dir = os.getenv("RUNTIME_DIR", "./runtime")
    # make the directory
    try:
        os.makedirs(runtime_dir, exist_ok=True)
    except:
        print("[ERROR] Failed to make runtime directory")

def summarise_transcript(client, transcript):
    chat_completion = client.get_client().chat.completions.create(
        model=client.get_active_model(),
        messages=[
            {"role": "system",
             "content": "You are designed to summarise educational transcripts. But you MUST still use their wording. Give me each summarised sentence on a new line."},
            {"role": "user",
             "content": transcript.get_transcript()}
        ]
    )

    return unwrap_response(chat_completion)


def main():
    # Init environment variables
    init_env()

    # Singleton openai client, I'm sticking to gpt 4o mini for testing
    openai_client = OpenAIWrapper(os.getenv("OPENAI_KEY"), OpenAIModel.GPT_4O_MINI)

    runtime_dir = "runtime"

    # download transcript and deserialize into WebVTT object
    download_transcript("https://www.youtube.com/watch?v=SHZAaGidUbg", runtime_dir)
    webvtt = WebVTT(runtime_dir + "/idk.en.vtt")
    transcript = webvtt.get_transcript()

    summary = summarise_transcript(openai_client, webvtt)

    # Probably gonna have an error like None has no attribute blah blah but who rlly cares

    for line in summary.split("\n"):
        start_index, end_index = find_subtext(transcript, line)
        start_time, end_time = webvtt.get_time_of_phrase(start_index, end_index)
        print(f"{line}: {start_time} --> {end_time}")

if __name__ == '__main__':
     main()
