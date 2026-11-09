from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(transcript_data):

    # Combine transcript segments while preserving timestamps
    full_text = ""

    for item in transcript_data:

        start = item["start"]
        text = item["text"]

        minutes = int(start // 60)
        seconds = int(start % 60)

        timestamp = f"{minutes:02d}:{seconds:02d}"

        full_text += f"[{timestamp}] {text}\n"

    # Initialize text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_text(full_text)

    return chunks