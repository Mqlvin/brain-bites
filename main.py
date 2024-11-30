import json
import os
import random
from threading import Thread

import openai
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, send_file
from werkzeug.utils import environ_property

from api.openai_client import (OpenAIModel, OpenAIWrapper, generate_questions,
                               summarise_chapter, summarise_to_topic,
                               summarise_transcript)
from flask_app.config import Config
from flask_app.forms import UploadForm
from process.ffmpeg_api import trim_video
from process.match import find_subtext
from process.upload import get_youtube_id, upload_video
from video.download import download_transcript
from video.webvtt import WebVTT, WebVTTUtil
from flask_app.icons import Icon, Color

runtime_dir = ""
openai_client = None
app = Flask(__name__, static_url_path='', static_folder="./templates/static")
  

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

def render(template, **kwargs):
    return render_template(template, title="Brain Bites", **kwargs)

@app.route("/")
@app.route("/index")
def index():
    return render("index.html")

@app.route("/videos")
def browse():

    unchosen_colors = [color.value for color in list(Color)]

    def random_color(__unchosen_colors):
        if len(__unchosen_colors) == 0:
            __unchosen_colors = [color.value for color in list(Color)]
        color = random.choice(__unchosen_colors)
        __unchosen_colors.remove(color)
        return color

    icons = [
        Icon("Engineering", random_color(unchosen_colors), "/videos/7rMgpExA4kM"),
        Icon("Biology", random_color(unchosen_colors), "/"),
        Icon("Chemistry", random_color(unchosen_colors), "/"),
        Icon("Physics", random_color(unchosen_colors), "/"),
        Icon("Computer Science", random_color(unchosen_colors), "/"),
        Icon("Maths", random_color(unchosen_colors), "/"),
    ]
    print(icons[0].get_background())
    return render("browse.html", icons=icons)

@app.route("/videos/<video_id>")
def videos(video_id):
    runtime_dir = os.getenv("RUNTIME_DIR", "./runtime")
    if video_id not in os.listdir(runtime_dir):
        return "Could not find video!"
    else:
        video_data_text = open(f"{runtime_dir}/{video_id}/associated_data.json", "r")
        video_data = json.loads(video_data_text.read())
        json_questions = video_data["quiz"] # once i accidentally added a semicolon here sorry for not being pythonic
        chapter_summary = video_data["chapter_summary"]
        chapter_count = video_data["chapter_count"]

        return render_template("player.html", chapters=chapter_count, topic=video_data["topic"], video_id=video_id, json_questions=json_questions, chapter_summary=chapter_summary)

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

    return render('upload.html', form=form)

@app.route("/upload-complete")
def upload_complete():
    return render("upload-complete.html")

def main():
    global openai_client
    init_env()

    # Singleton openai client, I'm sticking to gpt 4o mini for testing
    openai_client = OpenAIWrapper(os.getenv("OPENAI_KEY"), OpenAIModel.GPT_4O_MINI)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.run()


if __name__ == '__main__':
     main()
