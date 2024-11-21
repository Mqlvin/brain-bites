import os
import subprocess

# Note to future selves and repo dwellers that we tried our best to use the yt-dlp library and it just doesn't work. don't waste time on it again :)

# I have no idea
def download_video(video_url):
    # bit scrappy can convert this to parameter later
    try:
        os.makedirs("./runtime", exist_ok=True)
    except:
        print("[ERROR] Failed to make runtime directory")


    args = [
        "yt-dlp",
        "--write-subs",
        "--write-auto-subs",
        "--sub-lang", "en",
        "--sub-format", "webvtt",
        "--skip-download",
        "--output", "./runtime/%(id)s-transcript.%(ext)s",
        video_url
    ]

    subprocess.run(args)
