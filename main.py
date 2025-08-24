import os
import sys
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog,scrolledtext
import requests
import re
from urllib.parse import urljoin,urlparse
import shutil
from pathlib import Path

class CONST:
	pass
class FlashRunner:
	def run(filePath):
		if not os.path.exists(filePath):
			messagebox.showerror("错误", f"找不到文件: {filePath}")
			return
		try:
			if not os.path.exists(CONST.flashPlayerPath):
				messagebox.showwarning("警告", "未找到tool/FlashPlayer.exe")
				os.startfile(filePath)
			else:
				subprocess.Popen([CONST.flashPlayerPath, filePath])
		except Exception as e:
			messagebox.showerror("错误", f"无法运行游戏: {str(e)}")

class PHPTool:
	# 模拟 $.ajax 请求
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

class HtmlAnalyse:
	def getURLInfo(url):
		#输出(后缀, 网址类型) 网址类型有'4399''7k7k''17yy'
		if url.find('4399.com')!=-1:
			type='4399'
			char='a'
		elif url.find('7k7k.com')!=-1:
			type='7k7k'
			char='b'
		elif url.find('17yy.com')!=-1:
			type='17yy'
			char='c'
		else:
			type=None
			char='z'
		match = re.search(r'/([0-9]+)(_[0-9]+)?\.htm', url)
		if match:
			appendix=char+match.group(1)
		else:
			appendix=None
		return (appendix,type)
	def appendixToURL(appendix):
		#输出(url,site)
		match = re.search(r'^([a-z])([0-9]+)$', appendix)
		if not match:
			return None
		char=match.group(1)
		number=match.group(2)
		if char=='a':
			return ("https://www.4399.com/flash/"+number+".htm",'4399')
		elif char=='b':
			return ("https://www.7k7k.com/swf/"+number+".htm",'7k7k')
		elif char=='c':
			return ("http://www.17yy.com/f/play/"+number+".html",'17yy')
		else:
			return None
	def getNameAppendixOfFile(fileName,type):
		if type=='folder':
			match = re.search(r'_([^_]+)$',fileName)
			if match:
				return match.group(1)
			return None
		if type=='file':
			match = re.search(r'_([^_]+)\.swf$',fileName)
			if match:
				return match.group(1)
			return None
	def Get4399GameName(htmlContent):
		match = re.search(r'game_title\s*=\s*\'(.*?)\'', htmlContent)
		if match:
			return match.group(1)
		match = re.search(r'title\s*=\s*\'(.*?)\'', htmlContent)
		if match:
			return match.group(1)
		return "未知名称"
	def Get4399DirectSwfPath(htmlContent):
		match = re.search(r'_strGamePath\s*=\s*"(.*?\.swf)"', htmlContent)
		if match:
			return "https://sda.4399.com/4399swf"+match.group(1)
		match = re.search(r'src=\'(//sda\.4399\.com/.*?\.swf)\'', htmlContent)
		if match:
			return "https:"+match.group(1)
		return None
	def Get4399NewPagePath(htmlContent):
		match = re.search(r'_strGamePath\s*=\s*"(.*?\.html?)"', htmlContent)
		if match:
			return "https://sda.4399.com/4399swf"+match.group(1)
		match = re.search(r'src=\'(//sda\.4399\.com/.*?\.html?)\'', htmlContent)
		if match:
			return "https:"+match.group(1)
		return None
	def Get4399SwfPathInNewPage(htmlContent,newpagePath):
		matchpos = htmlContent.find('id="flashgame"')
		if matchpos==-1:
			return None
		match = re.search(r'src="(.*?\.swf)"', htmlContent[matchpos:])
		if match:
			return urljoin(newpagePath,match.group(1))
		return None
	def Is4399NewPageUnity(htmlContent):
		if htmlContent.find('WebPlayer.unity3d')!=-1:
			return True
		if htmlContent.find('unityPlayer')!=-1:
			return True
		return False
	def Is4399NewPageHtml5(htmlContent):
		if htmlContent.find('text/javascript')!=-1:
			return True
		return False
	def Get7k7kGameName(htmlContent):
		match = re.search(r'gameName:\s*"(.*?)"', htmlContent)
		if match:
			return match.group(1)
		return "未知名称"
	def Get7k7kDirectSwfPath(htmlContent):
		match = re.search(r'gamePath:\s*"(.*?\.swf)"', htmlContent)
		if match:
			return match.group(1)
		return None
	def Get7k7kNewPagePath(htmlContent):
		match = re.search(r'gamePath:\s*"(.*?\.html?)"', htmlContent)
		if match:
			return match.group(1)
		return None
	def Get7k7kSwfPathInNewPage(htmlContent,newpagePath):
		match = re.search(r'_src_\s*=\s*\'(.*?\.swf)\'', htmlContent)
		if match:
			return urljoin(newpagePath,match.group(1))
		return None
	def Get17yyGameName(htmlContent):
		match = re.search(r'm7_gamename\s*=\s*"(.*?)"', htmlContent)
		if match:
			return match.group(1)
		match = re.search(r'<title>(.*?)在线玩"', htmlContent)
		if match:
			return match.group(1)
		return "未知名称"
	def Get17yyGameCategory(htmlContent):
		match = re.search(r'var\s+date\s*=\s*"(.*?)"', htmlContent)
		if match:
			return match.group(1)
		return None
	def Get17yyGameID(htmlContent,url):
		match = re.search(r'm7_gameid\s*=\s*"([0-9]+?)"',htmlContent)
		if match:
			return int(match.group(1))
		match = re.search(r'/([0-9]+)\.html?"',url)
		if match:
			return int(match.group(1))
		return -1
	def Get17yySwfPathInNewPage(htmlContent,newpagePath):
		return HtmlAnalyse.Get7k7kSwfPathInNewPage(htmlContent,newpagePath)
		#我找不到足够的样本做实验

