import os
import subprocess

# Note to future selves and repo dwellers that we tried our best to use the yt-dlp library and it just didn't work.

# Downloads the transcript (overwrite = False means it'll used the cached file)
def download_transcript(video_url, runtime_directory, overwrite = False):

    # TODO: Right now it assumes format https://youtube.com/watch?v=xxxxxxxxxxx
    video_id = video_url[len(video_url) - 11:]
    if os.path.exists(runtime_directory + "/" + video_id + ".en.vtt") and not overwrite:
        print("[INFO] File already downloaded, skipping download...")
        return

    args = [
        "yt-dlp",
        "--write-subs",
        "--write-auto-subs",
        "--sub-lang", "en",
        "--sub-format", "webvtt",
        "--skip-download",
        "--output", runtime_directory + "/%(id)s.%(ext)s",
        video_url
    ]

    subprocess.run(args)
