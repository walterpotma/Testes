import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# Caminho externo ao checkout; o volume é fornecido pela plataforma.
VOLUME_PATH = Path(os.environ.get("VOLUME_PATH", "/mnt/hexon-data"))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.respond(200, {"status": "ok"})
            return
        if self.path != "/":
            self.respond(404, {"error": "Not found"})
            return
        try:
            files = sorted(item.name for item in VOLUME_PATH.iterdir())
            self.respond(200, {"app": "Hexon — Python", "volume_path": str(VOLUME_PATH), "mounted": True, "files": files})
        except OSError as error:
            self.respond(503, {"app": "Hexon — Python", "volume_path": str(VOLUME_PATH), "mounted": False, "error": str(error)})

    def respond(self, status, payload):
        data = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), Handler).serve_forever()