class GameDownloader:
	def __init__(self):
		self.site=None
		self.url=None
		self.appendix=None
		self.relateDownloadSWFNetPath=None
		self.relateDownloadFolderNetPath=None
		self.localFolder=None
		self.swfpathVariable=None
		self.header1 = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
		}
		self.header2 = None
		self.header3 = None
	def setSWFNetPath(self,SWFNetPath):
		if SWFNetPath=="":
			self.relateDownloadSWFNetPath=""
			self.relateDownloadFolderNetPath=""
			return
		self.relateDownloadSWFNetPath=SWFNetPath
		parsed = urlparse(SWFNetPath)
		pathObj = Path(parsed.path)
		dirPath = pathObj.parent.as_posix() + '/'
		self.relateDownloadFolderNetPath=f"{parsed.scheme}://{parsed.netloc}{dirPath}"
	def setSwfpathVariable(self,swfpathVariable=None):
		self.swfpathVariable=swfpathVariable
	def setInfo(self,url=None,appendix=None,site=None):
		self.url=url
		self.appendix=appendix
		self.site=site
		self.header2 = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
			'Referer': self.url
		}
	def setHeader3(self,newurl):
		self.header3 = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
			'Referer': newurl
		}
	def getSWFPath(self):
		#返回(gameName,swfPath)
		if self.site=='4399':
			return self.get4399SWFPath()
		elif self.site=='7k7k':
			return self.get7k7kSWFPath()
		elif self.site=='17yy':
			return self.get17yySWFPath()
		else:
			return None
	def downloadSWF(self):
		#返回文件名字
		result=self.getSWFPath()
		if not result:
			return None
		gameName=result[0]
		swfPath=result[1]
		parentPath=result[2]
		# 处理文件名冲突
		fileName = f"{gameName}_{self.appendix}.swf"
		filePath = os.path.join(CONST.downloadDir, fileName)
		counter = 1
		while os.path.exists(filePath):
			fileName = f"{gameName}_{counter}_{self.appendix}.swf"
			filePath = os.path.join(CONST.downloadDir, fileName)
			counter += 1
		# 下载SWF文件
		try:
			self.setHeader3(parentPath)
			swfResponse = requests.get(swfPath, headers=self.header3)
			with open(filePath, 'wb') as f:
				f.write(swfResponse.content)
		except Exception as e:
			messagebox.showerror("错误", f"找到SWF路径但下载失败: {str(e)}")
			return
		return fileName
		
	def get4399SWFPath(self):
		try:
			response = requests.get(self.url, headers=self.header1)
			response.encoding = 'gbk'
			htmlContent = response.text
			# 查找游戏名称
			gameName=HtmlAnalyse.Get4399GameName(htmlContent)
			# 查找SWF路径
			swfPath = HtmlAnalyse.Get4399DirectSwfPath(htmlContent)
			if not swfPath:
				newpagePath=HtmlAnalyse.Get4399NewPagePath(htmlContent)
				if not newpagePath:
					messagebox.showerror("错误", "无法找到游戏的SWF文件")
					return
				response2 = requests.get(newpagePath, headers=self.header2)
				response2.encoding = 'gbk'
				newpageContent = response2.text
				swfPath=HtmlAnalyse.Get4399SwfPathInNewPage(newpageContent,newpagePath)
				if not swfPath:
					if HtmlAnalyse.Is4399NewPageUnity(newpageContent):
						messagebox.showerror("错误", "这是Unity游戏，本程序无法下载")
						return
					if HtmlAnalyse.Is4399NewPageHtml5(newpageContent):
						messagebox.showerror("错误", "这是html5游戏，本程序无法下载")
						return
					messagebox.showerror("错误", "这是未知类型的游戏，本程序无法下载")
					return
				else:
					parentPath=newpagePath
			else:
				parentPath=self.url
		except Exception as e:
			messagebox.showerror("错误", f"下载失败: {str(e)}")
			return
		self.swfpathVariable.set(f"找到的SWF路径: {swfPath}")
		return (gameName,swfPath,parentPath)

	def get7k7kSWFPath(self):
		#7k7k可能用户是复制前一个界面的地址弄上去了
		if self.url.find("7k7k.com/flash/")!=-1:
			url2=self.url.replace("7k7k.com/flash/","7k7k.com/swf/")
			self.setInfo(url2,self.appendix,self.site)
		try:
			response = requests.get(self.url, headers=self.header1)
			response.encoding = 'utf-8'
			htmlContent = response.text
			# 查找游戏名称
			gameName=HtmlAnalyse.Get7k7kGameName(htmlContent)
			# 查找SWF路径
			swfPath = HtmlAnalyse.Get7k7kDirectSwfPath(htmlContent)
			if not swfPath:
				newpagePath=HtmlAnalyse.Get7k7kNewPagePath(htmlContent)
				if not newpagePath:
					messagebox.showerror("错误", "无法找到游戏的SWF文件")
					return
				response2 = requests.get(newpagePath, headers=self.header2)
				response2.encoding = 'utf-8'
				newpageContent = response2.text
				swfPath=HtmlAnalyse.Get7k7kSwfPathInNewPage(newpageContent,newpagePath)
				if not swfPath:
					messagebox.showerror("错误", "这是html5或其它游戏，本程序无法下载")
					return
				else:
					parentPath=newpagePath
			else:
				parentPath=self.url
		except Exception as e:
			messagebox.showerror("错误", f"下载失败: {str(e)}")
			return
		self.swfpathVariable.set(f"找到的SWF路径: {swfPath}")
		return (gameName,swfPath,parentPath)
	
	def get17yySWFPath(self):
		#17yy可能用户是复制前一个界面的地址弄上去了
		if self.url.find("17yy.com/f/")!=-1:
			if self.url.find("17yy.com/f/play/")==-1:
				url2=self.url.replace("17yy.com/f/","17yy.com/f/play/")
				self.setInfo(url2,self.appendix,self.site)
		try:
			response = requests.get(self.url, headers=self.header1)
			response.encoding = 'gbk'
			htmlContent = response.text
			# 查找游戏名称
			gameName=HtmlAnalyse.Get17yyGameName(htmlContent)
			gameCategory=HtmlAnalyse.Get17yyGameCategory(htmlContent)
			if not gameCategory:
				messagebox.showerror("错误","无法获取游戏类型")
				return
			# 查找SWF路径
			gameid=HtmlAnalyse.Get17yyGameID(htmlContent,self.url)
			if gameid==-1:
				messagebox.showerror("错误","无法获取游戏ID")
				return
			apiURL = "http://www.17yy.com/e/payapi/vip_ajax.php"
			postData = {
				"action": "getStatus",
				"id": gameid
			}
			result = PHPTool.callPhpApi(apiURL, data=postData, method="POST")
			if not result:
				return
			latterpath=result['data']['game_path']
			if len(latterpath)==0:
				messagebox.showerror("错误", f"php未返回游戏路径。重试可能能解决")
				return
			gotPath = "http://img1.17yy.com/swf/"+gameCategory+"/"+latterpath
			if gotPath.endswith(".swf"):
				swfPath=gotPath
				parentPath=self.url
			else:
				if gotPath.endswith(".htm") or gotPath.endswith(".html"):
					response2 = requests.get(gotPath, headers=self.header2)
					response2.encoding = 'gbk'
					newpageContent = response2.text
					swfPath=HtmlAnalyse.Get17yySwfPathInNewPage(newpageContent,gotPath)
					if not swfPath:
						messagebox.showerror("错误", "这是html5或其它游戏，本程序无法下载")
						return
					else:
						parentPath=gotPath
				else:
					messagebox.showerror("错误", f"未知类型的路径{gotPath}")
					return
		except Exception as e:
			messagebox.showerror("错误", f"下载失败: {str(e)}")
			return
		self.swfpathVariable.set(f"找到的SWF路径: {swfPath}")
		return (gameName,swfPath,parentPath)
	def getSWFPathWithAppendix(self,appendix):
		if not appendix:
			return ""
		result=HtmlAnalyse.appendixToURL(appendix)
		if not result:
			messagebox.showwarning("警告", "未知站点")
			return ""
		url=result[0]
		site=result[1]
		self.setInfo(url,appendix,site)
		result=self.getSWFPath()
		if not result:
			return ""
		return result[1]
	def relateDownload(self,path):
		realNetPath=self.relateDownloadFolderNetPath+path
		realLocalPath=os.path.join(self.localFolder,path)
		try:
			response = requests.get(realNetPath, headers=self.header3)
			lastFolder=os.path.dirname(realLocalPath)
			os.makedirs(lastFolder,exist_ok=True)
			with open(realLocalPath, 'wb') as f:
				f.write(response.content)
			return True
		except Exception as e:
			messagebox.showerror("错误", f"下载 {path} 失败: {str(e)}")
			return

