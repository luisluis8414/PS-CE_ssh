from http.server import HTTPServer, BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'''
<!DOCTYPE html>
<html>
<head><title>SSH Tutorial</title></head>
<body style="font-family: monospace; text-align: center; padding: 50px;">
    <h1>Hello from the server!</h1>
</body>
</html>
''')
    
    def log_message(self, format, *args):
        print(f"Request received: {args[0]}")

print("Server running on port 8080...")
print("Press Ctrl+C to stop")
HTTPServer(('127.0.0.1', 8080), MyHandler).serve_forever()