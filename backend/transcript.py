import re
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(video_url):

    parsed_url = urlparse(video_url.strip())
    hostname = parsed_url.hostname or ""

    video_id = None

    # Handle youtu.be URLs
    if hostname in ["youtu.be", "www.youtu.be"]:
        video_id = parsed_url.path.strip("/").split("/")[0]

    # Handle youtube.com URLs
    elif hostname.endswith("youtube.com") or hostname.endswith("youtube-nocookie.com"):

        if parsed_url.path == "/watch":
            video_id = parse_qs(parsed_url.query).get("v", [None])[0]

        else:
            path_parts = parsed_url.path.strip("/").split("/")

            if len(path_parts) >= 2 and path_parts[0] in [
                "embed", "shorts", "live"
            ]:
                video_id = path_parts[1]

    if video_id and re.fullmatch(r"[a-zA-Z0-9_-]{11}", video_id):
        return video_id

    raise ValueError("Invalid YouTube URL")


def get_transcript(video_url):

    try:
        video_id = extract_video_id(video_url)

        print("Extracting transcript for video:", video_id)

        api = YouTubeTranscriptApi()

        transcript = api.fetch(
            video_id,
            languages=["en", "en-US", "en-GB"]
        )

        transcript_data = []

        for snippet in transcript:

            transcript_data.append({
                "text": snippet.text,
                "start": snippet.start,
                "duration": snippet.duration
            })

        print("Transcript extracted:", len(transcript_data))

        return transcript_data

    except Exception as e:

        print("Transcript extraction error:", repr(e))

        return None


def format_timestamp(seconds):

    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)

    return f"{minutes:02d}:{remaining_seconds:02d}"