import subprocess
import json


# ffmpeg trim function keeps the segments you provide it to trim (basically the opposite you'd expect)
# hence, this function inverts the cut_segments to be keep_segments
def _invert_segments(cut_segments: list[(float, float)], video_length: float) -> list[(float, float)]:
    result: list[(float, float)] = []
    base_time = 0

    for tup in cut_segments:
        result.append((base_time, tup[0]))
        base_time = tup[1]

    if base_time != video_length:
        result.append((base_time, video_length))

    return result


# gets video length as float with ffprobe
def _ffprobe_video_length(input_path: str) -> float:
    result = subprocess.check_output(
            f"ffprobe -v quiet -show_streams -select_streams v:0 -of json '{input_path}'",
            shell=True).decode()

    return float(json.loads(result)['streams'][0]['duration'])



# Function to trim video via ffmpeg, input/output paths are self explanatory
# cut_segments is a SORTED list of tuples containing the start and end times of sections to be cut
def trim_video(input_path: str, output_path: str, cut_segments: list[(float, float)]):
    
    # cli/subprocess args
    args = [
        "ffmpeg",
        "-i", input_path,
        "-filter_complex", # now generate cut arguments...
    ]

    keep_segments = _invert_segments(cut_segments, _ffprobe_video_length(input_path))

    # appends specific trim arguments to arguments (one for audio one for video)
    trims = 0
    filters = ""
    for tup in keep_segments:
        filters += f"[0:v]trim=start={tup[0]}:end={tup[1]},setpts=PTS-STARTPTS,format=yuv420p[{trims}v];"
        filters += f"[0:a]atrim=start={tup[0]}:end={tup[1]},asetpts=PTS-STARTPTS[{trims}a];"
        trims += 1

    for i in range(trims):
        filters += f"[{i}v][{i}a]"

    filters += f"concat=n={trims}:v=1:a=1[outv][outa]"
    args.append(filters) # add filter list

    # add final args
    args.extend(["-map", "[outv]", "-map", "[outa]"])
    args.append(output_path)

    # uncomment to view command.. print(" ".join(args))
    subprocess.run(args)



# usage: trim_video("./video.mp4", "out.mp4", [(10, 30), (31, 35), (76, 86)])
