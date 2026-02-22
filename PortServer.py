#自动寻找可用端口并启动HTTP服务器的工具类。
#默认从1055开始尝试，最多尝试100个端口。
#可修改PortServer对象的on_request_start、on_request_end做一些调整
import socket
import threading
import atexit
from http.server import HTTPServer, SimpleHTTPRequestHandler
import functools

class PortServer:
	def __init__(self, start_port, max_attempts=100):
		self.start_port = start_port
		self.max_attempts = max_attempts
		self.port = None
		self.server = None
		self.thread = None
		self.on_request_start = None
		self.on_request_end = None
	def find_free_port(self):
		# 尝试找到可用端口
		for port in range(self.start_port, self.start_port + self.max_attempts):
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				try:
					s.bind(('localhost', port))
					return port
				except OSError:
					continue  # 端口被占用，继续尝试
		return -1
	def start(self, directory):
		#在指定目录启动HTTP服务器, 返回端口
		self.port = self.find_free_port()
		if self.port==-1:
			return
		#两个函数能动态调整
		def real_request_start(client_addr, command, path):
			if self.on_request_start:
				self.on_request_start(client_addr, command, path)
		def real_request_end(client_addr, command, path, code):
			if self.on_request_end:
				self.on_request_end(client_addr, command, path, code)

		handler = functools.partial(CallbackHTTPRequestHandler,
					directory=directory,
					on_request_start=real_request_start,
					on_request_end=real_request_end
					)
		self.server = HTTPServer(('localhost', self.port), handler)
		# 启动服务器
		self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
		self.thread.start()
		# 程序退出时关闭服务器
		atexit.register(self.stop)
	def stop(self):
		# 停止服务器
		if self.server:
			self.server.shutdown()
			self.server.server_close()
			self.server = None

class CallbackHTTPRequestHandler(SimpleHTTPRequestHandler):
	def __init__(self, *args, directory=None, on_request_start=None, on_request_end=None, **kwargs):
		self.on_request_start = on_request_start
		self.on_request_end = on_request_end
		super().__init__(*args, **kwargs, directory=directory)

	def parse_request(self):
		# 触发开始回调（此时只知客户端地址和请求行，状态码未知）
		result = super().parse_request()
		if self.on_request_start and result:
			self.on_request_start(self.client_address, self.command, self.path)
		return result

	def log_request(self, code='-', size='-'):
		# 触发结束回调（状态码已知）
		if self.on_request_end:
			self.on_request_end(self.client_address, self.command, self.path, code)
		super().log_request(code, size)

	def log_message(self, format, *args):
		#super().log_message(format, *args) #注释此行即不再print
		pass

	def handle_one_request(self):
		try:
			super().handle_one_request()
		except Exception as e:
			print(f"连接波动: {str(e)}")