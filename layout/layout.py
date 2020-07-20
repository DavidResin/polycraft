from http.server import HTTPServer, BaseHTTPRequestHandler
import os, ssl
from io import BytesIO
from ast import literal_eval

class LayoutHTTPRequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		self.wfile.write(b'Hello, world!')
		
	def do_POST(self):
		content_length = int(self.headers["Content-Length"])
		body = self.rfile.read(content_length)
		self.send_response(200)
		self.end_headers()
		response = BytesIO()
		response.write(b'This is POST request. ')
		response.write(b'Received: ')
		response.write(body)
		self.wfile.write(response.getvalue())

		d = literal_eval(body.decode('utf-8'))
		x = int(d["x"])
		z = int(d["z"])
		y = 100

		cmd = f"ssh mc-server@owo.miomjon.ch \"/usr/bin/screen -p 0 -S mc-server -X eval 'stuff \"'\"'\"fill {x} {y} {z} {x} {y} {z} light_blue_concrete_powder keep\"'\"'\"\\015'\""
		os.system(cmd)
		print(d)

	def do_OPTIONS(self):
	    self.send_response(200, "ok")
	    self.send_header('Access-Control-Allow-Origin', '*')
	    self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
	    self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
	    self.send_header("Access-Control-Allow-Headers", "Content-Type")
	    self.end_headers()

httpd = HTTPServer(('localhost', 8000), LayoutHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile="server.pem", server_side=True)
httpd.serve_forever()