from dotenv import load_dotenv
from video.download import download_video

load_dotenv()
env_config = dotenv_values(".env")

if __name__ == '__main__':
    download_video("https://www.youtube.com/watch?v=SHZAaGidUbg")
