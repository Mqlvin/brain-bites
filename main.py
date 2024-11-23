from dotenv import load_dotenv
import os

from video.download import download_transcript
from video.webvtt import WebVTT
from api.openai_client import OpenAIWrapper, OpenAIModel

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



if __name__ == '__main__':
    # Init environment variables
    init_env()

    # Singleton openai client, I'm sticking to gpt 4o mini for testing
    openai_client = OpenAIWrapper(os.getenv("OPENAI_KEY"), OpenAIModel.GPT_4O_MINI)

    # download transcript and deserialize into WebVTT object
    download_transcript("https://www.youtube.com/watch?v=SHZAaGidUbg", runtime_dir)
    transcript = WebVTT(runtime_dir + "/SHZAaGidUbg.en.vtt")
