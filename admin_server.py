import http.server
import socketserver
import json
import os
import subprocess
import gzip
import base64
import sys
import webbrowser
import threading
import time

DEFAULT_PORT = int(os.environ.get("PORT", 8000))

# Admin Portal Credentials (can be overridden via environment variables)
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "adminpassword123")

def check_auth(headers):
    auth_header = headers.get('Authorization')
    if not auth_header:
        return False
    try:
        auth_type, encoded = auth_header.split(' ', 1)
        if auth_type.lower() != 'basic':
            return False
        decoded = base64.b64decode(encoded.strip()).decode('utf-8')
        username, password = decoded.split(':', 1)
        return username == ADMIN_USERNAME and password == ADMIN_PASSWORD
    except Exception:
        return False

class AdminHandler(http.server.SimpleHTTPRequestHandler):
    def send_auth_prompt(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Delhi Police Admin Portal"')
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'<!DOCTYPE html><html><head><title>401 Unauthorized</title></head><body style="font-family:sans-serif; text-align:center; padding-top:50px;"><h1>401 Unauthorized</h1><p>Authentication required to access the Admin Portal.</p></body></html>')

    def translate_path(self, path):
        clean_path = path.split('?')[0]
        
        # 1. Admin Portal assets (e.g. css/js inside admin/)
        if clean_path.startswith('/admin/'):
            rel = clean_path[7:] # strip '/admin/'
            return os.path.abspath(os.path.join('admin', rel))

        # 2. QR Code assets
        if clean_path.startswith('/qr/'):
            rel = clean_path[4:] # strip '/qr/'
            return os.path.abspath(os.path.join('qr', rel))

        # 3. Public Web App assets (served from src/)
        if clean_path == '/':
            return os.path.abspath('src/index.html')
        
        rel_path = clean_path.lstrip('/')
        target_in_src = os.path.abspath(os.path.join('src', rel_path))

        if os.path.isdir(target_in_src):
            return os.path.join(target_in_src, 'index.html')

        return target_in_src

    def do_GET(self):
        clean_path = self.path.split('?')[0]
        
        # Handle /admin and /admin/
        if clean_path in ('/admin', '/admin/'):
            if not check_auth(self.headers):
                self.send_auth_prompt()
                return
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            with open('admin/index.html', 'rb') as f:
                self.wfile.write(f.read())
            return

        # Enforce authentication on all /admin/ subroutes
        if clean_path.startswith('/admin/'):
            if not check_auth(self.headers):
                self.send_auth_prompt()
                return

        # Enforce authentication on /api/get-content
        if clean_path == '/api/get-content':
            if not check_auth(self.headers):
                self.send_auth_prompt()
                return
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            with open('content/content.json', 'rb') as f:
                self.wfile.write(f.read())
            return
        
        return super().do_GET()

    def do_POST(self):
        clean_path = self.path.split('?')[0]

        if clean_path == '/api/save-content':
            if not check_auth(self.headers):
                self.send_auth_prompt()
                return

            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                
                # Save to content/content.json
                with open('content/content.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                # Run build.py
                res = subprocess.run([sys.executable, 'build.py'], capture_output=True, text=True)
                if res.returncode != 0:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'error', 'message': res.stderr}).encode('utf-8'))
                    return

                # Calculate payload size
                total_gz = 0
                for root, _, files in os.walk('src'):
                    for file in files:
                        if file.endswith(('.html', '.css', '.js', '.json', '.webmanifest')):
                            path = os.path.join(root, file)
                            with open(path, 'rb') as pf:
                                total_gz += len(gzip.compress(pf.read()))

                gz_kb = round(total_gz / 1024, 2)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'status': 'ok',
                    'message': 'Content saved and site pre-rendered cleanly!',
                    'gzipped_kb': gz_kb
                }).encode('utf-8'))

            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode('utf-8'))
            return

        self.send_error(404, "Endpoint not found")

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

def open_browser_delayed(url):
    time.sleep(1.2)
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Could not auto-open browser: {e}")

def main():
    httpd = None
    actual_port = DEFAULT_PORT
    ports_to_try = [DEFAULT_PORT, 8000, 8081, 8088, 3000, 5000, 8888]
    
    for p in ports_to_try:
        try:
            httpd = ThreadedHTTPServer(("127.0.0.1", p), AdminHandler)
            actual_port = p
            break
        except OSError:
            continue

    if not httpd:
        try:
            httpd = ThreadedHTTPServer(("", 0), AdminHandler)
            actual_port = httpd.socket.getsockname()[1]
        except Exception as e:
            print(f"Fatal error starting server: {e}")
            sys.exit(1)

    url = f"http://localhost:{actual_port}/"
    print(f"=========================================================")
    print(f" Law & Order App Server active on {url}")
    print(f" Public Web App:   {url} (No auth needed)")
    print(f" Admin Portal:     http://localhost:{actual_port}/admin/")
    print(f" Admin Credentials: Username: {ADMIN_USERNAME} | Password: {ADMIN_PASSWORD}")
    print(f"=========================================================")

    threading.Thread(target=open_browser_delayed, args=(url,), daemon=True).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped cleanly.")

if __name__ == "__main__":
    main()
