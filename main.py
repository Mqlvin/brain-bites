from dotenv import load_dotenv
import os
from video.download import download_video

load_dotenv()
openai_key = os.getenv("OPENAI_KEY")




if __name__ == '__main__':
    download_video("https://www.youtube.com/watch?v=SHZAaGidUbg")