class Application:
	def __init__(self, root):
		self.root = root
		self.root.title("常见网站flash游戏下载器 - 干大事的魔法师")
		self.root.geometry("720x540")
		self.gd=GameDownloader()
		if not os.path.isdir(CONST.downloadDir):
			os.makedirs(CONST.downloadDir) # 创建下载目录
		self.setupUI() # 绘制ui
		self.gameInfo_list=[]
		self.refreshGameList() # 刷新列表
	
	def setupUI(self):
		# 绘制ui
		# 顶部输入区域
		input_frame = ttk.Frame(self.root, padding="10")
		input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
		ttk.Label(input_frame, text="游戏URL:").grid(row=0, column=0, sticky=tk.W)
		self.url_entry = ttk.Entry(input_frame, width=70)
		self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
		# 按钮区域
		button_frame = ttk.Frame(self.root, padding="10")
		button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
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
		list_frame.grid(row=2, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
		# 创建列表和滚动条
		self.game_list = tk.Listbox(list_frame, height=20)
		scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.game_list.yview)
		self.game_list.configure(yscrollcommand=scrollbar.set)
		self.game_list.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
		scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
		# 按钮区域2
		button_frame2 = ttk.Frame(self.root, padding="10")
		button_frame2.grid(row=3, column=0, sticky=(tk.W, tk.E))
		self.delete_btn=ttk.Button(button_frame2, text="删除", command=self.btn_deleteGame)
		self.delete_btn.grid(row=0, column=0, padx=5)
		self.deleteAll_btn=ttk.Button(button_frame2, text="全部删除", command=self.btn_deleteAllGames)
		self.deleteAll_btn.grid(row=0, column=1, padx=5)
		self.refresh_btn=ttk.Button(button_frame2, text="刷新列表", command=self.btn_refreshGameList)
		self.refresh_btn.grid(row=0, column=2, padx=5)
		# 状态栏
		self.info_var = tk.StringVar()
		self.info_var.set("找到的SWF路径:")
		self.gd.setSwfpathVariable(self.info_var)
		info_entry = ttk.Entry(self.root, textvariable=self.info_var, state='readonly', foreground='blue')
		info_entry.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=5)
		self.status_var = tk.StringVar()
		self.status_var.set("V1.0，支持4399、7k7k、17yy")
		status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
		status_bar.grid(row=5, column=0, sticky=(tk.W, tk.E))
		# 配置网格权重
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(2, weight=1)
		list_frame.columnconfigure(0, weight=1)
		list_frame.rowconfigure(0, weight=1)
		# 绑定事件
		self.game_list.bind('<Double-Button-1>', self.on_doubleClick)
		self.game_list.bind('<<ListboxSelect>>', self.on_selectionChange)
	
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
	def on_selectionChange(self, event):
		self.selectionChange()
	
	def getSelectedIndex(self):
		# 获取选中的位置
		selection = self.game_list.curselection()
		if not selection:
			messagebox.showinfo("提示", "请先选择一个游戏")
			return None
		return selection[0]
		return self.game_list.get(selection[0])
	def getInputURL(self):
		url = self.url_entry.get().strip()
		if not url:
			messagebox.showinfo("提示", "请输入游戏URL，如https://www.4399.com/flash/6853.htm")
			return None
		return url
	def refreshGameList(self,showStatus=False):
		# 刷新列表
		self.game_list.delete(0, tk.END)
		self.gameInfo_list=[]
		try:
			items = os.listdir(CONST.downloadDir)
			for item in items:
				item_path = os.path.join(CONST.downloadDir, item)
				if os.path.isdir(item_path):
					self.game_list.insert(tk.END, f"{item}/")
					item_path2 = os.path.join(item_path, item+".swf")
					self.gameInfo_list.append(('folder', item, item_path2, HtmlAnalyse.getNameAppendixOfFile(item,'folder')))
					continue
				if os.path.isfile(item_path) and item.endswith('.swf'):
					self.game_list.insert(tk.END, f"{item}")
					self.gameInfo_list.append(('file', item, item_path, HtmlAnalyse.getNameAppendixOfFile(item,'file')))
					continue
		except Exception as e:
			messagebox.showerror("错误", f"无法读取游戏列表: {str(e)}")
		if showStatus:
			self.status_var.set(f"找到 {len(self.gameInfo_list)} 个游戏")
		if self.game_list.size()>=1:
			self.deleteAll_btn.config(state=tk.NORMAL)
		else:
			self.deleteAll_btn.config(state=tk.DISABLED)
		self.selectionChange()
	def selectionChange(self):
		# 改变选择
		selection = self.game_list.curselection()
		if not selection:
			self.play_btn.config(state=tk.DISABLED)
			self.delete_btn.config(state=tk.DISABLED)
			self.putFolder_btn.config(state=tk.DISABLED)
			self.relateDownload_btn.config(state=tk.DISABLED)
			return
		selected_index=selection[0]
		self.play_btn.config(state=tk.NORMAL)
		self.delete_btn.config(state=tk.NORMAL)
		if self.gameInfo_list[selected_index][0]=='file':
			self.putFolder_btn.config(state=tk.NORMAL)
			self.relateDownload_btn.config(state=tk.DISABLED)
		elif self.gameInfo_list[selected_index][0]=='folder':
			self.putFolder_btn.config(state=tk.DISABLED)
			self.relateDownload_btn.config(state=tk.NORMAL)
	
	def downloadGame(self,useNewTheard):
		url=self.getInputURL()
		if not url:
			return
		appendix,site=HtmlAnalyse.getURLInfo(url)
		# 不要重复下载
		if appendix!=None:
			for i in range(len(self.gameInfo_list)):
				if self.gameInfo_list[i][3]==appendix:
					self.game_list.selection_clear(0, tk.END)
					self.game_list.selection_set(i)
					self.game_list.see(i)
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
				if self.gameInfo_list[i][1]==downloadFilename:
					self.game_list.selection_clear(0, tk.END)
					self.game_list.selection_set(i)
					self.game_list.see(i)
					self.selectionChange()
					return True
			else:
				messagebox.showerror("错误", "未找到下载的文件")
	def realDownload(self,url,appendix,site):
		# 返回文件名称（除swf）
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
			return
		filePath=self.gameInfo_list[index][2]
		FlashRunner.run(filePath)
	
	def deleteOne(self,filePath,type):
		if not os.path.exists(filePath):
			messagebox.showerror("错误", f"找不到文件/文件夹: {filePath}")
			return
		try:
			if type == 'file':
				os.remove(filePath)
			elif type == 'folder':
				shutil.rmtree(filePath)
			return True
		except Exception as e:
			messagebox.showerror("错误", f"删除失败: {str(e)}")

	def deleteGame(self):
		# 删除选中的游戏
		index = self.getSelectedIndex()
		if index==-1:
			return
		filePath=os.path.join(CONST.downloadDir, self.gameInfo_list[index][1])
		if messagebox.askyesno("确认", f"确定要删除 {self.gameInfo_list[index][1]} 吗? "):
			result=self.deleteOne(filePath,self.gameInfo_list[index][0])
			if result:
				self.status_var.set(f"已删除: {self.gameInfo_list[index][1]}")
			self.refreshGameList()
	
	def deleteAllGames(self):
		# 删除所有游戏
		if len(self.gameInfo_list)==0:
			messagebox.showinfo("信息", "没有可删除的游戏")
			return
		if messagebox.askyesno("确认", f"确定要删除这 {len(self.gameInfo_list)} 个游戏吗?!"):
			for i in range(len(self.gameInfo_list)):
				filePath=os.path.join(CONST.downloadDir, self.gameInfo_list[i][1])
				self.deleteOne(filePath,self.gameInfo_list[i][0])
			self.status_var.set("已删除所有游戏")
			self.refreshGameList()
	def putIntoFolder(self):
		index = self.getSelectedIndex()
		if index==-1:
			return
		if self.gameInfo_list[index][0]=='folder':
			messagebox.showerror("错误", f"只能对swf文件操作")
			return
		realName=self.gameInfo_list[index][1][:-4]
		try:
			folderPath=os.path.join(CONST.downloadDir, realName)
			os.makedirs(folderPath)
			gamePath=os.path.join(folderPath, realName+".swf")
			os.rename(self.gameInfo_list[index][2],gamePath)
			netSWFPath=self.gd.getSWFPathWithAppendix(self.gameInfo_list[index][3])
			iniPath=os.path.join(folderPath, "SWFNetPath.ini")
			with open(iniPath,"w") as f:
				f.write(netSWFPath+"\n")
		except Exception as e:
			messagebox.showerror("错误", f"装入文件夹失败: {str(e)}")
		self.status_var.set("装入文件夹成功")
		self.refreshGameList()
		for i in range(len(self.gameInfo_list)):
			if self.gameInfo_list[i][1]==realName:
				self.game_list.selection_clear(0, tk.END)
				self.game_list.selection_set(i)
				self.game_list.see(i)
				self.selectionChange()
				break
		else:
			messagebox.showerror("错误", "未找到装好的文件")
			return
	def relateDownloader(self):
		index = self.getSelectedIndex()
		if index==-1:
			return
		if self.gameInfo_list[index][0]=='file':
			messagebox.showerror("错误", f"只能对文件夹操作")
			return
		RelatedDownloader(self.root,self.gameInfo_list[index][1],self.gameInfo_list[index][2],self.gd)

