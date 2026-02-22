#存放常量
from HtmlAnalyse import *
class Global:
	downloadDir=None
	flashPlayerPath=None
	port=None
	localhostDir=None
	downloadLocalhostPath=None
	portServer=None
	flashPagePath=None

class InfoItem:
	def __init__(self, type, FileOrFolderName):
		self.type=type
		if type=='folder':
			self.folderName=FileOrFolderName
			self.gameName=HtmlAnalyse.getGameNameOfFolder(FileOrFolderName)
			self.folderExt=HtmlAnalyse.getNameExtOfFolder(FileOrFolderName)
			self.gameRelaPath=os.path.join(FileOrFolderName,self.gameName+self.folderExt)
			self.gameFullPath=os.path.join(Global.downloadDir,self.gameRelaPath)
			self.folderRelaPath=self.folderName
			self.folderFullPath=os.path.join(Global.downloadDir,self.folderRelaPath)
			self.gameAppendix=HtmlAnalyse.getNameAppendixOfFile(FileOrFolderName,'folder')
			self.fileOrFolderName=FileOrFolderName
			self.displayText=FileOrFolderName+'/'
			self.iniFullPath=os.path.join(self.folderFullPath,"SWFNetPath.ini")
		elif type=='file':
			self.swfFileName=FileOrFolderName
			self.gameName=FileOrFolderName[:-4]
			self.gameAppendix=HtmlAnalyse.getNameAppendixOfFile(FileOrFolderName,'file')
			self.gameRelaPath=FileOrFolderName
			self.gameFullPath=os.path.join(Global.downloadDir,self.gameRelaPath)
			self.fileOrFolderName=FileOrFolderName
			self.displayText=FileOrFolderName

class DownloadResult:
	def __init__(self):
		self.type=None
		self.originUrl=None
		self.isNewPage=None
		self.newPageUrl=None
		self.swfUrl=None
		self.gameCleanName=None
		self.gameWidth=None
		self.gameHeight=None
		self.alreayContent=None

