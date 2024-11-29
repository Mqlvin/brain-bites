import os
from threading import Thread

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, send_file

from api.openai_client import OpenAIModel, OpenAIWrapper, unwrap_response
from flask_app.config import Config
from flask_app.forms import UploadForm
from process.ffmpeg_api import trim_video
from process.match import find_subtext
from process.upload import get_youtube_id, upload_video
from video.download import download_transcript
from video.webvtt import WebVTT, WebVTTUtil

runtime_dir = ""
openai_client = None
app = Flask(__name__, static_url_path='', static_folder="./templates/static")

# loads and handles init of environment variables
def init_env():
    global runtime_dir
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
             "content": "You are designed to summarise educational transcripts. But you MUST still use their wording. Give me each summarised sentence on a different, and split into chapters of about five sentences long, titled as <Chapter 1>, <Chapter 2> and so on."},
            {"role": "user",
             "content": transcript.get_transcript()}
        ]
    )

    return unwrap_response(chat_completion)

  
  
  

def init_env():
    global runtime_dir
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

      


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/videos/<video_id>")
def videos(video_id):
    runtime_dir = os.getenv("RUNTIME_DIR", "./runtime")
    if video_id not in os.listdir(runtime_dir):
        return "Could not find video!"
    else:
        chapter_count = len(list(filter(lambda x: x.startswith("chapter"), os.listdir(runtime_dir + "/" + video_id))))
        return render_template("player.html", chapters = chapter_count, topic = "Airplane")

@app.route("/source/<video_id>/<_>.mp4")
def source(video_id, _):
    return send_file(f"runtime/{video_id}/{_}.mp4")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        youtube_id = get_youtube_id(form.youtube_url.data)
        thread = Thread(target=upload_video, args=(openai_client, runtime_dir, youtube_id,))
        thread.run()
        return redirect("/upload-complete")

    return render_template('upload.html', form=form)

@app.route("/upload-complete")
def upload_complete():
    return render_template("upload-complete.html")



def main():
    init_env()

    youtube_id = "7rMgpExA4kM"
    if not os.path.isdir(f"{runtime_dir}/{youtube_id}"):

        # Singleton openai client, I'm sticking to gpt 4o mini for testing
        # openai_client = OpenAIWrapper(os.getenv("OPENAI_KEY"), OpenAIModel.GPT_4O_MINI)
    
        # download transcript and deserialize into WebVTT object
        # download_transcript("https://www.youtube.com/watch?v=" + youtube_id, runtime_dir)
        # webvtt = WebVTT(runtime_dir + f"/{youtube_id}/{youtube_id}.en.vtt")
        # transcript = webvtt.get_transcript()
        # print(transcript)
        # summary = summarise_transcript(openai_client, webvtt)
        # Probably gonna have an error like None has no attribute blah blah but who rlly cares
        # times_to_keep = []


       # chapter = -1
       # for line in summary.split("\n"):
       #     if WebVTTUtil.is_whitespace(line):
       #         continue
       #     if "<" in line or ">" in line:
       #         chapter += 1
       #         times_to_keep.append(list())
       #         continue
       #     start_index, end_index = find_subtext(transcript, line)
       #     start_time, end_time = webvtt.get_time_of_phrase(start_index, end_index)
       #     print(f"{line}: {start_time} --> {end_time}")
       #     times_to_keep[chapter].append((start_time.seconds(), end_time.seconds()))
    
       # for chapter_id, chapter_times in enumerate(times_to_keep):
            trim_video(f"{runtime_dir}/{youtube_id}/{youtube_id}.mp4", f"{runtime_dir}/{youtube_id}/chapter-{chapter_id}.mp4", chapter_times)


    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.run()


if __name__ == '__main__':
     main()
