import yt_dlp

# I have no idea
def download_video(video_url, save_directory=None):
    if save_directory is None:
        save_directory = f"../downloads/{video_url.split("=")[1]}"
    download_options = {
        "write-subs": True,
        "write-auto-subs": True,
        "sub-lang": "en",
        "sub-format": "webvtt",
        "convert-subs": True,
        "skip_download": True,
        "outtmpl": f"{save_directory}/%(id)s.%(ext)s"
    }
    with yt_dlp.YoutubeDL(download_options) as ydl:
        video_info = ydl.download([video_url])
    return video_info

