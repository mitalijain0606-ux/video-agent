"""
Video Agent — Zero-Dependency Web Backend API Server
Uses Python's built-in http.server so it runs instantly without needing extra pip installs!
Serves the top-tier web interface and exposes /api/process & /api/chat endpoints.
"""

import os
import json
import traceback
import mimetypes
from http.server import HTTPServer, ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from dotenv import load_dotenv

# Pipeline imports
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

load_dotenv(override=True)

# Global active session state
session_data = {
    "result": None,
    "rag_chain": None,
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")


class VideoAgentRequestHandler(BaseHTTPRequestHandler):

    def _send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, message, status=400):
        self._send_json({"status": "error", "detail": str(message)}, status=status)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ["/", "/index.html"]:
            file_path = os.path.join(STATIC_DIR, "index.html")
        elif path.startswith("/static/"):
            rel_path = path[len("/static/"):].lstrip("/")
            file_path = os.path.join(STATIC_DIR, rel_path)
        else:
            file_path = os.path.join(STATIC_DIR, path.lstrip("/"))

        if os.path.exists(file_path) and os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            mime_type = mime_type or "application/octet-stream"

            with open(file_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            payload = json.loads(post_data.decode("utf-8"))
        except Exception:
            payload = {}

        if path == "/api/process":
            source = payload.get("source", "").strip()
            language = payload.get("language", "english")

            if not source:
                return self._send_error("Please provide a valid YouTube URL or local file path.", 400)

            try:
                # 1. Audio processing
                chunks = process_input(source)

                # 2. Transcription
                transcript = transcribe_all(chunks, language)

                # 3. Title
                title = generate_title(transcript)

                # 4. Summary
                summary_text = summarize(transcript)

                # 5. Extractors
                action_items_raw = extract_action_items(transcript)
                decisions_raw = extract_key_decisions(transcript)
                questions_raw = extract_questions(transcript)

                # 6. RAG Chain
                rag_chain = build_rag_chain(transcript)

                def parse_items(raw):
                    if isinstance(raw, list):
                        return raw
                    if isinstance(raw, str):
                        return [line.strip("- *•").strip() for line in raw.split("\n") if line.strip()]
                    return []

                result = {
                    "title": title,
                    "transcript": transcript,
                    "summary": summary_text,
                    "action_items": parse_items(action_items_raw),
                    "key_decisions": parse_items(decisions_raw),
                    "open_questions": parse_items(questions_raw),
                }

                session_data["result"] = result
                session_data["rag_chain"] = rag_chain

                return self._send_json({"status": "success", "data": result})

            except Exception as e:
                traceback.print_exc()
                err_msg = str(e)
                if "401" in err_msg or "Unauthorized" in err_msg:
                    err_msg = "Mistral API Key is unauthorized or invalid (401 Unauthorized). Please check your MISTRAL_API_KEY in .env."
                return self._send_error(err_msg, 500)

        elif path == "/api/chat":
            question = payload.get("question", "").strip()
            if not question:
                return self._send_error("Question cannot be empty.", 400)

            rag_chain = session_data.get("rag_chain")
            if not rag_chain:
                return self._send_error("No active video session found. Please process a video first.", 400)

            try:
                answer = ask_question(rag_chain, question)
                return self._send_json({"status": "success", "answer": answer})
            except Exception as e:
                traceback.print_exc()
                return self._send_error(str(e), 500)

        else:
            self._send_error("Endpoint not found", 404)


def run_server(port=8000):
    server_address = ("", port)
    httpd = ThreadingHTTPServer(server_address, VideoAgentRequestHandler)
    print(f"\n=======================================================")
    print(f" 🚀 Video Agent Top 1% Web Application Running!")
    print(f" 👉 Open your browser at: http://localhost:{port}")
    print(f"=======================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped.")


if __name__ == "__main__":
    run_server(8000)
