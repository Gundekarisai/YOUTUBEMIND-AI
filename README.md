# 🎬 YouTubeMind AI
### Transform YouTube Videos into Knowledge with Artificial Intelligence

YouTubeMind AI is an AI-powered video intelligence platform that allows users to interact with YouTube videos using natural language.

Instead of watching an entire video to find specific information, users can simply paste a YouTube URL, process its transcript, and ask questions. The application uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information and generate context-aware answers using Google Gemini.

---

## 🚀 Key Features

### 💬 AI-Powered Video Chat
- Ask questions about YouTube videos.
- Get intelligent answers based on video transcripts.
- Maintain conversational history.
- Display the latest conversations first.

### 🧠 Retrieval-Augmented Generation (RAG)
- Extract YouTube video transcripts.
- Split transcripts into smaller text chunks.
- Generate semantic embeddings.
- Store embeddings using FAISS.
- Retrieve relevant context for user questions.
- Generate answers using Google Gemini.

### 📝 Smart Video Summarization
- Generate short summaries.
- Create detailed explanations.
- Extract important takeaways.

### 🔍 Semantic Search
- Search video content using natural language.
- Retrieve relevant transcript chunks.
- Display similarity scores.

### 📄 Transcript Viewer
- View extracted video transcripts.
- Display timestamps.
- Search transcript content.

### 🎨 Modern User Interface
- Professional dark-themed dashboard.
- Animated gradient backgrounds.
- Responsive layout.
- Interactive cards and navigation.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Frontend | Streamlit, HTML, CSS |
| Backend | Python |
| LLM | Google Gemini API |
| Embedding Model | Sentence Transformers |
| Vector Database | FAISS |
| Text Processing | LangChain Text Splitters |
| Transcript Extraction | YouTube Transcript API |
| Environment Management | Python Virtual Environment |
| Version Control | Git and GitHub |

---

## 🏗️ Project Architecture

```text
YouTubeMind-AI/
│
├── backend/
│   ├── transcript.py
│   ├── text_splitter.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retrieval.py
│   └── llm.py
│
├── database/
│
├── utils/
│   └── helpers.py
│
├── app.py
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ How It Works

YouTubeMind AI follows a Retrieval-Augmented Generation pipeline.

1. **YouTube URL Input:** The user provides a YouTube video URL.
2. **Transcript Extraction:** The application extracts the available video transcript.
3. **Text Chunking:** The transcript is divided into smaller chunks.
4. **Embedding Generation:** Sentence Transformers convert chunks into numerical vectors.
5. **Vector Storage:** FAISS stores the generated embeddings.
6. **Semantic Retrieval:** The user's question is converted into an embedding and relevant chunks are retrieved.
7. **AI Response Generation:** Retrieved context is passed to Google Gemini.
8. **Answer Display:** Gemini generates a natural-language answer grounded in the retrieved video content.

```text
YouTube Video URL
       |
       v
Transcript Extraction
       |
       v
Text Chunking
       |
       v
Embedding Generation
       |
       v
FAISS Vector Database
       |
       v
User Question
       |
       v
Semantic Retrieval
       |
       v
Relevant Context
       |
       v
Google Gemini
       |
       v
AI Generated Answer
```

---

## 💻 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YouTubeMind-AI.git
```

### 2. Navigate to the Project Directory

```bash
cd YouTubeMind-AI
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Gemini API Key

Create a `.env` file in the project root directory.

Add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Get your API key from Google AI Studio:

https://aistudio.google.com/apikey

**Important:** Never share your API key or upload your `.env` file to GitHub.

### 7. Run the Application

```bash
streamlit run app.py
```

Open your browser:

```text
http://localhost:8501
```

---

## 📸 Application Workflow

1. Open YouTubeMind AI.
2. Paste a YouTube video URL.
3. Click **Process Video**.
4. Wait for transcript extraction and vector database creation.
5. Open the AI Summary tab to generate summaries.
6. Open Chat with Video to ask questions.
7. Explore the transcript and retrieved sources.

---

## 🎯 Project Objective

The main objective of YouTubeMind AI is to reduce the time and effort required to understand long-form video content.

It makes video information more accessible by combining semantic search, vector databases, and generative AI.

---

## 🔮 Future Enhancements

- Support for multiple YouTube videos.
- Compare information across different videos.
- Timestamp-based answer navigation.
- Multilingual transcript support.
- Video-based knowledge library.
- User authentication and personalized workspaces.
- Persistent chat history.
- Export summaries as PDF.
- Support for additional video platforms.

---

## 👨‍💻 Developer

**Gundekari Sai**

B.Tech – Artificial Intelligence & Machine Learning

Interested in Artificial Intelligence, Machine Learning, Generative AI and building real-world applications.

---

## ⭐ Acknowledgements

- Google Gemini for AI-powered answer generation.
- FAISS for efficient similarity search.
- Sentence Transformers for semantic embeddings.
- Streamlit for the interactive web application.
- YouTube Transcript API for transcript extraction.

---

### 🎬 YouTubeMind AI
**Turning Videos into Knowledge.**
