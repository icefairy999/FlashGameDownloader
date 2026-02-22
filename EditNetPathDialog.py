#更改网络路径的那个对话框
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from GameDownloader import *
from HtmlAnalyse import *
from Common import *

class EditNetPathDialog:
	def __init__(self, parent, item, gd, confirmCallback):
		self.parent = parent
		self.item = item
		self.gd = gd
		self.confirmCallback=confirmCallback
		self.inirst=IniResult.fromFile(item.iniFullPath,item.folderExt)
		# 创建新窗口
		self.window = tk.Toplevel(parent)
		self.window.title("修改信息")
		self.window.geometry("510x260")
		self.window.transient(parent)
		self.window.grab_set()
		self.window.focus_set()
		self.setupUI()
		self.centerWindow()
		self.readIniAndSet()
		self.window.wait_window()

	def centerWindow(self):
		self.window.update_idletasks()
		width = self.window.winfo_width()
		height = self.window.winfo_height()
		x = (self.window.winfo_screenwidth() // 2) - (width // 2)
		y = (self.window.winfo_screenheight() // 2) - (height // 2)
		self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

	def setupUI(self):
		#第一行
		type_frame = ttk.Frame(self.window)
		type_frame.grid(row=0, column=0, padx=10, pady=(12,5), sticky=tk.W)
		ttk.Label(type_frame, text="信息类别：",width=8).grid(row=0, column=0, padx=(5,0))
		self.type_var = tk.StringVar()
		self.type_entry = ttk.Entry(type_frame, textvariable=self.type_var, state='readonly',width=10)
		self.type_entry.grid(row=0, column=1, padx=5)
		ttk.Label(type_frame, text="（由文件夹后缀的s或h决定，对应\"swf\"与\"htm\"）").grid(
			row=0, column=2, padx=5)

		#网络路径
		netPath_frame = ttk.Frame(self.window)
		netPath_frame.grid(row=1, column=0, padx=10, pady=(5,5), sticky=(tk.W,tk.E))
		ttk.Label(netPath_frame, text="网络路径：",width=8).grid(
			row=0, column=0, padx=(5,0))
		self.path_var = tk.StringVar()
		self.path_entry = ttk.Entry(netPath_frame, textvariable=self.path_var)
		self.path_entry.grid(row=0, column=1, padx=(5,12), sticky=(tk.W,tk.E))
		netPath_frame.columnconfigure(1, weight=1)

		# 宽高
		gameSize_frame = ttk.Frame(self.window)
		gameSize_frame.grid(row=2, column=0, padx=10, pady=(5,5), sticky=tk.W)
		ttk.Label(gameSize_frame, text="窗口宽：",width=8).grid(row=0, column=0, padx=(5,0))
		self.gameWidth_var = tk.StringVar()
		self.gameWidth_entry = ttk.Entry(gameSize_frame, textvariable=self.gameWidth_var,width=10)
		self.gameWidth_entry.grid(row=0, column=1, padx=(5,30))
		ttk.Label(gameSize_frame, text="窗口高：",width=8).grid(row=0, column=2, padx=(30,0))
		self.gameHeight_var = tk.StringVar()
		self.gameHeight_entry = ttk.Entry(gameSize_frame, textvariable=self.gameHeight_var,width=10)
		self.gameHeight_entry.grid(row=0, column=3, padx=5)

		#swf用:新页面与页面路径
		#新页面复选框
		isNewPage_frame=ttk.Frame(self.window)
		isNewPage_frame.grid(row=3, column=0, padx=10, pady=(5,5), sticky=tk.W)
		ttk.Label(isNewPage_frame, text="新页面：",width=8).grid(row=0, column=0, padx=(5,20))
		self.isNewPage_var = tk.StringVar()
		self.isNewPage_rb1=ttk.Radiobutton(isNewPage_frame, text="有", variable=self.isNewPage_var, value="有", command=self.on_selection_changed)
		self.isNewPage_rb1.grid(row=0, column=1, padx=20)
		self.isNewPage_rb2=ttk.Radiobutton(isNewPage_frame, text="无", variable=self.isNewPage_var, value="无", command=self.on_selection_changed)
		self.isNewPage_rb2.grid(row=0, column=2, padx=20)
		self.isNewPage_rb3=ttk.Radiobutton(isNewPage_frame, text="未知", variable=self.isNewPage_var, value="未知", command=self.on_selection_changed)
		self.isNewPage_rb3.grid(row=0, column=3, padx=20)
		#页面路径
		newPageUrl_frame=ttk.Frame(self.window)
		newPageUrl_frame.grid(row=4, column=0, padx=10, pady=(5,5), sticky=(tk.W,tk.E))
		ttk.Label(newPageUrl_frame, text="新页路径：",width=8).grid(row=0, column=0, padx=(5,0))
		self.newPageUrl_var = tk.StringVar()
		self.newPageUrl_entry = ttk.Entry(newPageUrl_frame, textvariable=self.newPageUrl_var)
		self.newPageUrl_entry.grid(row=0, column=1, padx=(5,12), sticky=(tk.W,tk.E))
		newPageUrl_frame.columnconfigure(1, weight=1)

		#自动识别按钮
		netPathAuto_frame = ttk.Frame(self.window)
		netPathAuto_frame.grid(row=5, column=0, padx=10, pady=(5,5), sticky=tk.W)
		self.netPathAuto_btn=ttk.Button(netPathAuto_frame, text="自动识别", command=self.btn_autoDetect)
		self.netPathAuto_btn.grid(row=0, column=0, padx=5)
		self.status_var = tk.StringVar()
		self.status_var.set("")
		status_bar = ttk.Label(netPathAuto_frame, textvariable=self.status_var, anchor=tk.W)
		status_bar.grid(row=0, column=1, padx=5)

		#确定取消
		button_frame = ttk.Frame(self.window)
		button_frame.grid(row=6, column=0, pady=(5,5), sticky=tk.W)
		self.confirm_btn=ttk.Button(button_frame, text="确定", command=self.btn_confirm)
		self.confirm_btn.grid(row=0, column=0, padx=(15,10))
		self.cancel_btn=ttk.Button(button_frame, text="取消", command=self.window.destroy)
		self.cancel_btn.grid(row=0, column=1, padx=10)
		self.reset_btn=ttk.Button(button_frame, text="重置", command=self.btn_reset)
		self.reset_btn.grid(row=0, column=2, padx=10)

		self.window.columnconfigure(0, weight=1)
	def on_selection_changed(self):
		self.changeNewPageRadioBtn()
	def btn_reset(self):
		self.readIniAndSet()

	def btn_autoDetect(self):
		result=self.real_autoDetect()
		if result:
			self.status_var.set("（自动识别网络路径与新页信息成功！）")
		else:
			self.status_var.set("自动识别网络路径与新页信息失败")
	def real_autoDetect(self):
		if self.item.gameAppendix==None:
			messagebox.showinfo("提示","自动识别需要看后缀(如_a82589)，此处没有，无法识别")
			return
		result=self.gd.getSWFPathWithAppendix(self.item.gameAppendix)
		#分情况
		if not result:
			#注:此前已经有很多错误提示了，无需再弹对话框
			return
		if self.item.folderExt=='.swf':
			#自己是swf
			if result.type!='swf':
				messagebox.showerror("错误",f"文件夹名显示这是swf文件，但网站的游戏不是flash游戏，而是{result.type}")
				return
			self.path_var.set(result.swfUrl)
			self.gameWidth_var.set(str(result.gameWidth))
			self.gameHeight_var.set(str(result.gameHeight))
			if result.isNewPage:
				self.isNewPage_var.set("有")
				self.newPageUrl_var.set(result.newPageUrl)
			else:
				self.isNewPage_var.set("无")
				self.newPageUrl_var.set("")
			self.changeNewPageRadioBtn()
			return True
		elif self.item.folderExt=='.htm':
			#自己是htm
			self.path_var.set(result.newPageUrl)
			self.gameWidth_var.set(str(result.gameWidth))
			self.gameHeight_var.set(str(result.gameHeight))
			return True
		else:
			messagebox.showerror("错误",f"未知的文件夹后缀{self.item.folderExt}")
			return
	def btn_confirm(self):
		result=self.saveIniFile()
		if result:
			self.confirmCallback()
			self.window.destroy()

	def saveIniFile(self):
		if self.inirst.type=="unknown":
			self.inirst.netPath=self.path_var.get()
		elif self.inirst.type=="swf":
			self.inirst.netPath=self.path_var.get()
			try:
				temp=int(self.gameWidth_entry.get())
			except Exception:
				temp=-999
			if temp>0:
				self.inirst.width=temp
			else:
				self.inirst.width=-1
			try:
				temp=int(self.gameHeight_entry.get())
			except Exception:
				temp=-999
			if temp>0:
				self.inirst.height=temp
			else:
				self.inirst.height=-1
			if self.isNewPage_var.get()=="有":
				self.inirst.isNewPage=1
				self.inirst.newPageUrl=self.newPageUrl_var.get()
			elif self.isNewPage_var.get()=="无":
				self.inirst.isNewPage=0
				self.inirst.newPageUrl=""
			else:
				self.inirst.isNewPage=-1
				self.inirst.newPageUrl=""
		elif self.inirst.type=="htm":
			self.inirst.netPath=self.path_var.get()
			try:
				temp=int(self.gameWidth_entry.get())
			except Exception:
				temp=-999
			if temp>0:
				self.inirst.width=temp
			else:
				self.inirst.width=-1
			try:
				temp=int(self.gameHeight_entry.get())
			except Exception:
				temp=-999
			if temp>0:
				self.inirst.height=temp
			else:
				self.inirst.height=-1
		try:
			self.inirst.WriteFile()
		except Exception as e:
			messagebox.showerror("错误", f"写入文件失败: {str(e)}")
			return
		return True
	def readIniAndSet(self):
		self.inirst.readFile()
		# 强制调整
		if self.item.folderExt==".swf":
			self.inirst.type="swf"
		elif self.item.folderExt==".htm":
			self.inirst.type="htm"
		else:
			self.inirst.type="unknown"
		# 分类讨论
		self.type_var.set(self.inirst.type)
		if self.inirst.type=="unknown":
			self.path_entry.config(state=tk.NORMAL)
			self.gameWidth_entry.config(state=tk.DISABLED)
			self.gameHeight_entry.config(state=tk.DISABLED)
			self.isNewPage_rb1.config(state=tk.DISABLED)
			self.isNewPage_rb2.config(state=tk.DISABLED)
			self.isNewPage_rb3.config(state=tk.DISABLED)
			self.newPageUrl_entry.config(state=tk.DISABLED)
			self.netPathAuto_btn.config(state=tk.NORMAL)
			#
			self.path_var.set(self.inirst.netPath)
			#
		elif self.inirst.type=="swf":
			self.path_entry.config(state=tk.NORMAL)
			self.gameWidth_entry.config(state=tk.NORMAL)
			self.gameHeight_entry.config(state=tk.NORMAL)
			self.isNewPage_rb1.config(state=tk.NORMAL)
			self.isNewPage_rb2.config(state=tk.NORMAL)
			self.isNewPage_rb3.config(state=tk.NORMAL)
			#self.newPageUrl_entry.config(state=tk.DISABLED)
			self.netPathAuto_btn.config(state=tk.NORMAL)
			#
			self.path_var.set(self.inirst.netPath)
			self.gameWidth_var.set(str(self.inirst.width))
			self.gameHeight_var.set(str(self.inirst.height))
			if self.inirst.isNewPage==1:
				self.isNewPage_var.set("有")
				self.newPageUrl_var.set(self.inirst.newPageUrl)
			elif self.inirst.isNewPage==0:
				self.isNewPage_var.set("无")
				self.newPageUrl_var.set("")
			else:
				self.inirst.isNewPage=-1
				self.isNewPage_var.set("未知")
				self.newPageUrl_var.set("")
			self.changeNewPageRadioBtn()
			#
		elif self.inirst.type=="htm":
			self.path_entry.config(state=tk.NORMAL)
			self.gameWidth_entry.config(state=tk.NORMAL)
			self.gameHeight_entry.config(state=tk.NORMAL)
			self.isNewPage_rb1.config(state=tk.DISABLED)
			self.isNewPage_rb2.config(state=tk.DISABLED)
			self.isNewPage_rb3.config(state=tk.DISABLED)
			self.newPageUrl_entry.config(state=tk.DISABLED)
			self.netPathAuto_btn.config(state=tk.NORMAL)
			#
			self.path_var.set(self.inirst.netPath)
			self.gameWidth_var.set(str(self.inirst.width))
			self.gameHeight_var.set(str(self.inirst.height))
			#
	def changeNewPageRadioBtn(self):
		if self.isNewPage_var.get()=="有":
			self.newPageUrl_entry.config(state=tk.NORMAL)
		else:
			self.newPageUrl_entry.config(state=tk.DISABLED)

