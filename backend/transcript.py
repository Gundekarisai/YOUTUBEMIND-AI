import re
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(video_url):

    pattern = (
        r"(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/)|"
        r"youtu\.be\/)([a-zA-Z0-9_-]{11})"
    )

    match = re.search(pattern, video_url)

    if match:
        return match.group(1)

    raise ValueError("Invalid YouTube URL")


def get_transcript(video_url):

    try:
        video_id = extract_video_id(video_url)

        api = YouTubeTranscriptApi()

        transcript = api.fetch(video_id, languages=["en"])

        transcript_data = []

        for snippet in transcript:

            transcript_data.append({
                "text": snippet.text,
                "start": snippet.start,
                "duration": snippet.duration
            })

        return transcript_data

    except Exception as e:

        print("Transcript extraction error:", e)

        return None


def format_timestamp(seconds):

    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)

    return f"{minutes:02d}:{remaining_seconds:02d}"