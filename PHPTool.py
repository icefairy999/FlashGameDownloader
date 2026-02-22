#用于调用php
import requests
from tkinter import messagebox

class PHPTool:
	# 模拟 $.ajax 请求
	@staticmethod
	def callPhpApi(url, data=None, method="GET", headers=None):
		#向 PHP 接口发送请求并获取响应
		#参数:
		#	url: PHP 接口的 URL
		#	data: 要发送的数据（字典形式）
		#	method: 请求方法 ("GET" 或 "POST")
		#	headers: 自定义请求头
		if headers is None:
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
				'Accept': 'application/json, text/javascript, */*; q=0.01',
				'X-Requested-With': 'XMLHttpRequest',  # 表明这是一个 AJAX 请求
				'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			}
		try:
			# 根据请求方法发送请求
			if method.upper() == "GET":
				response = requests.get(url, params=data, headers=headers)
			else:
				response = requests.post(url, data=data, headers=headers)
			# 检查请求是否成功
			if response.status_code == 200:
				# 尝试解析 JSON 响应（假设 PHP 返回 JSON）
				try:
					return response.json()
				except ValueError:
					# 如果不是 JSON，返回原始文本
					return response.text
			else:
				messagebox.showerror("错误", f"php请求失败，状态码: {response.status_code}")
				return None
		except Exception as e:
			messagebox.showerror("错误", f"php请求过程中发生错误: {str(e)}")
			return None