import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai


# LOAD ENVIRONMENT VARIABLES

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini API key not found!")


# INITIALIZE GEMINI

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.5-flash-lite"


# CONVERSATIONAL MEMORY

def contextualize_question(question, chat_history):

    if not chat_history:
        return question

    history_text = ""

    for message in chat_history[-6:]:

        history_text += (
            f"{message['role']}: {message['content']}\n"
        )

    prompt = f"""
    You are a question-rewriting assistant.

    Rewrite the latest user question as a standalone question
    using the previous conversation when necessary.

    Rules:
    - Resolve references such as he, she, it and they.
    - Preserve the original meaning.
    - Do not answer the question.
    - Do not add new facts.
    - If the question is already clear, return it unchanged.

    Previous conversation:
    {history_text}

    Latest question:
    {question}

    Return only the rewritten question.
    """

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text.strip()


# GENERATE AI ANSWER

def generate_answer(question, context, chat_history=None):

    history_text = ""

    if chat_history:

        for message in chat_history[-6:]:

            history_text += (
                f"{message['role']}: {message['content']}\n"
            )

    prompt = f"""
    You are YouTubeMind AI, an intelligent video assistant.

    Answer the user's question using ONLY the information
    available in the provided video context.

    Use conversation history to understand follow-up questions.

    Rules:
    - Do not invent information.
    - Do not use outside knowledge.
    - If the video does not contain the answer, clearly
      say that the video does not provide enough information.
    - Give clear and understandable answers.

    Previous Conversation:
    {history_text}

    Video Context:
    {context}

    Current User Question:
    {question}

    Answer:
    """

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text


# GENERATE VIDEO SUMMARY

def generate_video_summary(chunks, summary_type="Detailed"):

    context = "\n\n".join(chunks)

    if summary_type == "Short":

        instructions = """
        Create a short summary of the entire video.
        Explain the main idea in approximately 150 words.
        """

    elif summary_type == "Detailed":

        instructions = """
        Create a detailed summary of the video.

        Organize it using:
        1. Introduction
        2. Main Topics
        3. Important Events
        4. Conclusion

        Explain the important information clearly.
        """

    elif summary_type == "Key Takeaways":

        instructions = """
        Extract the most important takeaways from the video.

        Present them as numbered bullet points.
        Focus on the most valuable information.
        """

    else:

        instructions = "Create a clear summary of the video."


    prompt = f"""
    You are YouTubeMind AI, an expert video summarization assistant.

    Analyze the following YouTube video transcript.

    {instructions}

    Important rules:
    - Use ONLY information from the transcript.
    - Do not invent facts.
    - Do not include unsupported information.
    - Use clear and simple language.
    - Organize the output professionally.

    VIDEO TRANSCRIPT:

    {context}

    Generate the requested summary.
    """

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text