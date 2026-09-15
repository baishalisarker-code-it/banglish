import os
import mimetypes
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler

RENDER_BACKEND = "https://banglabridge-backend.onrender.com"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class handler(BaseHTTPRequestHandler):
    def _proxy_request(self, target_url):
        try:
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len) if content_len > 0 else None
            req = urllib.request.Request(
                target_url,
                data=body,
                headers={
                    "Content-Type": self.headers.get("Content-Type", "application/json"),
                    "User-Agent": "BanglaBridge-Vercel-Proxy"
                },
                method=self.command
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                self.send_response(resp.getcode())
                self.send_header("Content-Type", resp.headers.get("Content-Type", "application/json"))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(data)
        except Exception as e:
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(f'{{"error": "Backend proxy failed: {str(e)}"}}'.encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_POST(self):
        path = self.path.split("?")[0]
        if path.startswith("/api/"):
            target_url = f"{RENDER_BACKEND}{self.path}"
            self._proxy_request(target_url)
            return
        self.send_response(404)
        self.end_headers()

    def do_GET(self):
        path = self.path.split("?")[0].lstrip("/")
        
        # Proxy API calls
        if path.startswith("api/"):
            target_url = f"{RENDER_BACKEND}/{path}"
            self._proxy_request(target_url)
            return

        # Serve static assets
        if not path or path == "index.html":
            file_name = "index.html"
        else:
            file_name = path

        file_path = os.path.abspath(os.path.join(BASE_DIR, file_name))
        
        # If not found directly, check inside frontend/
        if not os.path.isfile(file_path):
            file_path = os.path.abspath(os.path.join(BASE_DIR, "frontend", file_name))

        # Fallback to index.html for SPA
        if not os.path.isfile(file_path):
            file_path = os.path.join(BASE_DIR, "index.html")

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

            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Cache-Control", "public, max-age=3600")
            self.end_headers()
            with open(file_path, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"File not found")
