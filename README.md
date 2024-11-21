## Brain Bites
Shorten long documentaries 📽️ into short, education-packed videos ⚡.
<br>

### Usage / Running
#### Dependencies
To run the project, you will need the `openai` and `dotenv` Python libraries.<br>
You can either `pip install` them, or can install them otherwise appropriate to your operating system.<br>
<br>
You will also need `yt-dlp` available on your system's PATH, so it is executable from the terminal.<br>
<br>
The project will require an environment variable keystore (`.env` file) with the following keys:
- `OPENAI_KEY` - Your OpenAI API key.
- `RUNTIME_DIR` (optional) - The runtime directory, defaults to `./runtime`

<br>

### The Vision
The current project trajectory is to use AI and LLM to trim YouTube videos from lengthy documentaries into short and fast paced educational videos.<br>
This is to make videos more engaging and practical for usage, such as in a classroom, where time and attention spans are limited.<br>

The exact implementation / front-end of the project (whether a website, gamified app, e.g.) is work-in-progress.

<br>

### The Process
- We feed **OpenAI's GPT-4** with YouTube transcripts, asking the LLM to regenerate a concise / trimmed transcript.<br>
- A comparison between the full and trimmed transcript will occur using *(wip)*, finding the removed sentences from the transcript.<br>
- The removed sentences from the transcript will be cut from the video using **ffmpeg**, shortening the video.<br>

<br>

### Inversity
This is an [Inversity](https://inversity.co/) project application.<br>
We were tasked with "How can AI make education more engaging, effective and equitable?"
