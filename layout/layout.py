from http.server import HTTPServer, BaseHTTPRequestHandler
import os, ssl, signal
from io import BytesIO
from ast import literal_eval

template = "/usr/bin/screen -p 0 -S mc-server -X eval 'stuff \"'\"'\"execute at MCRaisin run fill {0} {1} {2} {0} {1} {2} light_blue_concrete_powder keep\"'\"'\"\\015'; "
prefix = "ssh mc-server@owo.miomjon.ch \""
cmd = prefix
count = 0

class LayoutHTTPRequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		self.wfile.write(b'Hello, world!')
		
	def do_POST(self):
		global cmd, count
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
		y = "~" #100

		cmd += template.format(x, y, z)
		count += 1

	def do_OPTIONS(self):
	    self.send_response(200, "ok")
	    self.send_header('Access-Control-Allow-Origin', '*')
	    self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
	    self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
	    self.send_header("Access-Control-Allow-Headers", "Content-Type")
	    self.end_headers()

	def log_message(self, format, *args):
		return

	def itimer_handler(signum, frame):
		global cmd, count
		if cmd != prefix:
			os.system(cmd[:-2] + "\"")
			cmd = prefix
			print(str(count), "blocks placed")
			count = 0

	signal.signal(signal.SIGALRM, itimer_handler)
	signal.setitimer(signal.ITIMER_REAL, 5, 5)

httpd = HTTPServer(('localhost', 8000), LayoutHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile="server.pem", server_side=True)
httpd.serve_forever()