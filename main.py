import tkinter as tk
from Common import *
from Application import *
from PortServer import *
from tkinter import messagebox

if __name__ == "__main__":
	Global.localhostDir="."
	Global.downloadLocalhostPath="FlashDownloads/"
	Global.downloadDir="./FlashDownloads"
	Global.flashPlayerPath="./tool/FlashPlayer.exe"
	Global.flashPagePath="./tool/FlashPage.htm"
	ps=PortServer(1055)
	ps.start(Global.localhostDir) #在当前目录下建立
	if ps.port>0:
		Global.port=ps.port
	else:
		messagebox.showwarning("警告","无法找到可用端口, 只能像普通文件一样运行htm文件, 有的游戏可能不能正常运行.")
		Global.port=-1
	Global.portServer=ps
	root = tk.Tk()
	app = Application(root)
	root.mainloop()
