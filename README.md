# 🎬 Video Agent — AI Video & Audio Assistant with RAG Q&A

An end-to-end AI-powered video processing assistant that converts YouTube videos or local audio/video recordings into actionable meeting summaries, structured insights, and an interactive RAG (Retrieval-Augmented Generation) chat engine.

---

🚀 Deployed Link

Deployed Link: https://video-agent-kbbmhgmzwpchbkrs85lvea.streamlit.app/

## 🌟 Key Features

- **📹 Multi-Source Support**: Seamlessly ingests YouTube URLs or local video/audio files (`.mp4`, `.mp3`, `.wav`, `.m4a`).
- **🎙️ Speech-to-Text Transcription**:
  - **Whisper**: Local GPU-accelerated OpenAI Whisper integration (`mps` for Apple Silicon / CUDA for NVIDIA / CPU fallback).
  - **Sarvam AI**: Optional integration for Hinglish/Hindi speech-to-text with auto-translation to English.
- **📝 Automated Summarization & Insights Extraction**:
  - Map-Reduce transcript summarization using **Mistral AI** (`mistral-small-latest`).
  - Automatic extraction of **Action Items** (Task, Owner, Deadline), **Key Decisions**, and **Open Questions**.
- **💬 Interactive Meeting Chat (RAG)**:
  - Vector database storage via **ChromaDB** with **Mistral AI Embeddings**.
  - Ask any question about the meeting context and receive precise, grounded answers.
- **🎨 Top 1% Modern Web Interface & CLI**:
  - Zero-dependency built-in Python backend server (`server.py`).
  - Sleek, modern responsive web frontend dashboard (`static/index.html`).
  - Terminal CLI mode (`main.py`) for quick command-line execution.

---

## 🏗️ Project Architecture

```text
Video Agent/
├── core/
│   ├── transcriber.py       # Whisper & Sarvam AI transcription routing
│   ├── summarizer.py        # Map-reduce transcript summarization
│   ├── extractor.py         # Action items, key decisions & open questions extraction
│   ├── vector_store.py      # ChromaDB embedding & retrieval index
│   └── rag_engine.py        # LangChain RAG pipeline & Q&A chain
├── utils/
│   └── audio_processor.py   # YouTube download (yt-dlp) & audio chunking (pydub)
├── static/                  # Modern Web Dashboard assets
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── app.py                   # Streamlit Dashboard (optional)
├── main.py                  # CLI Interface
├── server.py                # Zero-dependency Python Web Server (Port 8000)
├── test.py                  # Quick test script
├── requirements.txt         # Project dependencies
├── .env.example             # Environment variables template
└── README.md                # Documentation
```

---

## ⚡ Quick Start

### 1. Prerequisites

Make sure you have **Python 3.10+** and **ffmpeg** installed on your system.

**On macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**On Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

---

### 2. Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mitalijain0606-ux/video-agent.git
   cd video-agent
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

### 3. Environment Setup

Create a `.env` file in the root directory by copying `.env.example`:

```bash
cp .env.example .env
```

Open `.env` and fill in your API keys:

```env
# Required for LLM Summarization & Embeddings
MISTRAL_API_KEY=your_mistral_api_key_here

# Whisper Model Size (tiny, base, small, medium, large)
WHISPER_MODEL=small

# Optional: Sarvam AI API Key (for Hinglish audio translation)
SARVAM_API_KEY=your_sarvam_api_key_here
SARVAM_STT_MODEL=saaras:v2.5
SARVAM_STT_TRANSLATE_URL=https://api.sarvam.ai/speech-to-text-translate
```

---

## 🚀 Running the Application

### Option A: Web Application (Recommended)

Start the built-in server:
```bash
python server.py
```
Open your browser and navigate to **`http://localhost:8000`**.

### Option B: Terminal CLI

Run the command-line interface:
```bash
python main.py
```
Follow the interactive prompts to enter a YouTube link or local file path.

---

## 🛠️ Tech Stack

- **Framework & Orchestration**: LangChain Core, LangChain MistralAI, LangChain Chroma
- **LLM & Embeddings**: Mistral AI (`mistral-small-latest`, `mistral-embed`)
- **Speech-to-Text**: OpenAI Whisper, Sarvam AI
- **Vector Database**: ChromaDB
- **Audio & Media**: yt-dlp, PyDub, ffmpeg
- **Frontend / Backend**: HTML5, Vanilla CSS, Vanilla JavaScript, Python HTTP Server

---

## 📄 License

This project is open-source under the MIT License.
