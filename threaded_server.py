import http.server
import socketserver
import os
import sys

PORT = 8123
DIRECTORY = "/home/ubuntu/dataprep/thumbnails/asset/2d/"

if not os.path.exists(DIRECTORY):
    print(f"❌ FATAL: Image directory not found: {DIRECTORY}")
    sys.exit(1)

try:
    os.chdir(DIRECTORY)
    print(f"📂 Serving images from: {DIRECTORY}")
except Exception as e:
    print(f"❌ Error accessing directory: {e}")
    sys.exit(1)

# Robust Handler (Prevents crashes on 404s)
Handler = http.server.SimpleHTTPRequestHandler
class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

print(f"🚀 Image Server running on port {PORT}")
with ThreadedHTTPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
