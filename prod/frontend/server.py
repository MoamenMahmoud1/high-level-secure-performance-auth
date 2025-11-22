# server_https.py
import http.server
import ssl

port = 5500
handler = http.server.SimpleHTTPRequestHandler

httpd = http.server.HTTPServer(('127.0.0.1', port), handler)

# إنشاء SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

# ربط الـ context مع الـ socket
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"Serving HTTPS on 127.0.0.1:{port}")
httpd.serve_forever()
