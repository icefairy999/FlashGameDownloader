#用于正式的下载
import os
import requests
from tkinter import messagebox

from HtmlAnalyse import *
from Common import *
from PHPTool import *
from RelatedDownloader import *


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
		self.header4 = None
	def setSWFNetPath(self,SWFNetPath):
		if not SWFNetPath:
			self.relateDownloadSWFNetPath=""
			self.relateDownloadFolderNetPath=""
			return
		self.relateDownloadSWFNetPath=SWFNetPath
		self.relateDownloadFolderNetPath=HtmlAnalyse.fromSWFPathGetParentPath(SWFNetPath)
		self.header3 = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
			'Referer': self.relateDownloadSWFNetPath
		}
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
	def setHeader4(self,newurl):
		self.header4 = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
			'Referer': newurl
		}
	def getSWFPath(self):
		#返回一个DownloadResult对象
		if self.site=='4399':
			return self.get4399SWFPath()
		elif self.site=='7k7k':
			return self.get7k7kSWFPath()
		elif self.site=='17yy':
			return self.get17yySWFPath()
		else:
			messagebox.showerror("错误","未知站点")
			return None
	def downloadSWF(self):
		#返回文件名字
		result=self.getSWFPath()
		if not result:
			return
		# 处理文件名冲突，但不知有啥意义，因为本身就不能重复下载
		gameName = ""
		counter = 0
		while True:
			if counter==0:
				gameName = f"{result.gameCleanName}_{self.appendix}"
			else:
				gameName = f"{result.gameCleanName}_{counter}_{self.appendix}"
			if result.type=="swf":
				tryFilePath=os.path.join(Global.downloadDir, f"{gameName}.swf")
				if os.path.exists(tryFilePath):
					counter += 1
					continue
			elif result.type=="htm":
				tryFilePath=os.path.join(Global.downloadDir, f"{gameName}h")
				if os.path.exists(tryFilePath):
					counter += 1
					continue
			break			
		# 下载SWF文件
		if result.type=="swf":
			fileRelaName=f"{gameName}.swf"
			fileFullPath = os.path.join(Global.downloadDir, fileRelaName)
			#设置parentPath
			if result.isNewPage:
				parentPath=result.newPageUrl
			else:
				parentPath=result.originUrl
			try:
				self.setHeader4(parentPath)
				swfResponse = requests.get(result.swfUrl, headers=self.header4, timeout=(3,10))
				with open(fileFullPath, 'wb') as f:
					f.write(swfResponse.content)
			except Exception as e:
				messagebox.showerror("错误", f"找到SWF路径但下载失败: {str(e)}")
				return
			return fileRelaName
		elif result.type=="htm":
			#建立文件夹
			folderRelaName=f"{gameName}h"
			folderFullPath=os.path.join(Global.downloadDir, folderRelaName)
			try:
				os.makedirs(folderFullPath,exist_ok=True)
			except Exception as e:
				messagebox.showerror("错误", f"无法创建文件夹{folderFullPath}/: {str(e)}")
				return
			#建立SWFNetPath.ini
			iniRelaPath=os.path.join(folderRelaName,"SWFNetPath.ini")
			iniFullPath=os.path.join(Global.downloadDir, iniRelaPath)
			inirst=IniResult(iniFullPath)
			inirst.type="htm"
			inirst.netPath=result.swfUrl
			inirst.width=result.gameWidth
			inirst.height=result.gameHeight
			try:
				inirst.WriteFile()
			except Exception as e:
				messagebox.showerror("错误", f"写入{inirst.iniFullPath}失败: {str(e)}")
				return
			#最后下载
			htmRelaPath=os.path.join(folderRelaName,gameName+".htm")
			htmFullPath=os.path.join(Global.downloadDir,htmRelaPath)
			try:
				with open(htmFullPath, 'wb') as f:
					f.write(result.alreayContent)
			except Exception as e:
				messagebox.showerror("错误", f"写入文件{htmFullPath}失败: {str(e)}")
				return
			return folderRelaName
		else:
			messagebox.showerror("错误", f"未知的返回类型: {result.type}")
			return
	def get4399SWFPath(self):
		result=DownloadResult()
		result.originUrl=self.url
		try:
			response = requests.get(self.url, headers=self.header1, timeout=(3,10))
			htmlContent, encoding1 = HtmlAnalyse.decodeWebContent(response.content)
			# 查找游戏名称、宽、高
			result.gameCleanName=HtmlAnalyse.toSafeFileName(HtmlAnalyse.Get4399GameName(htmlContent))
			result.gameWidth,result.gameHeight=HtmlAnalyse.Get4399GameWidthHeight(htmlContent)
			# 查找SWF路径
			directSwfPath = HtmlAnalyse.Get4399DirectSwfPath(htmlContent)
			if not directSwfPath:
				newPagePath=HtmlAnalyse.Get4399NewPagePath(htmlContent)
				if not newPagePath:
					messagebox.showerror("错误", "无法找到游戏所在页面")
					return
				response2 = requests.get(newPagePath, headers=self.header2, timeout=(3,10))
				newPageContent, encoding2 = HtmlAnalyse.decodeWebContent(response2.content)
				newSwfPath=HtmlAnalyse.Get4399SwfPathInNewPage(newPageContent,newPagePath)
				if not newSwfPath:
					if HtmlAnalyse.Is4399NewPageH5Wan(newPageContent):
						#H5wan游戏 - 只有4399比较复杂，有个外壳
						newH5Path=HtmlAnalyse.Get4399H5WanGamePath(newPagePath)
						self.setHeader4(newH5Path)
						response3 = requests.get(newH5Path, headers=self.header4, timeout=(3,10))
						h5PageContent, encoding3 = HtmlAnalyse.decodeWebContent(response3.content)
						if HtmlAnalyse.Is4399404Page(h5PageContent):
							messagebox.showwarning("警告","似乎是H5Wan游戏，但似乎又不是")
							result.type='htm'
							result.swfUrl=newPagePath
							result.newPageUrl=newPagePath
							tempText=HtmlAnalyse.Page4399Replace(newPageContent)
							result.alreayContent=tempText.encode(encoding2)
						else:
							result.type='htm'
							result.swfUrl=newH5Path
							result.newPageUrl=newH5Path
							#H5Wan游戏都会加载4399的一个api，有它，广告点不动。我们把它转向我们自己的一个替代api
							tempText=HtmlAnalyse.Page4399Replace(h5PageContent)
							result.alreayContent=tempText.encode(encoding3)
					else:
						result.type='htm'
						result.swfUrl=newPagePath
						result.newPageUrl=newPagePath
						tempText=HtmlAnalyse.Page4399Replace(newPageContent)
						result.alreayContent=tempText.encode(encoding2)
				else:
					result.type='swf'
					result.isNewPage=True
					result.newPageUrl=newPagePath
					result.swfUrl=newSwfPath
			else:
				result.type='swf'
				result.isNewPage=False
				result.swfUrl=directSwfPath
		except Exception as e:
			messagebox.showerror("错误", f"下载失败: {str(e)}")
			return
		self.swfpathVariable.set(f"找到的SWF路径: {result.swfUrl}")
		return result

	def get7k7kSWFPath(self):
		#7k7k可能用户是复制前一个界面的地址弄上去了
		if self.url.find("7k7k.com/flash/")!=-1:
			url2=self.url.replace("7k7k.com/flash/","7k7k.com/swf/")
			self.setInfo(url2,self.appendix,self.site)
		result=DownloadResult()
		result.originUrl=self.url
		try:
			response = requests.get(self.url, headers=self.header1, timeout=(3,10))
			htmlContent, encoding1 = HtmlAnalyse.decodeWebContent(response.content)
			# 查找游戏名称、宽高
			result.gameCleanName=HtmlAnalyse.toSafeFileName(HtmlAnalyse.Get7k7kGameName(htmlContent))
			result.gameWidth,result.gameHeight=HtmlAnalyse.Get7k7kGameWidthHeight(htmlContent)
			# 查找SWF路径
			directSwfPath = HtmlAnalyse.Get7k7kDirectSwfPath(htmlContent)
			if not directSwfPath:
				newPagePath=HtmlAnalyse.Get7k7kNewPagePath(htmlContent)
				if not newPagePath:
					messagebox.showerror("错误", "无法找到游戏所在页面")
					return
				response2 = requests.get(newPagePath, headers=self.header2, timeout=(3,10))
				newPageContent, encoding2 = HtmlAnalyse.decodeWebContent(response2.content)
				newSwfPath=HtmlAnalyse.Get7k7kSwfPathInNewPage(newPageContent,newPagePath)
				if not newSwfPath:
					result.type='htm'
					result.swfUrl=newPagePath
					result.newPageUrl=newPagePath
					tempText=HtmlAnalyse.Page7k7k17yyReplace(newPageContent)
					result.alreayContent=tempText.encode(encoding2)
				else:
					result.type='swf'
					result.isNewPage=True
					result.newPageUrl=newPagePath
					result.swfUrl=newSwfPath
			else:
				result.type='swf'
				result.isNewPage=False
				result.swfUrl=directSwfPath
		except Exception as e:
			messagebox.showerror("错误", f"下载失败: {str(e)}")
			return
		self.swfpathVariable.set(f"找到的SWF路径: {result.swfUrl}")
		return result
	
	def get17yySWFPath(self):
		#17yy可能用户是复制前一个界面的地址弄上去了
		if self.url.find("17yy.com/f/")!=-1:
			if self.url.find("17yy.com/f/play/")==-1:
				url2=self.url.replace("17yy.com/f/","17yy.com/f/play/")
				self.setInfo(url2,self.appendix,self.site)
		result=DownloadResult()
		result.originUrl=self.url
		try:
			response = requests.get(self.url, headers=self.header1, timeout=(3,10))
			htmlContent, encoding1 = HtmlAnalyse.decodeWebContent(response.content)
			# 查找游戏名称
			result.gameCleanName=HtmlAnalyse.toSafeFileName(HtmlAnalyse.Get17yyGameName(htmlContent))
			result.gameWidth,result.gameHeight=HtmlAnalyse.Get17yyGameWidthHeight(htmlContent)
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
			phpResult = PHPTool.callPhpApi(apiURL, data=postData, method="POST")
			if not phpResult:
				return
			latterpath=phpResult['data']['game_path']
			if len(latterpath)==0:
				messagebox.showerror("错误", f"php未返回游戏路径，可能是vip游戏。若不是请重试")
				return
			gotPath = "http://img1.17yy.com/swf/"+gameCategory+"/"+latterpath
			if gotPath.endswith(".swf"):
				result.type='swf'
				result.isNewPage=False
				result.swfUrl=gotPath
			else:
				if gotPath.endswith(".htm") or gotPath.endswith(".html"):
					response2 = requests.get(gotPath, headers=self.header2, timeout=(3,10))
					newPageContent, encoding2 = HtmlAnalyse.decodeWebContent(response2.content)
					newSwfPath=HtmlAnalyse.Get17yySwfPathInNewPage(newPageContent,gotPath)
					if not newSwfPath:
						result.type='htm'
						result.swfUrl=gotPath
						result.newPageUrl=gotPath
						tempText=HtmlAnalyse.Page7k7k17yyReplace(newPageContent)
						result.alreayContent=tempText.encode(encoding2)
					else:
						result.type='swf'
						result.isNewPage=True
						result.newPageUrl=gotPath
						result.swfUrl=newSwfPath
				else:
					messagebox.showerror("错误", f"未知类型的路径{gotPath}")
					return
		except Exception as e:
			messagebox.showerror("错误", f"下载失败: {str(e)}")
			return
		self.swfpathVariable.set(f"找到的SWF路径: {result.swfUrl}")
		return result
	def setInfoWithAppendix(self,appendix):
		if not appendix:
			return ""
		result=HtmlAnalyse.appendixToURL(appendix)
		if not result:
			messagebox.showwarning("警告", "未知站点")
			return ""
		url=result[0]
		site=result[1]
		self.setInfo(url,appendix,site)

	def getSWFPathWithAppendix(self,appendix):
		self.setInfoWithAppendix(appendix)
		result=self.getSWFPath()
		return result

	def relateDownload(self,path,msgboxError=True):
		#请把setSWFNetPath和localFolder设置好先
		#返回:1成功，0失败，-1为404
		realNetPath=HtmlAnalyse.BatchDownloadJoinNetPath(self.relateDownloadFolderNetPath, path)
		if realNetPath=="":
			errText=f"下载 {path} 失败: 路径不规范（含..、特殊字符、空格）且之前未被查出"
			if msgboxError:
				messagebox.showerror("错误", errText)
			else:
				raise Exception(errText)
			return 0
		realLocalPath=os.path.join(self.localFolder,path)
		try:
			response = requests.get(realNetPath, headers=self.header3, timeout=(3,10))
			lastFolder=os.path.dirname(realLocalPath)
			os.makedirs(lastFolder,exist_ok=True)
			with open(realLocalPath, 'wb') as f:
				f.write(response.content)
			#检查一下404
			if HtmlAnalyse.IsAnyone404Page(response.content.decode(encoding='utf-8',errors='ignore')):
				return -1
			return 1
		except Exception as e:
			errText=f"下载 {path} 失败: {str(e)}"
			if msgboxError:
				messagebox.showerror("错误", errText)
			else:
				raise Exception(errText)
			return 0
		return 0
	def downloadMainHtm(self,folderName,gameName,netPath):
		#请于setInfoWithAppendix后使用
		#这里设置folderName，因为有可能是 游戏名_后缀，也可能是 游戏名_后缀_swf
		localRelaPath=os.path.join(folderName,gameName+".htm")
		localFullPath=os.path.join(Global.downloadDir,localRelaPath)
		try:
			response = requests.get(netPath, headers=self.header2, timeout=(3,10))
			with open(localFullPath, 'wb') as f:
				f.write(response.content)
			return True
		except Exception as e:
			messagebox.showerror("错误", f"下载 {netPath} 失败: {str(e)}")
			return