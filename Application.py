#主界面
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import shutil
from GameDownloader import *
from HtmlAnalyse import *
from Common import *
from FlashRunner import *
from RelatedDownloader import *
from AutoDownloader import *
from ToolDownloader import *

class Application:
	def __init__(self, root):
		self.root = root
		self.root.title("常见网站小游戏下载器 - 干大事的魔法师")
		self.root.geometry("720x540")
		self.gd=GameDownloader()
		self.ad=AutoDownloader(self.gd)
		self.rdWindow=None
		self.tdWindow=None
		if not os.path.isdir(Global.downloadDir):
			os.makedirs(Global.downloadDir) # 创建下载目录
		self.setupUI() # 绘制ui
		self.gameInfo_list=[]
		self.refreshGameList() # 刷新列表
	
	def setupUI(self):
		# 绘制ui
		# 顶部输入区域
		input_frame = ttk.Frame(self.root, padding="10")
		input_frame.grid(row=0, column=0, sticky=(tk.W,tk.E))
		ttk.Label(input_frame, text="游戏URL:").grid(row=0, column=0)
		self.url_entry = ttk.Entry(input_frame)
		self.url_entry.grid(row=0, column=1, sticky=(tk.W,tk.E), padx=(5,60))
		input_frame.columnconfigure(1, weight=1)

		# 按钮区域
		button_frame = ttk.Frame(self.root, padding="10")
		button_frame.grid(row=1, column=0, sticky=tk.W)
		self.downloadAndPlay_btn=ttk.Button(button_frame, text="下载并游玩", command=self.btn_downloadAndPlay)
		self.downloadAndPlay_btn.grid(row=0, column=0, padx=5)
		self.download_btn=ttk.Button(button_frame, text="下载", command=self.btn_downloadGame)
		self.download_btn.grid(row=0, column=1, padx=5)
		self.play_btn=ttk.Button(button_frame, text="游玩", command=self.btn_playGame)
		self.play_btn.grid(row=0, column=2, padx=5)
		self.putFolder_btn=ttk.Button(button_frame, text="装入文件夹", command=self.btn_putIntoFolder)
		self.putFolder_btn.grid(row=0, column=3, padx=5)
		self.relateDownload_btn=ttk.Button(button_frame, text="关联文件下载器", command=self.btn_relateDownload)
		self.relateDownload_btn.grid(row=0, column=4, padx=5)
		
		# 游戏列表区域
		list_frame = ttk.Frame(self.root, padding="10")
		list_frame.grid(row=2, column=0, sticky=(tk.N,tk.S,tk.W,tk.E))
		# 创建列表和滚动条
		self.game_list = tk.Listbox(list_frame, height=20)
		scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.game_list.yview)
		self.game_list.configure(yscrollcommand=scrollbar.set)
		self.game_list.grid(row=0, column=0, sticky=(tk.N,tk.S,tk.W,tk.E))
		scrollbar.grid(row=0, column=1, sticky=(tk.N,tk.S))
		list_frame.columnconfigure(0, weight=1)
		list_frame.rowconfigure(0, weight=1)

		# 按钮区域2
		button_frame2 = ttk.Frame(self.root, padding="10")
		button_frame2.grid(row=3, column=0, sticky=(tk.W,tk.E))
		self.delete_btn=ttk.Button(button_frame2, text="删除", command=self.btn_deleteGame)
		self.delete_btn.grid(row=0, column=0, padx=5)
		self.deleteAll_btn=ttk.Button(button_frame2, text="全部删除", command=self.btn_deleteAllGames)
		self.deleteAll_btn.grid(row=0, column=1, padx=5)
		self.refresh_btn=ttk.Button(button_frame2, text="刷新列表", command=self.btn_refreshGameList)
		self.refresh_btn.grid(row=0, column=2, padx=5)
		self.tooldownload_btn=ttk.Button(button_frame2, text="自由下载工具", command=self.btn_tooldownload)
		self.tooldownload_btn.grid(row=0, column=4, padx=5)
		self.swfToHtm_btn=ttk.Button(button_frame2, text="改为htm打开", command=self.btn_swfToHtm)
		self.swfToHtm_btn.grid(row=0, column=5, padx=(5,30))
		button_frame2.columnconfigure(3,weight=1)

		# 状态栏1
		info_frame = ttk.Frame(self.root)
		info_frame.grid(row=4, column=0, sticky=(tk.W,tk.E))
		self.info_var = tk.StringVar()
		self.info_var.set("找到的SWF路径:")
		self.gd.setSwfpathVariable(self.info_var)
		info_entry = ttk.Entry(info_frame, textvariable=self.info_var, state='readonly', foreground='blue')
		info_entry.grid(row=0, column=0, sticky=(tk.W,tk.E), pady=5)
		self.portTextVar = tk.StringVar()
		if Global.port>0:
			self.portTextVar.set(f"端口:{Global.port}")
		else:
			self.portTextVar.set(f"端口:无")
		style = ttk.Style() # 配置自定义样式，添加左边距
		style.configure('MyLeftPadding.TEntry', padding=(5, 0))
		ttk.Entry(info_frame, textvariable=self.portTextVar, width=10, state='readonly', style='MyLeftPadding.TEntry').grid(row=0, column=1)
		info_frame.columnconfigure(0,weight=1)

		# 状态栏2
		self.status_var = tk.StringVar()
		self.status_var.set(f"V2.0，支持4399、7k7k、17yy，可下载H5和Unity游戏。提示：http://localhost:{Global.port}/ 必须开着这个程序才能访问。")
		style2 = ttk.Style() # 配置自定义样式，添加左边距
		style2.configure('MyLeftPadding.TLabel', padding=(3, 0))
		status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, style='MyLeftPadding.TLabel')
		status_bar.grid(row=5, column=0, sticky=(tk.W,tk.E))
		# 配置网格权重
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(2, weight=1)
		# 绑定事件
		self.game_list.bind('<Double-Button-1>', self.on_doubleClick)
		self.game_list.bind('<<ListboxSelect>>', self.on_selectionUpdate)
		#防止失去焦点
		self.root.bind("<FocusIn>", self.on_focus)
	def on_focus(self, event):
		if self.root.state() in ('iconic', 'withdrawn'):
			self.root.deiconify()

	def btn_tooldownload(self):
		self.tdWindow=ToolDownloader(self.root)
		self.tdWindow=None
	def btn_downloadAndPlay(self):
		threading.Thread(target=self.thread_downloadPlayGame, daemon=True).start()
	def btn_downloadGame(self):
		self.downloadGame(useNewTheard=True)
	def btn_playGame(self):
		self.playGame()
	def btn_deleteGame(self):
		self.deleteGame()
	def btn_deleteAllGames(self):
		self.deleteAllGames()
	def btn_refreshGameList(self):
		self.refreshGameList(True)
	def btn_putIntoFolder(self):
		self.putIntoFolder()
	def btn_relateDownload(self):
		self.relateDownloader()
	def on_doubleClick(self, event):
		self.playGame()
	def on_selectionUpdate(self, event):
		self.selectionUpdate()
	
	def getSelectedIndex(self):
		# 获取选中的位置
		selection = self.game_list.curselection()
		if not selection:
			messagebox.showinfo("提示", "请先选择一个游戏")
			return None
		return selection[0]
	
	def getInputURL(self):
		url = self.url_entry.get().strip()
		if not url:
			messagebox.showinfo("提示", "请输入游戏URL，如https://www.4399.com/flash/6853.htm")
			return None
		return url
	
	def refreshGameList(self,showStatus=False):
		# 刷新列表，读取文件更新gameInfo_list里的信息（以InfoItem形式），game_list不再选中
		self.game_list.delete(0, tk.END)
		self.gameInfo_list=[]
		oldFolderNum=0
		oldFolderExample=""
		try:
			items = os.listdir(Global.downloadDir)
			for item in items:
				item_path = os.path.join(Global.downloadDir, item)
				if os.path.isdir(item_path):
					self.game_list.insert(tk.END, f"{item}/")
					self.gameInfo_list.append(InfoItem('folder',item))
					if HtmlAnalyse.isOldFolderName(item):
						if oldFolderNum==0:
							oldFolderExample=item
						oldFolderNum+=1
					continue
				if os.path.isfile(item_path) and item.endswith('.swf'):
					self.game_list.insert(tk.END, f"{item}")
					self.gameInfo_list.append(InfoItem('file',item))
					continue
		except Exception as e:
			messagebox.showerror("错误", f"无法读取游戏列表: {str(e)}")
		if showStatus:
			statusAppend=""
			if oldFolderNum>=1:
				statusAppend=f". 由于版本更新，请在旧文件夹名后加上s改成新文件夹名，如 {oldFolderExample} 应改成 {oldFolderExample}s。有{oldFolderNum}个文件夹仍是旧名字。"
			self.status_var.set(f"找到 {len(self.gameInfo_list)} 个游戏"+statusAppend)
		if self.game_list.size()>=1:
			self.deleteAll_btn.config(state=tk.NORMAL)
		else:
			self.deleteAll_btn.config(state=tk.DISABLED)
		self.selectionUpdate()
	def selectionUpdate(self):
		# 更新选择，更新按钮颜色
		selection = self.game_list.curselection()
		if not selection:
			self.play_btn.config(state=tk.DISABLED)
			self.delete_btn.config(state=tk.DISABLED)
			self.putFolder_btn.config(state=tk.DISABLED)
			self.relateDownload_btn.config(state=tk.DISABLED)
			self.swfToHtm_btn.config(state=tk.DISABLED)
			return
		selected_index=selection[0]
		self.play_btn.config(state=tk.NORMAL)
		self.delete_btn.config(state=tk.NORMAL)
		if self.gameInfo_list[selected_index].type=='file':
			self.putFolder_btn.config(state=tk.NORMAL)
			self.relateDownload_btn.config(state=tk.DISABLED)
			self.swfToHtm_btn.config(state=tk.DISABLED)
		elif self.gameInfo_list[selected_index].type=='folder':
			self.putFolder_btn.config(state=tk.DISABLED)
			self.relateDownload_btn.config(state=tk.NORMAL)
			if self.gameInfo_list[selected_index].folderExt=='.swf':
				self.swfToHtm_btn.config(state=tk.NORMAL)
			else:
				self.swfToHtm_btn.config(state=tk.DISABLED)
	
	def downloadGame(self,useNewTheard):
		url=self.getInputURL()
		if not url:
			return
		appendix,site=HtmlAnalyse.getURLInfo(url)
		# 不要重复下载
		if appendix!=None:
			for i in range(len(self.gameInfo_list)):
				if self.gameInfo_list[i].gameAppendix==appendix:
					self.game_list.selection_clear(0, tk.END)
					self.game_list.selection_set(i)
					self.game_list.see(i)
					self.selectionUpdate()
					messagebox.showinfo("提示", "游戏已存在")
					return
		if useNewTheard:
			# 在新线程中下载，避免界面冻结
			threading.Thread(target=self.thread_downloadGame, args=(url,appendix,site), daemon=True).start()
		else:
			downloadFilename=self.realDownload(url,appendix,site)
			if not downloadFilename:
				return
			for i in range(len(self.gameInfo_list)):
				if self.gameInfo_list[i].fileOrFolderName==downloadFilename:
					self.game_list.selection_clear(0, tk.END)
					self.game_list.selection_set(i)
					self.game_list.see(i)
					self.selectionUpdate()
					return True
			else:
				messagebox.showerror("错误", "未找到下载的文件")
				
	def realDownload(self,url,appendix,site):
		# 返回完整文件/文件夹名称
		self.status_var.set("正在下载游戏...")
		self.gd.setInfo(url,appendix,site)
		fileName=self.gd.downloadSWF()
		if not fileName:
			self.status_var.set("下载失败")
			return None
		self.status_var.set(f"下载完成: {fileName}")
		self.refreshGameList()
		return fileName

	def thread_downloadGame(self, url, name_appendix,site):
		self.realDownload(url,name_appendix,site)	
	def thread_downloadPlayGame(self):
		result=self.downloadGame(useNewTheard=False)
		if result:
			self.playGame()
	
	def playGame(self):
		# 游玩选中的游戏
		index = self.getSelectedIndex()
		if index==-1:
			messagebox.showerror("错误", f"没有选中游戏")
			return
		FlashRunner.playGame(self.gameInfo_list[index])
		
	def deleteOneWithFullPath(self,fullPath,type):
		if not os.path.exists(fullPath):
			messagebox.showerror("错误", f"找不到文件/文件夹: {fullPath}")
			return
		try:
			if type == 'file':
				os.remove(fullPath)
			elif type == 'folder':
				shutil.rmtree(fullPath)
			return True
		except Exception as e:
			messagebox.showerror("错误", f"删除失败: {str(e)}")

	def deleteGame(self):
		# 删除选中的游戏
		index = self.getSelectedIndex()
		if index==-1:
			messagebox.showerror("错误", f"没有选中游戏.")
			return
		item=self.gameInfo_list[index]
		fullPath=os.path.join(Global.downloadDir, item.fileOrFolderName)
		fullPathName1=HtmlAnalyse.getNormPath(fullPath)
		fullPathName2=""
		if item.type=='folder':
			fullPathName2="\\下的全部文件"
		if messagebox.askyesno("确认", f"确定要删除 {item.displayText} 吗？即{fullPathName1}{fullPathName2}"):
			result=self.deleteOneWithFullPath(fullPath,item.type)
			if result:
				self.status_var.set(f"已删除: {item.displayText}，即{fullPathName1}{fullPathName2}")
			self.refreshGameList()
	
	def deleteAllGames(self):
		# 删除所有游戏
		if len(self.gameInfo_list)==0:
			messagebox.showerror("错误", "没有可删除的游戏")
			return
		if messagebox.askyesno("确认", f"确定要删除这 {len(self.gameInfo_list)} 个游戏吗?!"):
			for i in range(len(self.gameInfo_list)):
				item=self.gameInfo_list[i]
				fullPath=os.path.join(Global.downloadDir, item.fileOrFolderName)
				self.deleteOneWithFullPath(fullPath, item.type)
			self.status_var.set("已删除所有游戏")
			self.refreshGameList()

	def putIntoFolder(self):
		index = self.getSelectedIndex()
		if index==-1:
			messagebox.showerror("错误", f"没有选中文件")
			return
		item=self.gameInfo_list[index]
		if item.type=='folder':
			messagebox.showerror("错误", f"只能对swf文件操作")
			return
		try:
			folderFullPath=os.path.join(Global.downloadDir, item.gameName+"s")
			os.makedirs(folderFullPath)
			gameNewFullPath=os.path.join(folderFullPath, item.gameName+".swf")
			os.rename(item.gameFullPath,gameNewFullPath)
			result=self.gd.getSWFPathWithAppendix(item.gameAppendix)
			if result:
				netSWFPath=result.swfUrl
			else:
				netSWFPath=""
			newIniFullPath=os.path.join(folderFullPath, "SWFNetPath.ini")
			inirst=IniResult(newIniFullPath)
			inirst.type="swf"
			inirst.netPath=netSWFPath
			inirst.width=result.gameWidth
			inirst.height=result.gameHeight
			if result.isNewPage:
				inirst.isNewPage=1
				inirst.newPageUrl=result.newPageUrl
			else:
				inirst.isNewPage=0
			inirst.WriteFile()
		except Exception as e:
			messagebox.showerror("错误", f"装入文件夹失败: {str(e)}")
			return
		self.status_var.set("装入文件夹成功")
		self.refreshGameList()
		for i in range(len(self.gameInfo_list)):
			if self.gameInfo_list[i].fileOrFolderName==item.gameName+'s':
				self.game_list.selection_clear(0, tk.END)
				self.game_list.selection_set(i)
				self.game_list.see(i)
				self.selectionUpdate()
				break
		else:
			messagebox.showerror("错误", "未找到装好的文件")
			return
		
	def relateDownloader(self):
		index = self.getSelectedIndex()
		if index==-1:
			return
		if self.gameInfo_list[index].type=='file':
			messagebox.showerror("错误", f"只能对文件夹操作")
			return
		self.rdWindow=RelatedDownloader(self.root, self.gameInfo_list[index],self.gd,self.ad)
		self.rdWindow=None
		
	def btn_swfToHtm(self):
		index = self.getSelectedIndex()
		if index==-1:
			messagebox.showerror("错误", f"没有选中文件")
			return
		item=self.gameInfo_list[index]
		if item.type=='file':
			messagebox.showerror("错误", f"只能对文件夹操作")
			return
		if item.type=='folder' and item.folderExt!='.swf':
			messagebox.showerror("错误", f"只能对swf文件操作，而它的扩展名为 {item.folderExt}")
			return
		#询问
		if not messagebox.askyesno("确认", f"确定要将 {item.gameName} 改用htm打开吗？这将失去下载的优势（只是断网也能玩了），你仍需要为浏览器安装flash插件，并忍受插件不稳定的痛苦。只有不得不需要浏览器环境时才要这么做。"):
			return
		#正式转换
		result=self.real_swfToHtm(item)
		if result==2:
			self.status_var.set("转换成htm成功")
		elif result==None:
			self.status_var.set("转换成htm失败")
		self.refreshGameList()
		if result==2:
			for i in range(len(self.gameInfo_list)):
				if self.gameInfo_list[i].fileOrFolderName==item.gameName+'h':
					self.game_list.selection_clear(0, tk.END)
					self.game_list.selection_set(i)
					self.game_list.see(i)
					self.selectionUpdate()
					break
			else:
				messagebox.showerror("错误", "未找到变动的文件")
				return

	def real_swfToHtm(self, item):
		#读取一下SWFNetPath.ini
		folderFullPath=os.path.join(Global.downloadDir,item.folderName)
		isOk=-1
		inirst=IniResult.fromFile(item.iniFullPath,".swf")
		if inirst.type=="swf":
			isOk=inirst.isNewPage
			if isOk:
				newPageUrl=inirst.newPageUrl
				gameInnerName=HtmlAnalyse.getURLFilename(inirst.netPath)
				gameWidth=inirst.width
				gameHeight=inirst.height
			else:
				newPageUrl=inirst.netPath
				gameInnerName="mainSwfGame.swf"
				gameWidth=inirst.width
				gameHeight=inirst.height
		if isOk==-1:
			#不知道，看一看吧
			result=self.gd.getSWFPathWithAppendix(item.gameAppendix)
			if not result:
				messagebox.showerror("错误", "既不能在SWFNetPath.ini里找到信息，也无法去网站获取信息，无法知道下载路径和游戏名")
				return
			if result.isNewPage:
				isOk=1
				newPageUrl=result.newPageUrl
				gameInnerName=HtmlAnalyse.getURLFilename(result.swfUrl)
				gameWidth=result.gameWidth
				gameHeight=result.gameHeight
			else:
				isOk=0
				newPageUrl=result.swfUrl
				gameInnerName="mainSwfGame.swf"
				gameWidth=result.gameWidth
				gameHeight=result.gameHeight
		
		#改文件夹名!
		newFolderName=item.gameName+"h"
		newFolderFullPath=os.path.join(Global.downloadDir, newFolderName)
		while True:
			try:
				os.rename(folderFullPath, newFolderFullPath)
				break
			except PermissionError as e:
				retryResult=messagebox.askretrycancel("文件夹被占用", f"无法重命名文件夹 {folderFullPath} 为 {newFolderFullPath}，是否是其它程序在占用? 请关闭相关程序后点击[重试]. {str(e)}")
				if retryResult:
					pass
				else:
					return
			except Exception as e:
				messagebox.showerror("错误", f"无法重命名文件夹 {folderFullPath} 为 {newFolderFullPath}. {str(e)}")
				return
		#改swf名！
		gameOldRelaPath=os.path.join(newFolderName, item.gameName+".swf")
		gameOldFullPath=os.path.join(Global.downloadDir, gameOldRelaPath)
		if os.path.isfile(gameOldFullPath):
			gameNewRelaPath=os.path.join(newFolderName, gameInnerName)
			gameNewFullPath=os.path.join(Global.downloadDir, gameNewRelaPath)
			try:
				os.rename(gameOldFullPath,gameNewFullPath)
			except Exception as e:
				try:
					shutil.copy2(gameOldFullPath,gameNewFullPath)
				except Exception as e:
					if isOk==1:
						messagebox.showwarning("警告", f"无法更名或复制原来的 {gameOldFullPath} 为 {gameNewFullPath}，你需要在“关联文件下载器”里自行下载 {gameInnerName}. {str(e)}")
					elif isOk==0:
						messagebox.showwarning("警告", f"无法更名或复制原来的 {gameOldFullPath} 为 {gameNewFullPath}，你需要自行更名. {str(e)}")
				else:
					messagebox.showinfo("提示", f"{gameOldFullPath} 可能被占用，于是我采用了复制的方法建立 {gameOldFullPath}. 您可稍后可自行删除 {gameOldFullPath} 节省空间。")
		else:
			if isOk==1:
				messagebox.showwarning("警告", f"找不到旧游戏 {gameOldFullPath}，你需要在“关联文件下载器”里自行下载 {gameInnerName}")
			elif isOk==0:
				messagebox.showwarning("警告", f"找不到旧游戏 {gameOldFullPath}，你删它干啥..")
				return
		#下载htm文件
		if isOk==1:
			self.gd.setInfoWithAppendix(item.gameAppendix)
			result=self.gd.downloadMainHtm(newFolderName,item.gameName,newPageUrl)
			if not result:
				return
		elif isOk==0:
			localRelaPath=os.path.join(newFolderName,item.gameName+".htm")
			localFullPath=os.path.join(Global.downloadDir,localRelaPath)
			try:
				shutil.copy2(Global.flashPagePath,localFullPath)
			except Exception as e:
				messagebox.showerror("错误", f"无法复制 {Global.flashPagePath} 到 {localFullPath} : {str(e)}")
				return
		#改SWFNetPath.ini
		newIniFullPath=os.path.join(newFolderFullPath, "SWFNetPath.ini")
		inirst2=IniResult(newIniFullPath)
		inirst2.type="htm"
		inirst2.netPath=newPageUrl
		inirst2.width=gameWidth
		inirst2.height=gameHeight
		try:
			inirst2.WriteFile()
		except Exception as e:
			messagebox.showerror("错误",f"设置 {newIniFullPath} 时发生错误. {str(e)}")
			return
		return 2

