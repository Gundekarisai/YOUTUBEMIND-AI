
import re
from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi


# --------------------------------------------------
# 1. EXTRACT YOUTUBE VIDEO ID
# --------------------------------------------------

def extract_video_id(video_url):

    video_url = video_url.strip()

    # Add https if the user does not provide it
    if not video_url.startswith(("http://", "https://")):
        video_url = "https://" + video_url

    parsed_url = urlparse(video_url)
    hostname = (parsed_url.hostname or "").lower()

    video_id = None

    # Handle youtu.be links
    if hostname in ["youtu.be", "www.youtu.be"]:
        video_id = parsed_url.path.strip("/").split("/")[0]

    # Handle youtube.com links
    elif hostname.endswith("youtube.com") or hostname.endswith("youtube-nocookie.com"):

        if parsed_url.path == "/watch":
            video_id = parse_qs(parsed_url.query).get("v", [None])[0]

        else:
            path_parts = parsed_url.path.strip("/").split("/")

            if len(path_parts) >= 2 and path_parts[0] in [
                "embed",
                "shorts",
                "live"
            ]:
                video_id = path_parts[1]

    # Validate video ID
    if video_id and re.fullmatch(r"[a-zA-Z0-9_-]{11}", video_id):
        return video_id

    raise ValueError("Invalid YouTube URL. Please enter a valid video link.")


# --------------------------------------------------
# 2. EXTRACT VIDEO TRANSCRIPT
# --------------------------------------------------

def get_transcript(video_url):

    try:

        video_id = extract_video_id(video_url)

        print("\n--------------------------------")
        print("YouTube Transcript Extraction")
        print("--------------------------------")
        print("Video ID:", video_id)

        api = YouTubeTranscriptApi()

        # Fetch available transcripts
        transcript_list = api.list(video_id)

        available_transcripts = list(transcript_list)

        if not available_transcripts:
            raise ValueError(
                "No captions are available for this YouTube video."
            )

        # Display available languages
        print("\nAvailable transcripts:")

        for item in available_transcripts:
            print(
                "Language:", item.language,
                "| Code:", item.language_code,
                "| Auto-generated:", item.is_generated
            )

        # --------------------------------------------------
        # 3. FIND ENGLISH TRANSCRIPT
        # --------------------------------------------------

        transcript = None

        for item in available_transcripts:

            if item.language_code in ["en", "en-US", "en-GB"]:
                transcript = item
                print("\nEnglish transcript found.")
                break

        # --------------------------------------------------
        # 4. TRANSLATE IF ENGLISH IS NOT AVAILABLE
        # --------------------------------------------------

        if transcript is None:

            print("\nEnglish captions not found.")

            # Select the first available transcript
            original_transcript = available_transcripts[0]

            print(
                "Trying translation from:",
                original_transcript.language
            )

            if original_transcript.is_translatable:

                try:
                    transcript = original_transcript.translate("en")
                    print("Translation to English successful.")

                except Exception as translation_error:
                    print("Translation failed:", repr(translation_error))

                    # Use original language if translation fails
                    transcript = original_transcript

            else:

                print("Translation is not available.")
                transcript = original_transcript

        # --------------------------------------------------
        # 5. FETCH TRANSCRIPT DATA
        # --------------------------------------------------

        fetched_transcript = transcript.fetch()

        transcript_data = []

        for snippet in fetched_transcript:

            transcript_data.append({
                "text": snippet.text,
                "start": snippet.start,
                "duration": snippet.duration
            })

        if not transcript_data:
            raise ValueError("The transcript is empty.")

        print("\nTranscript extracted successfully!")
        print("Total transcript segments:", len(transcript_data))
        print("--------------------------------\n")

        return transcript_data

    except Exception as error:
        print("Transcript extraction error:", repr(error))
        return None


# --------------------------------------------------
# 6. FORMAT VIDEO TIMESTAMP
# --------------------------------------------------

def format_timestamp(seconds):

    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)

    return f"{minutes:02d}:{remaining_seconds:02d}"
