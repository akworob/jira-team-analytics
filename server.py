#!/usr/bin/env python3
"""
Simple HTTP server with CORS proxy for JIRA Dashboard
Run with: python3 server.py
Access at: http://localhost:8000
"""

import http.server
import socketserver
import json
import urllib.request
import urllib.error
from urllib.parse import urlparse, parse_qs
import base64
import sys

PORT = 8000

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # Check if this is a proxy request to JIRA
        if self.path.startswith('/jira-proxy'):
            self.handle_jira_proxy()
        else:
            # Serve static files
            super().do_GET()

    def handle_jira_proxy(self):
        try:
            # Parse query parameters
            parsed_path = urlparse(self.path)
            params = parse_qs(parsed_path.query)

            jira_url = params.get('url', [''])[0]
            auth_header = self.headers.get('X-JIRA-Auth', '')

            if not jira_url or not auth_header:
                self.send_error(400, 'Missing url or X-JIRA-Auth header')
                return

            # Create request to JIRA
            req = urllib.request.Request(jira_url)
            req.add_header('Authorization', auth_header)
            req.add_header('Accept', 'application/json')
            req.add_header('Content-Type', 'application/json')

            # Make request
            with urllib.request.urlopen(req) as response:
                data = response.read()

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(data)

        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_msg = json.dumps({'error': str(e), 'code': e.code})
            self.wfile.write(error_msg.encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_msg = json.dumps({'error': str(e)})
            self.wfile.write(error_msg.encode())

    def log_message(self, format, *args):
        # Custom logging
        sys.stdout.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format % args))


def run_server():
    with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
        print(f"🚀 JIRA Dashboard Server running at http://localhost:{PORT}")
        print(f"📊 Open http://localhost:{PORT}/jira_dashboard.html in your browser")
        print(f"Press Ctrl+C to stop the server\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n⛔ Server stopped")
            sys.exit(0)


if __name__ == "__main__":
    run_server()
