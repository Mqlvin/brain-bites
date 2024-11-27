from api.openai_client import OpenAIModel, OpenAIWrapper, unwrap_response
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
             "content": "You are designed to summarise educational transcripts. But you MUST still use their wording. Give me each summarised sentence on a new line."},
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

    print(transcript)

    summary = summarise_transcript(openai_client, webvtt)

    # Probably gonna have an error like None has no attribute blah blah but who rlly cares

    times_to_keep = []

    for line in summary.split("\n"):
        if WebVTTUtil.is_whitespace(line):
            continue
        start_index, end_index = find_subtext(transcript, line)
        start_time, end_time = webvtt.get_time_of_phrase(start_index, end_index)
        print(f"{line}: {start_time} --> {end_time}")
        times_to_keep.append((start_time.seconds(), end_time.seconds()))

    trim_video(f"./runtime/{youtube_id}/{youtube_id}.mp4", f"{youtube_id}.mp4", times_to_keep)