class RelatedDownloader:
	def __init__(self, parent, gameName, swfPath,gd):
		self.parent = parent
		self.gameName = gameName
		self.swfPath=swfPath
		self.folderpath=os.path.dirname(self.swfPath)
		self.gd=gd
		self.read_ini_file()
		self.cancelFlag = False
		self.isdownloading = False
		self.gd.localFolder=self.folderpath
		# 创建新窗口
		self.window = tk.Toplevel(parent)
		self.window.title("关联文件下载器")
		self.window.geometry("450x350")
		self.window.transient(parent)
		self.window.grab_set()
		self.setupUI()
		self.updateBtnStatus()
		self.centerWindow()
	def centerWindow(self):
		self.window.update_idletasks()
		width = self.window.winfo_width()
		height = self.window.winfo_height()
		x = (self.window.winfo_screenwidth() // 2) - (width // 2)
		y = (self.window.winfo_screenheight() // 2) - (height // 2)
		self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
	def read_ini_file(self):
		iniPath=os.path.join(self.folderpath,"SWFNetPath.ini")
		if os.path.exists(iniPath):
			with open(iniPath,"r") as f:
				SWFNetPath=f.readline().strip()
				self.gd.setSWFNetPath(SWFNetPath)
		else:
			messagebox.showwarning("警告",f"找不到文件 {iniPath}")
			self.gd.setSWFNetPath("")
	def setupUI(self):
		ttk.Label(self.window, text="游戏名称：").grid(
			row=0, column=0, sticky=tk.W, padx=10, pady=5)
		ttk.Label(self.window, text=self.gameName).grid(
			row=0, column=1, sticky=tk.W, padx=0, pady=5)
		self.netPath_var = tk.StringVar()
		self.netPath_var.set(self.gd.relateDownloadSWFNetPath)
		ttk.Label(self.window, text="网络路径：").grid(
			row=1, column=0, sticky=tk.W, padx=10, pady=5)
		ttk.Entry(self.window, textvariable=self.netPath_var, state='readonly').grid(
			row=1, column=1, sticky=(tk.W,tk.E), padx=0, pady=5)
		self.changeNetPathBtn=ttk.Button(self.window, text="修改", command=self.btn_openEditDialog)
		self.changeNetPathBtn.grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)
		# 文件列表输入框
		download_frame = ttk.Frame(self.window)
		download_frame.grid(row=2, column=0, columnspan=3, pady=5, sticky=(tk.S,tk.W))
		ttk.Label(download_frame, text="要下载的文件:").grid(
			row=0, column=0, sticky=tk.W, padx=5)
		self.downloadInfo_var = tk.StringVar()
		self.downloadInfo_var.set("")
		ttk.Label(download_frame, textvariable=self.downloadInfo_var).grid(
			row=0, column=1, sticky=tk.W, padx=5)
		ttk.Button(download_frame, text="清除内容", command=self.btn_clearText).grid(
			row=0, column=0, padx=5)
		#输入框
		self.files_text = scrolledtext.ScrolledText(self.window, width=40, height=10)
		self.files_text.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky=(tk.N, tk.S, tk.W, tk.E))
		# 按钮框架
		button_frame = ttk.Frame(self.window)
		button_frame.grid(row=4, column=0, columnspan=3, pady=10, sticky=(tk.S,tk.W))
		self.BatchDownloadBtn=ttk.Button(button_frame, text="批量下载", command=self.btn_batchDownload)
		self.BatchDownloadBtn.grid(row=0, column=0, padx=5)
		self.CancelDownloadBtn=ttk.Button(button_frame, text="取消下载", command=self.btn_cancelDownload)
		self.CancelDownloadBtn.grid(row=0, column=1, padx=5)
		ttk.Button(button_frame, text="尝试游玩", command=self.btn_tryPlay).grid(row=0, column=2, padx=5)
		self.ExitBtn=ttk.Button(button_frame, text="退出", command=self.window.destroy)
		self.ExitBtn.grid(row=0, column=3, padx=5)
		# 配置网格权重
		self.window.columnconfigure(1, weight=1)
		self.window.rowconfigure(3, weight=1)
		#关闭窗口时
		self.window.protocol("WM_DELETE_WINDOW", self.on_close)
	def on_close(self):
		# 关闭窗口时
		if self.isdownloading:
			messagebox.showinfo("提示", "请先等待下载完成")
		else:
			self.window.destroy()
	def updateBtnStatus(self):
		if self.isdownloading:
			self.changeNetPathBtn.config(state=tk.DISABLED)
			self.BatchDownloadBtn.config(state=tk.DISABLED)
			self.CancelDownloadBtn.config(state=tk.NORMAL)
			self.ExitBtn.config(state=tk.DISABLED)
		else:
			self.changeNetPathBtn.config(state=tk.NORMAL)
			self.BatchDownloadBtn.config(state=tk.NORMAL)
			self.CancelDownloadBtn.config(state=tk.DISABLED)
			self.ExitBtn.config(state=tk.NORMAL)
	
	def btn_cancelDownload(self):
		self.cancelFlag=True
		self.downloadInfo_var.set("取消中...")

	def btn_clearText(self):
		self.files_text.delete("1.0",tk.END)
	def btn_openEditDialog(self):
		EditNetPathDialog(self.window,self.gameName, self.folderpath, self.gd,
			lambda:self.netPath_var.set(self.gd.relateDownloadSWFNetPath))
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
		FlashRunner.run(self.swfPath)
	def thread_batchDownload(self,things):
		allNum=len(things)
		success=0
		self.gd.setHeader3(self.gd.relateDownloadSWFNetPath)
		for i in range(allNum):
			self.downloadInfo_var.set(f"下载第 {i}/{allNum} 个文件...")
			result=self.gd.relateDownload(things[i])
			if result:
				success+=1
			if self.cancelFlag:
				self.downloadInfo_var.set(f"取消成功，尝试下载 {i}/{allNum} 个，成功 {success} 个，但不排除404网页")
				break
		else:
			self.downloadInfo_var.set(f"尝试下载了 {allNum} 个文件，成功 {success} 个，但不排除404网页")
		self.isdownloading=False
		self.updateBtnStatus()


