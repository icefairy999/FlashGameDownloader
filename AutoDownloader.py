#用于自动下载的处理
from PortServer import *
from Common import *
import threading
import time

class AutoDownloader:
	def __init__(self, gd):
		self.isWorking=False
		self.isAutoDownloading=False
		self.downloadOk=True

		self.totalTaskNum=0
		self.loadingTaskNum=0
		self.successTaskNum=0
		self.notFoundTaskNum=0
		self.failTaskNum=0
		self.statusUpdated=False
		self.lastDownloading=""
		self.lastDownloadOk=False

		self.downloadedList=[]

		self.textList=CycleList(200)
		self.textListNextCount=1
		self.textListUpdated=False

		self.localRelaBase=None
		self.gameRelaName=None

		self.lock=threading.Lock()
		self.statusLock=threading.Lock()
		self.downListLock=threading.Lock()
		self.gd=gd

		Global.portServer.on_request_start=self.on_request_start
		Global.portServer.on_request_end=self.on_request_end
		#这是一个十分诡异的决定，portServer是全局的，而AutoDownloader是实例对象。这样无法处理多个AutoDownloader的情况，虽然用不到，只是代码看起来很奇怪而已
	
	def InitNewProject(self, localRelaBase, gameRelaName):
		self.localRelaBase=localRelaBase
		self.gameRelaName=gameRelaName
		with self.downListLock:
			self.downloadedList.clear()
		with self.statusLock:
			self.totalTaskNum=0
			self.loadingTaskNum=0
			self.successTaskNum=0
			self.notFoundTaskNum=0
			self.failTaskNum=0
			self.statusUpdated=True
			self.lastDownloading=""
			self.lastDownloadOk=True
			self.downloadOk=True
	
	def DestoryProject(self):
		pass

	def startRecord(self):
		self.clearTextList()
		self.isWorking=True

	def exitRecord(self):
		if not self.isWorking:
			return
		self.isWorking=False

	def startAutoDownloading(self):
		self.isAutoDownloading=True

	def stopAutoDownloading(self):
		self.isAutoDownloading=False

	def clearTextList(self):
		with self.lock:
			self.textList.clear()
			self.textListNextCount=1
			self.textListUpdated=True

	def on_request_start(self, client_addr, command, path):
		if not self.isAutoDownloading:
			return
		pathResult=HtmlAnalyse.getBatchDownloadRelativePath(self.localRelaBase, path)
		if pathResult=="":
			return
		#现在相对路径已经得到了，并且结果是安全的，开始正式下载
		#特殊排除
		if pathResult==self.gameRelaName:
			return #对自己的读取不算，因为我们有统一的命名，4399不是这个名
		#绝对路径
		realLocalPath=os.path.join(self.gd.localFolder, pathResult)
		#看看是不是已下载过
		with self.downListLock:
			if pathResult in self.downloadedList:
				return
		#看看是不是已存在
		if os.path.exists(realLocalPath):
			return
		#下载
		with self.downListLock:
			if pathResult in self.downloadedList:
				return
			self.downloadedList.append(pathResult)
			#添加进下载列表先，下载失败再说
		#直接下载，绝对不要用线程，线程下载速度跟不上，网页直接加载失败，还要刷新，得不偿失
		with self.statusLock:
			if not self.isAutoDownloading:
				return
			self.downloadOk=False
			self.lastDownloading=pathResult
			self.lastDownloadOk=False
			self.totalTaskNum+=1
			self.loadingTaskNum+=1
			self.statusUpdated=True
		try:
			result=self.gd.relateDownload(pathResult,False)
		except Exception as e:
			with self.lock:
				self.textList.append(f"{self.textListNextCount}. [错误]{str(e)}")
				self.textListNextCount+=1
				self.textListUpdated=True
			result=0
		if result==-1:
			with self.lock:
				self.textList.append(f"{self.textListNextCount}. [下载404]{pathResult} (自动删掉)")
				self.textListNextCount+=1
				self.textListUpdated=True
			os.remove(realLocalPath)
		with self.statusLock:
			self.loadingTaskNum-=1
			if result==1: #成功
				self.successTaskNum+=1
			elif result==0: #失败
				self.failTaskNum+=1
			elif result==-1: #404
				self.notFoundTaskNum+=1
			self.statusUpdated=True
			if self.loadingTaskNum==0:
				self.downloadOk=True
			self.lastDownloadOk=True
		if result==0:
			with self.downListLock:
				try:
					self.downloadedList.remove(pathResult)
				except Exception:
					pass

	def on_request_end(self,client_addr, command, path, code):
		if not self.isWorking:
			return
		result=HtmlAnalyse.getBatchDownloadRelativePath(self.localRelaBase, path)
		if result=="":
			return
		if 400<=code<=599:
			with self.lock:
				self.textList.append(f"{self.textListNextCount}. [{code}]{result} ({command})")
				self.textListNextCount+=1
				self.textListUpdated=True
		
class CycleList:
	def __init__(self,maxSize):
		self.maxSize=maxSize
		self.data=[None for _ in range(self.maxSize)]
		self.nowCount=0
		self.visibleItemNum=0
		self.clear()

	def clear(self):
		self.nowCount=0
		self.visibleItemNum=0
		for i in range(self.maxSize):
			self.data[i]=None

	def append(self,item):
		self.data[self.nowCount%self.maxSize]=item
		self.nowCount+=1
		self.visibleItemNum+=1
		if self.visibleItemNum>self.maxSize:
			self.visibleItemNum=self.maxSize
	def getLast(self,num):
		#num为0到99
		return self.data[(self.nowCount-1-num)%self.maxSize]
	