class IniResult:
	def __init__(self, iniFullPath, folderExt="undefined"):
		self.type=None
		self.netPath=None
		self.isNewPage=None
		self.newPageUrl=None
		self.width=None
		self.height=None
		self.errmsg=None
		self.iniFullPath=iniFullPath
		self.folderExt=folderExt

	@staticmethod
	def fromFile(iniFullPath,folderExt):
		rtn=IniResult(iniFullPath,folderExt)
		rtn.readFile()
		return rtn
	
	def readFile(self):
		# folderExt填.swf或.htm
		self.errmsg=""
		if not os.path.isfile(self.iniFullPath):
			self.type="notexist"
			self.errmsg+=f"文件不存在. "
			return
		with open(self.iniFullPath,"r") as f:
			self.netPath=f.readline().strip()
			self.type=f.readline().strip()
			if self.folderExt==".swf":
				if self.type=="swf":
					temp=f.readline().strip()
					temp2=IniResult._strToInt(temp)
					if temp2==-2:
						self.errmsg+=f"第三行应为正整数|Unknown，而非{temp}. "
						temp2=-1
					self.width=temp2
					temp=f.readline().strip()
					temp2=IniResult._strToInt(temp)
					if temp2==-2:
						self.errmsg+=f"第四行应为正整数|Unknown，而非{temp}. "
						temp2=-1
					self.height=temp2
					temp=f.readline().strip()
					if temp=="True":
						self.isNewPage=1
					elif temp=="False":
						self.isNewPage=0
					elif temp=="Unknown":
						self.isNewPage=-1
					else:
						self.isNewPage=-1
						self.errmsg+=f"第五行只能为True|False|Unknown，而非{temp}. "
					if self.isNewPage==1:
						self.newPageUrl=f.readline().strip()
					if len(f.readline())>0:
						self.errmsg+=f"文件有冗余. "
					return
				elif self.type=="":
					self.type="swf"
					self.width=-1
					self.height=-1
					self.isNewPage=-1
					self.errmsg+=f"版本更新，旧的SWFNetPath.ini需要更改. "
					if len(f.readline())>0:
						self.errmsg+=f"文件有冗余. "
					return
				else:
					self.errmsg+=f"类型不匹配，应为swf，实为{self.type}. "
					self.type="swf"
					self.isNewPage=-1
					return
			elif self.folderExt==".htm":
				if self.type=="htm":
					temp=f.readline().strip()
					temp2=IniResult._strToInt(temp)
					if temp2==-2:
						self.errmsg+=f"第三行应为正整数|Unknown，而非{temp}. "
						temp2=-1
					self.width=temp2
					temp=f.readline().strip()
					temp2=IniResult._strToInt(temp)
					if temp2==-2:
						self.errmsg+=f"第四行应为正整数|Unknown，而非{temp}. "
						temp2=-1
					self.height=temp2
					if len(f.readline())>0:
						self.errmsg+=f"文件有冗余. "
					return
				else:
					self.errmsg+=f"类型不匹配，应为htm，实为{self.type}. "
					self.type="htm"
					self.width=-1
					self.height=-1
					return
			else:
				if self.type=="unknown":
					if len(f.readline())>0:
						self.errmsg+=f"文件有冗余. "
					return
				else:
					self.errmsg+=f"类型不匹配，应为unknown，实为{self.type}. "
					self.type="unknown"
				return
	def WriteFile(self):
		if self.type=="swf":
			try:
				with open(self.iniFullPath,"w") as f:
					f.write(self.netPath)
					f.write("\n"+"swf")
					if self.width>0:
						f.write("\n"+str(self.width))
					else:
						f.write("\n"+"Unknown")
					if self.height>0:
						f.write("\n"+str(self.height))
					else:
						f.write("\n"+"Unknown")
					if self.isNewPage==1:
						f.write("\n"+"True")
					elif self.isNewPage==0:
						f.write("\n"+"False")
					elif self.isNewPage==-1:
						f.write("\n"+"Unknown")
					else:
						raise Exception(f"未知isNewPage值: {self.isNewPage}")
					if self.isNewPage==1:
						f.write("\n"+self.newPageUrl)
			except Exception as e:
				raise Exception(f"写入文件时发生错误: {str(e)}")
		elif self.type=="htm":
			try:
				with open(self.iniFullPath,"w") as f:
					f.write(self.netPath)
					f.write("\n"+"htm")
					if self.width>0:
						f.write("\n"+str(self.width))
					else:
						f.write("\n"+"Unknown")
					if self.height>0:
						f.write("\n"+str(self.height))
					else:
						f.write("\n"+"Unknown")
			except Exception as e:
				raise Exception(f"写入文件时发生错误: {str(e)}")
		elif self.type=="unknown":
			try:
				with open(self.iniFullPath,"w") as f:
					f.write(self.netPath)
					f.write("\n"+"unknown")
			except Exception as e:
				raise Exception(f"写入文件时发生错误: {str(e)}")
		else:
			raise Exception(f"未知type值: {self.type}")
	def ShowInfo(self):
		# 将信息显示为字符串
		rtn=""
		err1=""
		err2=""
		err3=""
		if self.errmsg:
			err1="[错误]"
			err2=f"{self.errmsg}| "
			err3=f"- {self.iniFullPath}"
		if self.type=="swf":
			info1=""
			info2=""
			info3=""
			info4=""
			if self.width>0:
				info3=f"{self.width}"
			else:
				info3=f"未知"
			if self.height>0:
				info4=f"{self.height}"
			else:
				info4=f"未知"
			if self.isNewPage==1:
				info1=f"新页面:True "
				info2=f"路径: {self.newPageUrl} "
			elif self.isNewPage==0:
				info1=f"新页面:False "
			elif self.isNewPage==-1:
				info1=f"新页面:未知 "
			rtn=f"{err1}{err2}大小:{info3}x{info4} {info1}{info2}{err3}"
		elif self.type=="htm":
			if self.width>0:
				info2=f"{self.width}"
			else:
				info2=f"未知"
			if self.height>0:
				info3=f"{self.height}"
			else:
				info3=f"未知"
			rtn=f"{err1}{err2}大小:{info2}x{info3} {err3}"
		else:
			rtn=f"{err1}{err2}{err3}"
		return rtn

	@staticmethod
	def _strToInt(value):
		#将正整数字符串转换为数字，Unknown返回-1，不规范返回-2
		if value == "Unknown":
			return -1
		if not value.isdigit():
			return -2
		try:
			num = int(value)
		except Exception:
			num = -999
		if num > 0:
			return num
		else:
			return -2
	