import os
import subprocess

# Note to future selves and repo dwellers that we tried our best to use the yt-dlp library and it just didn't work.

# Downloads the transcript (overwrite = False means it'll used the cached file)
def download_transcript(video_url, runtime_directory, overwrite = False):

    # TODO: Right now it assumes format https://youtube.com/watch?v=xxxxxxxxxxx
    video_id = video_url[len(video_url) - 11:]

    directory = f"{runtime_directory}/{video_id}"

    if not os.path.exists(directory):
        os.makedirs(directory)

    subtitle_downloaded = os.path.exists(directory + f"/{video_id}.en.vtt")
    video_downloaded = os.path.exists(directory + f"/{video_id}.mp4")

    args = [
        "yt-dlp",
        "--output", directory + "/%(id)s.%(ext)s",
    ]


    if not video_downloaded or overwrite:
        args.append("-f 137+140")
    else:
        args.append("--skip-download")
        print("[info] video already downloaded, skipping downloading")

    if not subtitle_downloaded or overwrite:
        args.append("--write-auto-subs")
        args.append("--sub-lang")
        args.append("en")
        args.append("--sub-format")
        args.append("webvtt")
    else:
        print("[info] subtitles already downloaded, skipping download")

    if subtitle_downloaded and video_downloaded and not overwrite:
        return

    args.append(video_url)
    subprocess.run(args)
