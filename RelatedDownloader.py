#关联文件下载器窗口
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from GameDownloader import *
from HtmlAnalyse import *
from Common import *
from FlashRunner import *
from EditNetPathDialog import *
from AutoDownloader import *

class RelatedDownloader:
	def __init__(self, parent, item, gd, ad):
		self.parent = parent
		self.item = item
		self.gd = gd
		self.ad = ad
		self.enpdWindow=None
		self.inirst=IniResult.fromFile(item.iniFullPath,item.folderExt)
		self.gd.setSWFNetPath(self.inirst.netPath)
		self.cancelFlag = False
		self.isdownloading = False
		self.gd.localFolder=self.item.folderFullPath
		if self.item.folderExt==".htm":
			self.HTM=True
		else:
			self.HTM=False
		# 创建新窗口
		self.window = tk.Toplevel(parent)
		self.window.title("关联文件下载器")
		if not self.HTM:
			self.window.geometry("500x370")
		else:
			self.window.geometry("560x550")
		self.window.transient(parent)
		self.window.grab_set()
		self.window.focus_set()
		self.setupUI()
		self.updateBtnStatus()
		self.centerWindow()
		#
		if self.HTM:
			self.onPauseText=False
			temp=quote(self.item.gameName)
			folderRelaRelaPath=f"/{Global.downloadLocalhostPath}{temp}h/"
			self.ad.InitNewProject(folderRelaRelaPath, f"{temp}.htm")
			self.ad.startRecord()
			self.adStatusProfix="已停止，"
			self.realUpdateAutoDownloadStatus(False)
			self.afterId=self.window.after(0,self.updateAutoDownloadDialogField_loop)
			self.afterId2=self.window.after(0,self.updateAutoDownloadStatus_loop)
		self.window.wait_window()

	def centerWindow(self):
		self.window.update_idletasks()
		width = self.window.winfo_width()
		height = self.window.winfo_height()
		x = (self.window.winfo_screenwidth() // 2) - (width // 2)
		y = (self.window.winfo_screenheight() // 2) - (height // 2)
		self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

	def setupUI(self):
		fileName_frame = ttk.Frame(self.window)
		fileName_frame.grid(row=0, column=0, columnspan=3, pady=5, sticky=tk.W)
		ttk.Label(fileName_frame, text="文件名称：").grid(row=0, column=0, padx=10)
		ttk.Label(fileName_frame, text=self.item.gameName+self.item.folderExt,width=25).grid(row=0, column=1, padx=0)
		self.tryPlayBtn=ttk.Button(fileName_frame, text="尝试游玩", command=self.btn_tryPlay)
		self.tryPlayBtn.grid(row=0, column=2, padx=5)

		#路径信息
		self.netPath_var = tk.StringVar()
		self.netPath_var.set(self.inirst.netPath)
		ttk.Label(self.window, text="网络路径：").grid(row=1, column=0, padx=10, pady=(0,0))
		ttk.Entry(self.window, textvariable=self.netPath_var, state='readonly').grid(row=1, column=1, sticky=(tk.W,tk.E), padx=0, pady=(5,0))
		ttk.Label(self.window, text="相关信息：").grid(row=2, column=0, padx=10, pady=(0,5))
		self.iniInfo_var = tk.StringVar()
		self.iniInfo_var.set(self.inirst.ShowInfo())
		ttk.Entry(self.window, textvariable=self.iniInfo_var, state='readonly').grid(row=2, column=1, sticky=(tk.W,tk.E), padx=0, pady=(0,5))
		self.changeNetPathBtn=ttk.Button(self.window, text="修改", command=self.btn_openEditDialog)
		self.changeNetPathBtn.grid(row=1, column=2,rowspan=2, padx=5, pady=5)
		# 文件列表输入框
		download_frame = ttk.Frame(self.window)
		download_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
		self.clearTextBtn=ttk.Button(download_frame, text="清除内容", command=self.btn_clearText)
		self.clearTextBtn.grid(row=0, column=0, padx=5)
		self.downloadInfo_var = tk.StringVar()
		self.downloadInfo_var.set("请输入要下载的文件")
		ttk.Label(download_frame, textvariable=self.downloadInfo_var).grid(row=0, column=1, padx=5)
		#输入框
		self.files_text = scrolledtext.ScrolledText(self.window, height=5)
		self.files_text.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky=(tk.N,tk.S,tk.W,tk.E))
		# 按钮框架
		button_frame = ttk.Frame(self.window)
		button_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky=(tk.W,tk.E))
		self.BatchDownloadBtn=ttk.Button(button_frame, text="批量下载", command=self.btn_batchDownload)
		self.BatchDownloadBtn.grid(row=0, column=0, padx=5)
		self.CancelDownloadBtn=ttk.Button(button_frame, text="取消下载", command=self.btn_cancelDownload)
		self.CancelDownloadBtn.grid(row=0, column=1, padx=5)
		self.notCoverExist_var=tk.BooleanVar()
		self.notCoverExist_var.set(True)
		self.notCoverExist_checkBtn=ttk.Checkbutton(button_frame,text="不覆盖已有文件", variable=self.notCoverExist_var)
		self.notCoverExist_checkBtn.grid(row=0, column=2, padx=(20,5))
		self.ExitBtn=ttk.Button(button_frame, text="退出", command=self.on_close)
		self.ExitBtn.grid(row=0, column=4, padx=5)
		button_frame.columnconfigure(3, weight=1)
		if self.HTM:
			#日志按钮框
			autoDownloadStatus_frame = ttk.Frame(self.window)
			autoDownloadStatus_frame.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
			self.autoDownloadTextPauseBtn=ttk.Button(autoDownloadStatus_frame, text="暂停滚动", command=self.btn_autoDownloadTextPause)
			self.autoDownloadTextPauseBtn.grid(row=0, column=0, padx=5)
			self.autoDownloadTextClearBtn=ttk.Button(autoDownloadStatus_frame, text="清除内容", command=self.btn_autoDownloadTextClear)
			self.autoDownloadTextClearBtn.grid(row=0, column=1, padx=5)
			self.autoDownloadLastName_var = tk.StringVar()
			self.autoDownloadLastName_var.set("")
			self.autoDownloadLastName_label=ttk.Label(autoDownloadStatus_frame, textvariable=self.autoDownloadLastName_var)
			self.autoDownloadLastName_label.grid(row=0, column=2, padx=5)
			#日志信息框
			self.autoDownloadDialog_text = scrolledtext.ScrolledText(self.window, height=10)
			self.autoDownloadDialog_text.grid(row=7, column=0, columnspan=3, padx=10, pady=5, sticky=(tk.N,tk.S,tk.W,tk.E))
			#自动下载按钮
			autoDownloadBtn_frame = ttk.Frame(self.window)
			autoDownloadBtn_frame.grid(row=8, column=0, columnspan=3, padx=5, pady=(5,15), sticky=tk.W)
			self.AutoDownloadStartBtn=ttk.Button(autoDownloadBtn_frame, text="自动下载所需文件", command=self.btn_AutoDownloadStart)
			self.AutoDownloadStartBtn.grid(row=0, column=0, padx=5)
			self.AutoDownloadStopBtn=ttk.Button(autoDownloadBtn_frame, text="停止自动下载", command=self.btn_AutoDownloadStop)
			self.AutoDownloadStopBtn.grid(row=0, column=1, padx=5)
			self.autoDownloadStatus_var = tk.StringVar()
			self.autoDownloadStatus_var.set("")
			self.autoDownloadStatus_label=ttk.Label(autoDownloadBtn_frame, textvariable=self.autoDownloadStatus_var)
			self.autoDownloadStatus_label.grid(row=0, column=2, padx=5)
		# 配置网格权重
		self.window.columnconfigure(1, weight=1)
		if not self.HTM:
			self.window.rowconfigure(4, weight=1)
		else:
			self.window.rowconfigure(4, weight=1)
			self.window.rowconfigure(7, weight=1)
		#关闭窗口时
		self.window.protocol("WM_DELETE_WINDOW", self.on_close)
		# 防止失去焦点
		self.window.bind("<Map>", self.on_map)
		self.window.bind("<FocusIn>", self.on_focus)
	def on_map(self,event):
		if self.parent.state() in ('iconic', 'withdrawn'):
			self.parent.deiconify()
	def on_focus(self, event):
		if self.window.state() in ('iconic', 'withdrawn'):
			self.window.deiconify()

	def btn_AutoDownloadStart(self):
		if len(self.gd.relateDownloadSWFNetPath)==0:
			messagebox.showinfo("提示","需要先填写swf在网上的路径")
			return
		self.adStatusProfix="下载中... "
		self.ad.startAutoDownloading()
		self.realUpdateAutoDownloadStatus(False)
		self.updateBtnStatus()
		
	def btn_AutoDownloadStop(self):
		self.adStatusProfix="已停止，"
		self.ad.stopAutoDownloading()
		self.realUpdateAutoDownloadStatus(False)
		self.updateBtnStatus()

	def updateAutoDownloadStatus_loop(self):
		if self.ad.statusUpdated==True:
			self.realUpdateAutoDownloadStatus()
		self.afterId2=self.window.after(500,self.updateAutoDownloadStatus_loop)

	def realUpdateAutoDownloadStatus(self, doubleCheck=True):
		with self.ad.statusLock:
			if doubleCheck and self.ad.statusUpdated==False:
				return
			totalTaskNum=self.ad.totalTaskNum
			loadingTaskNum=self.ad.loadingTaskNum
			successTaskNum=self.ad.successTaskNum
			notFoundTaskNum=self.ad.notFoundTaskNum
			failTaskNum=self.ad.failTaskNum
			lastDownloadName=self.ad.lastDownloading
			lastDownloadStatusOk=self.ad.lastDownloadOk
			self.ad.statusUpdated=False
		totalTaskText=f"总共{totalTaskNum}个"
		if loadingTaskNum>0:
			loadingTaskText=f"，下载中{loadingTaskNum}个"
		else:
			loadingTaskText=""
		if successTaskNum>0:
			successTaskText=f"，成功{successTaskNum}个"
		else:
			successTaskText=""
		if notFoundTaskNum>0:
			notFoundTaskText=f"，404有{notFoundTaskNum}个"
		else:
			notFoundTaskText=""
		if failTaskNum>0:
			failTaskText=f"，失败{failTaskNum}个"
		else:
			failTaskText=""
		text=f"{self.adStatusProfix}{totalTaskText}{loadingTaskText}{successTaskText}{notFoundTaskText}{failTaskText}"
		self.autoDownloadStatus_var.set(text)
		
		if lastDownloadStatusOk:
			lastStatusText="下载完成 "
		else:
			lastStatusText="下载中: "
		self.autoDownloadLastName_var.set(f"{lastStatusText}{lastDownloadName}")

	def btn_autoDownloadTextPause(self):
		if self.onPauseText:
			#恢复
			self.afterId=self.window.after(0,self.updateAutoDownloadDialogField_loop)
			self.autoDownloadTextPauseBtn.config(text="暂停滚动")
			self.onPauseText=False
		else:
			#暂停
			if self.afterId:
				self.window.after_cancel(self.afterId)
				self.afterId=None
			self.autoDownloadTextPauseBtn.config(text="继续滚动")
			self.onPauseText=True

	def updateAutoDownloadDialogField_loop(self):
		if self.ad.textListUpdated==True:
			self.realUpdateAutoDownloadDialogField()
		self.afterId=self.window.after(500,self.updateAutoDownloadDialogField_loop)

	def realUpdateAutoDownloadDialogField(self):
		with self.ad.lock:
			if self.ad.textListUpdated==False:
				return
			lines=[self.ad.textList.getLast(i) for i in range(self.ad.textList.visibleItemNum)]
			self.ad.textListUpdated=False
		text="\n".join(lines)
		self.autoDownloadDialog_text.delete("1.0",tk.END)
		self.autoDownloadDialog_text.insert(tk.END, text)

	def btn_autoDownloadTextClear(self):
		self.ad.clearTextList()
		self.realUpdateAutoDownloadDialogField()

	def on_close(self):
		# 关闭窗口时
		if self.isdownloading:
			messagebox.showinfo("提示", "请先等待下载完成")
		else:
			if self.HTM:
				self.ad.exitRecord()
				if self.ad.isAutoDownloading:
					self.ad.stopAutoDownloading()
					with self.ad.statusLock:
						isOk=self.ad.downloadOk
					if not isOk:
						self.adStatusProfix="结束剩余下载... "
						self.realUpdateAutoDownloadStatus(False)
						self.ExitBtn.config(state=tk.DISABLED)
						#将所有按钮失效，但外观不变
						self.changeNetPathBtn.config(command=None)
						self.BatchDownloadBtn.config(command=None)
						self.CancelDownloadBtn.config(command=None)
						self.AutoDownloadStartBtn.config(command=None)
						self.AutoDownloadStopBtn.config(command=None)
						#等待完成
						self.onDestoryWaitAutoDownloadOk(8000)
						return
			self.reallyDestory()
	def onDestoryWaitAutoDownloadOk(self,timeout):
		with self.ad.statusLock:
			isOk=(self.ad.downloadOk)
		if isOk:
			self.reallyDestory()
			return
		if timeout<=0:
			if messagebox.askyesno("下载超时",f"不知为什么，这么长时间仍未下载完。下载任务无法打断，退出会有未知后果。要继续下载选“是”，要退出选“否”"):
				timeout=8000
			else:
				self.reallyDestory()
				return
		self.window.after(3,lambda:self.onDestoryWaitAutoDownloadOk(timeout-3))
	def reallyDestory(self):
		if self.HTM:
			if self.afterId:
				self.window.after_cancel(self.afterId)
			if self.afterId2:
				self.window.after_cancel(self.afterId2)
			self.ad.DestoryProject()
		self.window.destroy()

	def updateBtnStatus(self):
		cnpState=True
		if self.isdownloading:
			cnpState=False
			self.BatchDownloadBtn.config(state=tk.DISABLED)
			self.CancelDownloadBtn.config(state=tk.NORMAL)
			self.ExitBtn.config(state=tk.DISABLED)
			self.notCoverExist_checkBtn.config(state=tk.DISABLED)
		else:
			self.BatchDownloadBtn.config(state=tk.NORMAL)
			self.CancelDownloadBtn.config(state=tk.DISABLED)
			self.ExitBtn.config(state=tk.NORMAL)
			self.notCoverExist_checkBtn.config(state=tk.NORMAL)
		if self.HTM:
			if self.ad.isAutoDownloading:
				cnpState=False
				self.AutoDownloadStartBtn.config(state=tk.DISABLED)
				self.AutoDownloadStopBtn.config(state=tk.NORMAL)
			else:
				self.AutoDownloadStartBtn.config(state=tk.NORMAL)
				self.AutoDownloadStopBtn.config(state=tk.DISABLED)
		if cnpState:
			self.changeNetPathBtn.config(state=tk.NORMAL)
		else:
			self.changeNetPathBtn.config(state=tk.DISABLED)
	
	def btn_cancelDownload(self):
		self.cancelFlag=True
		self.downloadInfo_var.set("取消中...")

	def btn_clearText(self):
		self.files_text.delete("1.0",tk.END)
	def btn_openEditDialog(self):
		self.enpdWindow=EditNetPathDialog(self.window,self.item, self.gd, self.btn_openEditDialog_confirmCallback)
		self.enpdWindow=None

	def btn_openEditDialog_confirmCallback(self):
		#这个callback只会在点确定时用，其它的情况则只写往下写
		self.inirst.readFile()
		self.gd.setSWFNetPath(self.inirst.netPath)
		self.netPath_var.set(self.inirst.netPath)
		self.iniInfo_var.set(self.inirst.ShowInfo())

	def btn_batchDownload(self):
		if len(self.gd.relateDownloadSWFNetPath)==0:
			messagebox.showinfo("提示","需要先填写swf在网上的路径")
			return
		textContent = self.files_text.get("1.0", tk.END)
		lines = textContent.split('\n')
		# 处理每一行：去除首尾空白，过滤空行
		processedLines = []
		for line in lines:
			strippedLine = line.strip()
			if strippedLine!="":
				processedLines.append(strippedLine)
		if len(processedLines)==0:
			messagebox.showinfo("提示","您还未填写任何东西")
			return
		self.isdownloading=True
		self.cancelFlag=False
		self.updateBtnStatus()
		threading.Thread(target=self.thread_batchDownload,args=(processedLines,), daemon=True).start()
	def btn_tryPlay(self):
		FlashRunner.playGame(self.item)
	def thread_batchDownload(self,things):
		def setStatusVarText():
			allNumText=f"总共{allNum}个"
			successNumText=f"，成功{successNum}个"
			notVaildNum=allNum-safeNum
			if notVaildNum>0:
				notVaildNumText=f"，不规范名称{notVaildNum}个"
			else:
				notVaildNumText=""
			repeatNum=safeNum-uniqueNum
			if repeatNum>0:
				repeatNumText=f"，重复{repeatNum}个"
			else:
				repeatNumText=""
			existNum=uniqueNum-uniqueNewNum
			if existNum>0:
				existNumText=f"，已存在{existNum}个"
			else:
				existNumText=""
			if notFoundNum>0:
				notFoundNumText=f"，404有{notFoundNum}个"
			else:
				notFoundNumText=""
			if failNum>0:
				failNumText=f"，其余失败{failNum}个"
			else:
				failNumText=""
			self.downloadInfo_var.set(f"{prefixText}{allNumText}{successNumText}{notVaildNumText}{repeatNumText}{existNumText}{notFoundNumText}{failNumText}")
		
		allNum=len(things)
		self.downloadInfo_var.set(f"预处理中...")
		#合规
		things2=[]
		for name in things:
			temp=HtmlAnalyse.getBatchDownloadValidName(name)
			if temp:
				things2.append(temp)
		safeNum=len(things2)
		#去重
		things3 = list(dict.fromkeys(things2)) #python3.7以上
		uniqueNum=len(things3)
		#接着去除已存在的
		if self.notCoverExist_var.get():
			things4=[]
			for name in things3:
				fileFullPath=os.path.join(self.item.folderFullPath,name)
				if not os.path.exists(fileFullPath):
					things4.append(name)
		else:
			things4=things3
		uniqueNewNum=len(things4)
		#开始下载
		successNum=0
		notFoundNum=0
		failNum=0
		prefixText=""
		for i in range(uniqueNewNum):
			prefixText=f"下载第 {i}/{uniqueNewNum} 个... "
			setStatusVarText()
			result=self.gd.relateDownload(things4[i])
			if result==1:
				successNum+=1
			elif result==0:
				failNum+=1
			elif result==-1:
				notFoundNum+=1
			if self.cancelFlag:
				prefixText="取消成功，"
				break
		else:
			prefixText="下载完成，"
		setStatusVarText()
		self.isdownloading=False
		self.updateBtnStatus()


