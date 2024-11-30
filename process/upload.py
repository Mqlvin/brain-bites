import json

from api.openai_client import OpenAIModel, OpenAIWrapper, unwrap_response, summarise_to_topic, generate_questions, \
    summarise_chapter
from process.ffmpeg_api import trim_video
from process.match import find_subtext
from video.download import download_transcript
from video.webvtt import WebVTT, WebVTTUtil

def get_youtube_id(youtube_url):
    return youtube_url.split("=")[-1]

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

# download transcript and deserialize into WebVTT object
def upload_video(openai_client, runtime_dir, youtube_id):
    download_transcript(f"https://www.youtube.com/watch?v={youtube_id}", runtime_dir)
    webvtt = WebVTT(runtime_dir + f"/{youtube_id}/{youtube_id}.en.vtt")
    transcript = webvtt.get_transcript()
    summary = summarise_transcript(openai_client, webvtt)

    # Probably gonna have an error like None has no attribute blah blah but who rlly cares

    times_to_keep = []

    cache_info = {"topic": "undefined", "chapter_count": 0, "chapter_explanations": [], "quiz": []}
    cache_info["topic"] = summarise_to_topic(openai_client, transcript)
    summary = summarise_transcript(openai_client, webvtt)
    question_object = generate_questions(openai_client, summary)
    cache_info["quiz"] = question_object
    chapter_summaries = summarise_chapter(openai_client, summary)
    cache_info["chapter_summary"] = chapter_summaries

    times_to_keep = []

    chapter = -1
    for line in summary.split("\n"):
        if WebVTTUtil.is_whitespace(line):
            continue
        if "<" in line or ">" in line:
            chapter += 1
            times_to_keep.append(list())
            continue
        start_index, end_index = find_subtext(transcript, line)
        start_time, end_time = webvtt.get_time_of_phrase(start_index, end_index)
        print(f"{line}: {start_time} --> {end_time}")
        times_to_keep[chapter].append((start_time.seconds(), end_time.seconds()))
        cache_info["chapter_count"] = len(times_to_keep)

    for chapter_id, chapter_times in enumerate(times_to_keep):
        trim_video(f"{runtime_dir}/{youtube_id}/{youtube_id}.mp4",
                   f"{runtime_dir}/{youtube_id}/chapter-{chapter_id}.mp4", chapter_times)

    cache_file = open(f"{runtime_dir}/{youtube_id}/associated_data.json", "w")
    cache_file.write(json.dumps(cache_info))
    cache_file.close()