class EditNetPathDialog:
	def __init__(self, parent,gameName, folderpath, gd,callback):
		self.parent = parent
		self.gameName = gameName
		self.folderpath = folderpath
		self.gd = gd
		self.callback=callback
		# 创建新窗口
		self.window = tk.Toplevel(parent)
		self.window.title("修改网络路径")
		self.window.geometry("450x110")
		self.window.transient(parent)
		self.window.grab_set()
		self.setupUI()
		self.centerWindow()
	def centerWindow(self):
		self.window.update_idletasks()
		width = self.window.winfo_width()
		height = self.window.winfo_height()
		x = (self.window.winfo_screenwidth() // 2) - (width // 2)
		y = (self.window.winfo_screenheight() // 2) - (height // 2)
		self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
	def setupUI(self):
		ttk.Label(self.window, text="请输入网络路径：").grid(
			row=0, column=0, sticky=tk.W, padx=5, pady=5)
		self.path_var = tk.StringVar(value=self.gd.relateDownloadSWFNetPath)
		self.status_var = tk.StringVar()
		self.status_var.set("")
		status_bar = ttk.Label(self.window, textvariable=self.status_var, anchor=tk.W)
		status_bar.grid(row=0, column=1, sticky=tk.W, padx=5)
		#第二行
		self.path_entry = ttk.Entry(self.window, textvariable=self.path_var, width=40)
		self.path_entry.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=(tk.W, tk.E))
		button_frame = ttk.Frame(self.window)
		button_frame.grid(row=2, column=0, columnspan=3, pady=5,sticky=(tk.W))
		ttk.Button(button_frame, text="自动识别", command=self.btn_autoDetect).grid(row=0, column=0, padx=5)
		ttk.Button(button_frame, text="确定", command=self.btn_confirm).grid(row=0, column=1, padx=5)
		ttk.Button(button_frame, text="取消", command=self.window.destroy).grid(row=0, column=2, padx=5)
		self.window.columnconfigure(1, weight=1)
	def btn_autoDetect(self):
		appendix=HtmlAnalyse.getNameAppendixOfFile(self.gameName,'folder')
		if appendix!=None:
			netSWFPath=self.gd.getSWFPathWithAppendix(appendix)
			if netSWFPath!="":
				self.path_var.set(netSWFPath)
				self.status_var.set("（自动识别成功！）")
				return
		messagebox.showerror("错误","自动识别网络路径失败")
		return
	def btn_confirm(self):
		newPath = self.path_var.get().strip()
		self.gd.setSWFNetPath(newPath)
		self.saveINIFile()
		self.callback()
		self.window.destroy()
	def saveINIFile(self):
		iniPath=os.path.join(self.folderpath,"SWFNetPath.ini")
		try:
			with open(iniPath,"w") as f:
				f.write(self.gd.relateDownloadSWFNetPath+"\n")
		except Exception as e:
			messagebox.showerror("错误", f"保存失败: {str(e)}")

if __name__ == "__main__":
	CONST.downloadDir="./FlashDownloads"
	CONST.flashPlayerPath="./tool/FlashPlayer.exe"
	root = tk.Tk()
	app = Application(root)
	root.mainloop()
