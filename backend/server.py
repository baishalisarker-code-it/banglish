"""
BanglaBridge Zero-Dependency HTTP & REST API Server
Serves the modern frontend web app and provides REST API endpoints
for real-time translation, emotion scoring, and sarcasm detection.
"""

import os
import json
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from .pipeline import full_pipeline
from .core.translator import is_nllb_available

def load_env():
    """Loads environment variables from .env file into os.environ if present."""
    env_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
    if os.path.exists(env_file):
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k not in os.environ:
                            os.environ[k] = v
        except Exception:
            pass

load_env()

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

PRESETS = [
    {
        "id": "mixed-banglish",
        "title": "Mixed Banglish + Script",
        "badge": "Code-Switching",
        "direction": "auto",
        "text": "আমি যাবো। কিন্তু ami bhalo achi na। তুমি কেমন আছো?"
    },
    {
        "id": "deadpan-sarcasm",
        "title": "Deadpan Sarcasm & Irony",
        "badge": "Sarcasm ⚠️",
        "direction": "auto",
        "text": "বাহ! তোমার কাজটা খুব ভালো হয়েছে। এই কাজটা ফালতু হয়ে গেছে।"
    },
    {
        "id": "romanized-colloquial",
        "title": "Pure Banglish Conversation",
        "badge": "Romanized",
        "direction": "auto",
        "text": "ami bhalo achi kintu meeting ta miss korte chai na"
    },
    {
        "id": "cultural-slang",
        "title": "Colloquial Slang & Idiom",
        "badge": "Cultural Nuance",
        "direction": "auto",
        "text": "এই কাজটা ফালতু হয়ে গেছে, চারিদিকে শুধু ঝামেলা।"
    },
    {
        "id": "english-to-bengali",
        "title": "English to Bengali",
        "badge": "En → Bn",
        "direction": "en-bn",
        "text": "How are you today? Thank you very much for your great work."
    }
]

class BanglaBridgeHandler(BaseHTTPRequestHandler):
    """Custom HTTP Request Handler serving frontend and REST API."""

    def _set_headers(self, status_code=200, content_type="application/json"):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        allowed_origin = os.environ.get("ALLOWED_ORIGIN", "*")
        self.send_header("Access-Control-Allow-Origin", allowed_origin)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self._set_headers(204)

    def do_GET(self):
        """Handle static files and GET API routes."""
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            data = {
                "status": "healthy",
                "app": "BanglaBridge",
                "version": "1.0.0",
                "nllb_available": is_nllb_available()
            }
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return

        if path == "/api/presets":
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps(PRESETS).encode("utf-8"))
            return

        # Static file serving
        rel_path = path.lstrip("/")
        if not rel_path or rel_path == "index.html":
            file_path = os.path.join(FRONTEND_DIR, "index.html")
        else:
            file_path = os.path.join(FRONTEND_DIR, rel_path)

        # Security check: ensure within FRONTEND_DIR
        file_path = os.path.abspath(file_path)
        if not file_path.startswith(FRONTEND_DIR) or not os.path.isfile(file_path):
            # Fallback to index.html for SPA routing
            file_path = os.path.join(FRONTEND_DIR, "index.html")

        if os.path.exists(file_path) and os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = "application/octet-stream"
            if file_path.endswith(".js"):
                mime_type = "application/javascript"
            elif file_path.endswith(".css"):
                mime_type = "text/css"
            elif file_path.endswith(".html"):
                mime_type = "text/html; charset=utf-8"

            self._set_headers(200, mime_type)
            with open(file_path, "rb") as f:
                self.wfile.write(f.read())
        else:
            self._set_headers(404, "application/json")
            self.wfile.write(json.dumps({"error": "File not found"}).encode("utf-8"))

    def do_POST(self):
        """Handle POST API routes."""
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/translate":
            try:
                content_len = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_len).decode("utf-8")
                payload = json.loads(body) if body else {}

                text = payload.get("text", "")
                direction = payload.get("direction", "auto")

                result = full_pipeline(text=text, direction=direction)
                self._set_headers(200, "application/json")
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self._set_headers(500, "application/json")
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
            return

        self._set_headers(404, "application/json")
        self.wfile.write(json.dumps({"error": f"Path '{path}' not recognized"}).encode("utf-8"))

    def log_message(self, format, *args):
        """Suppress noisy request logs, keeping terminal clean."""
        # Print only API requests or errors
        if len(args) > 0 and isinstance(args[0], str) and ("/api/" in args[0] or "500" in args[0]):
            super().log_message(format, *args)

def start_server(port: int = 8080, host: str = "0.0.0.0"):
    """Starts the HTTP server on specified port and host interface."""
    server_address = (host, port)
    httpd = HTTPServer(server_address, BanglaBridgeHandler)
    print(f"BanglaBridge Server listening on http://{host}:{port}")
    return httpd

if __name__ == "__main__":
    import sys
    # Read PORT and HOST from environment (standard on Render, Railway, Heroku) or CLI
    port = int(os.environ.get("PORT", sys.argv[1] if len(sys.argv) > 1 else 8080))
    host = os.environ.get("HOST", "0.0.0.0")
    server = start_server(port=port, host=host)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nBanglaBridge Server stopped.")
        server.server_close()


