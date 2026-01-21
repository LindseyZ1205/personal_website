from __future__ import annotations

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/api/health":
            payload = {"status": "ok"}
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/":
            self.path = "/index.html"

        return super().do_GET()


def main() -> None:
    host = "127.0.0.1"
    port = 8080

    httpd = ThreadingHTTPServer(
        (host, port),
        lambda *args, **kwargs: Handler(*args, directory=".", **kwargs),
    )

    print(f"Serving on http://{host}:{port}")
    print(f"Health check: http://{host}:{port}/api/health")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
