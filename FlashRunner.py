#用于运行swf文件
import os
import subprocess
from Common import *
from tkinter import messagebox
from urllib.parse import urljoin,urlparse,quote
import webbrowser

class FlashRunner:

	@staticmethod
	def playGame(item):
		#输入InfoItem对象
		if item.type=='file':
			FlashRunner.run(item.gameFullPath)
		elif item.type=='folder':
			if item.folderExt=='.swf':
				FlashRunner.run(item.gameFullPath)
			elif item.folderExt==".htm":
				if Global.port>0:
					safeGameName = quote(item.gameName, safe='')
					inirst=IniResult.fromFile(item.iniFullPath,".htm")
					if inirst.width>0:
						width=inirst.width
					else:
						width=800
					if inirst.height>0:
						height=inirst.height
					else:
						height=600
					fullUrl = f"http://localhost:{Global.port}/frame.htm?game={safeGameName}&width={width}&height={height}"
					webbrowser.open(fullUrl)
				else:
					os.startfile(item.gameFullPath)
			else:
				messagebox.showinfo("提示", f"为安全, 只能打开.swf和.htm文件, 这个文件夹标记的扩展名为{item.folderExt}, 不支持打开.")
	
	@staticmethod
	def run(fileFullPath):
		if not os.path.isfile(fileFullPath):
			messagebox.showerror("错误", f"找不到文件: {fileFullPath}")
			return
		try:
			if not os.path.exists(Global.flashPlayerPath):
				messagebox.showwarning("警告", "未找到tool/FlashPlayer.exe")
				os.startfile(fileFullPath)
			else:
				subprocess.Popen([Global.flashPlayerPath, fileFullPath])
		except Exception as e:
			messagebox.showerror("错误", f"无法运行游戏: {str(e)}")
