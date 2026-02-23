#下载工具对话框
import os
import requests
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from HtmlAnalyse import *
from Common import *

class ToolDownloader:
	def __init__(self, parent):
		self.parent = parent
		# 创建新窗口
		self.window = tk.Toplevel(parent)
		self.window.title("自由下载工具")
		self.window.geometry("510x140")
		self.window.transient(parent)
		self.window.grab_set()
		self.window.focus_set()
		self.setupUI()
		self.centerWindow()
		self.window.wait_window()

	def centerWindow(self):
		self.window.update_idletasks()
		width = self.window.winfo_width()
		height = self.window.winfo_height()
		x = (self.window.winfo_screenwidth() // 2) - (width // 2)
		y = (self.window.winfo_screenheight() // 2) - (height // 2)
		self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

	def setupUI(self):
		#两列
		ttk.Label(self.window, text="网址：").grid(row=0, column=0, padx=5, pady=(6,3), sticky=tk.W)
		ttk.Label(self.window, text="上级网址：").grid(row=1, column=0, padx=5, pady=3, sticky=tk.W)
		ttk.Label(self.window, text="文件名：").grid(row=2, column=0, padx=5, pady=3, sticky=tk.W)
		self.url_var = tk.StringVar()
		self.url_entry = ttk.Entry(self.window, textvariable=self.url_var)
		self.url_entry.grid(row=0, column=1, padx=(5,16), pady=(6,3), sticky=(tk.W,tk.E))
		self.ref_var = tk.StringVar()
		self.ref_entry = ttk.Entry(self.window, textvariable=self.ref_var)
		self.ref_entry.grid(row=1, column=1, padx=(5,16), pady=3, sticky=(tk.W,tk.E))
		self.name_var = tk.StringVar()
		self.name_entry = ttk.Entry(self.window, textvariable=self.name_var)
		self.name_entry.grid(row=2, column=1, padx=(5,16), pady=3, sticky=(tk.W,tk.E))
		#按钮
		btn_frame = ttk.Frame(self.window)
		btn_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
		self.download_btn=ttk.Button(btn_frame, text="下载", command=self.btn_download)
		self.download_btn.grid(row=0, column=0, padx=5)
		self.exit_btn=ttk.Button(btn_frame, text="退出", command=self.window.destroy)
		self.exit_btn.grid(row=0, column=1, padx=5)
		self.status_var = tk.StringVar()
		self.status_var.set("")
		ttk.Label(btn_frame, textvariable=self.status_var).grid(row=0, column=2, padx=5, pady=10)
		#列宽
		self.window.columnconfigure(1, weight=1)
		self.window.bind("<Map>", self.on_map)
		self.window.bind("<FocusIn>", self.on_focus)
	def on_map(self,event):
		if self.parent.state() in ('iconic', 'withdrawn'):
			self.parent.deiconify()
	def on_focus(self, event):
		if self.window.state() in ('iconic', 'withdrawn'):
			self.window.deiconify()

	def btn_download(self):
		self.download_btn.config(state=tk.DISABLED)
		result=self.real_download()
		if result:
			self.status_var.set("下载成功!")
		else:
			self.status_var.set("下载失败")
		self.download_btn.config(state=tk.NORMAL)
	def real_download(self):
		url=self.url_entry.get()
		ref=self.ref_entry.get()
		name=self.name_entry.get()
		if not HtmlAnalyse.isGoodFileName(name):
			messagebox.showerror("错误","文件名不规范，不应出现..和?*\"<>|:")
			return
		try:
			headers={
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 
				'Referer': ref
			}
			response = requests.get(url, headers=headers)
			with open(name, "wb") as f:
				f.write(response.content)
		except Exception as e:
			messagebox.showerror("错误",f"下载失败：{str(e)}")
			return
		return True

