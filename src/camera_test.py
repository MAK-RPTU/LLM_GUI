# from http.server import SimpleHTTPRequestHandler, HTTPServer

# class CORSRequestHandler(SimpleHTTPRequestHandler):
#     def end_headers(self):
#         self.send_header("Access-Control-Allow-Origin", "*")
#         super().end_headers()

# httpd = HTTPServer(("0.0.0.0", 8080), CORSRequestHandler)
# httpd.serve_forever()

# simple Python HTTP server with MIME types
from http.server import HTTPServer, SimpleHTTPRequestHandler
import mimetypes

mimetypes.add_type('application/vnd.apple.mpegurl', '.m3u8')
mimetypes.add_type('video/MP2T', '.ts')

server_address = ('', 8080)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
print("Serving on port 8080")
httpd.serve_forever()
