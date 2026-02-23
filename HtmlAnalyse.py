#用于各种文本处理
import os.path
import re
from urllib.parse import urljoin,urlparse,quote,unquote
from pathlib import Path

class HtmlAnalyse:

	@staticmethod
	def toSafeFileName(name):
		"""
		将字符串转换为安全的名字：
		- 删除所有非法字符：/\\:?<>*|
		- 删除点号 .
		- 将下划线 _ 替换为连字符 -
		- 长度小于100
		"""
		# 定义要删除的字符集合
		forbidden_chars = set('/\\:?<>*|. \t\n')
		safe_chars = []
		for ch in name:
			if ch in forbidden_chars:
				# 删除非法字符和点号（点号已在 forbidden_chars 中）
				continue
			elif ch == '_':
				safe_chars.append('-')
			else:
				safe_chars.append(ch)
		result=''.join(safe_chars)
		return result[:100]
	
	@staticmethod
	def getURLFilename(url):
		parsed = urlparse(url)
		clean_path = parsed.path
		filename = os.path.basename(clean_path)
		return filename
	
	@staticmethod
	def getURLExt(url):
		parsed = urlparse(url)
		clean_path = parsed.path
		filename = os.path.basename(clean_path)
		name, ext = os.path.splitext(filename)
		return ext
	
	@staticmethod
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
	
	@staticmethod
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
		
	@staticmethod
	def getNameAppendixOfFile(fileName,type):
		if type=='folder':
			match = re.search(r'_([a-z][0-9]+)[a-z]$',fileName)
			if match:
				return match.group(1)
			match = re.search(r'_([a-z][0-9]+)$',fileName)
			if match:
				return match.group(1)
			return None
		if type=='file':
			match = re.search(r'_([a-z][0-9]+)\.swf$',fileName)
			if match:
				return match.group(1)
			return None
		
	@staticmethod
	def getNameExtOfFolder(fileName):
		match = re.search(r'_[a-z][0-9]+([a-z])$',fileName)
		if match:
			if match.group(1)=='s':
				return ".swf"
			elif match.group(1)=='h':
				return ".htm"
			else:
				return ".unknown"
		match = re.search(r'_[a-z][0-9]+$',fileName)
		if match:
			return ".swf"
		return ".unknown"

	@staticmethod
	def getGameNameOfFolder(fileName):
		match = re.search(r'_[a-z][0-9]+[a-z]$',fileName)
		if match:
			return fileName[:-1]
		match = re.search(r'_[a-z][0-9]+$',fileName)
		if match:
			return fileName
		return "未知名称"

	@staticmethod
	def getCleanName(gameName):
		match = re.search(r'_[a-z][0-9]+$',gameName)
		if match:
			return gameName[:-len(match.group(0))]
		return gameName

	@staticmethod
	def isOldFolderName(fileName):
		match = re.search(r'_[a-z][0-9]+[a-z]$',fileName)
		if match:
			pass
		else:
			match = re.search(r'_[a-z][0-9]+$',fileName)
			if match:
				return True
		return False

	@staticmethod
	def Get4399GameName(htmlContent):
		match = re.search(r'game_title\s*=\s*\'(.*?)\'', htmlContent)
		if match:
			return match.group(1)
		match = re.search(r'title\s*=\s*\'(.*?)\'', htmlContent)
		if match:
			return match.group(1)
		return "未知名称"
	
	@staticmethod
	def Get4399DirectSwfPath(htmlContent):
		match = re.search(r'_strGamePath\s*=\s*"(.*?\.swf)"', htmlContent)
		if match:
			return "https://sda.4399.com/4399swf"+match.group(1)
		match = re.search(r'src=\'(//sda\.4399\.com/.*?\.swf)\'', htmlContent)
		if match:
			return "https:"+match.group(1)
		return None
	
	@staticmethod
	def Get4399NewPagePath(htmlContent):
		match = re.search(r'_strGamePath\s*=\s*"(.*?\.html?)"', htmlContent)
		if match:
			return "https://sda.4399.com/4399swf"+match.group(1)
		match = re.search(r'src=\'(//sda\.4399\.com/.*?\.html?)\'', htmlContent)
		if match:
			return "https:"+match.group(1)
		return None
	
	@staticmethod
	def Get4399SwfPathInNewPage(htmlContent,newpagePath):
		matchpos = htmlContent.find('id="flashgame"')
		if matchpos==-1:
			return None
		match = re.search(r'src="(.*?\.swf)"', htmlContent[matchpos:])
		if match:
			return urljoin(newpagePath,match.group(1))
		return None
	
	@staticmethod
	def Get4399H5WanGamePath(newpagePath):
		return HtmlAnalyse.fromSWFPathGetParentPath(newpagePath)+"gameIndex.html"
	
	@staticmethod
	def Is4399NewPageUnity(htmlContent):
		if htmlContent.find('WebPlayer.unity3d')!=-1:
			return True
		if htmlContent.find('unityPlayer')!=-1:
			return True
		return False
	
	@staticmethod
	def Is4399NewPageH5Wan(htmlContent):
		if htmlContent.find('h5wan')!=-1:
			return True
		if htmlContent.find('h5api-core')!=-1:
			return True
		return False
	
	@staticmethod
	def Is4399404Page(htmlContent):
		if htmlContent.find('<title>404 Not Found</title>')!=-1:
			return True
		return False
	@staticmethod
	def IsAnyone404Page(htmlContent):
		if htmlContent.find('404 Not Found')!=-1:
			return True
		if htmlContent.find('Document not found')!=-1:
			return True
	
	@staticmethod
	def Get7k7kGameName(htmlContent):
		match = re.search(r'gameName:\s*"(.*?)"', htmlContent)
		if match:
			return match.group(1)
		return "未知名称"
	
	@staticmethod
	def Get7k7kDirectSwfPath(htmlContent):
		match = re.search(r'gamePath:\s*"(.*?\.swf)"', htmlContent)
		if match:
			return match.group(1)
		return None
	
	@staticmethod
	def Get7k7kNewPagePath(htmlContent):
		match = re.search(r'gamePath:\s*"(.*?\.html?)"', htmlContent)
		if match:
			return match.group(1)
		return None
	
	@staticmethod
	def Get7k7kSwfPathInNewPage(htmlContent,newpagePath):
		match = re.search(r'_src_\s*=\s*\'(.*?\.swf)\'', htmlContent)
		if match:
			return urljoin(newpagePath,match.group(1))
		return None
	
	@staticmethod
	def Get17yyGameName(htmlContent):
		match = re.search(r'm7_gamename\s*=\s*"(.*?)"', htmlContent)
		if match:
			return match.group(1)
		match = re.search(r'<title>(.*?)在线玩"', htmlContent)
		if match:
			return match.group(1)
		return "未知名称"
	
	@staticmethod
	def Get17yyGameCategory(htmlContent):
		match = re.search(r'var\s+date\s*=\s*"(.*?)"', htmlContent)
		if match:
			return match.group(1)
		return None
	
	@staticmethod
	def Get17yyGameID(htmlContent,url):
		match = re.search(r'm7_gameid\s*=\s*"([0-9]+)"',htmlContent)
		if match:
			return int(match.group(1))
		match = re.search(r'/([0-9]+)\.html?"',url)
		if match:
			return int(match.group(1))
		return -1
	
	@staticmethod
	def Get17yySwfPathInNewPage(htmlContent,newpagePath):
		return HtmlAnalyse.Get7k7kSwfPathInNewPage(htmlContent,newpagePath)
		#我找不到足够的样本做实验


	@staticmethod
	def Get4399GameWidthHeight(htmlContent):
		#要么返回(-1,-1)，要么返回两个，只有一个不行
		width=-1
		height=-1
		match = re.search(r'_w\s*=\s*(\d+)[,;]', htmlContent)
		if match:
			width=int(match.group(1))
		match = re.search(r'_h\s*=\s*(\d+)[,;]', htmlContent)
		if match:
			height=int(match.group(1))
		if width>0 and height>0:
			return (width,height)
		else:
			return (-1,-1)
	
	@staticmethod
	def Get7k7kGameWidthHeight(htmlContent):
		#要么返回(-1,-1)，要么返回两个，只有一个不行
		width=-1
		height=-1
		match = re.search(r'gamewidth:\s*(\d+),', htmlContent)
		if match:
			width=int(match.group(1))
		match = re.search(r'gameheight:\s*(\d+),', htmlContent)
		if match:
			height=int(match.group(1))
		if width>0 and height>0:
			return (width,height)
		else:
			return (-1,-1)

	@staticmethod
	def Get17yyGameWidthHeight(htmlContent):
		#要么返回(-1,-1)，要么返回两个，只有一个不行
		width=-1
		height=-1
		match = re.search(r'flash_w\s*=\s*(\d+);', htmlContent)
		if match:
			width=int(match.group(1))
		match = re.search(r'flash_h\s*=\s*(\d+);', htmlContent)
		if match:
			height=int(match.group(1))
		if width>0 and height>0:
			return (width,height)
		else:
			return (-1,-1)

	@staticmethod
	def fromSWFPathGetParentPath(SWFNetPath):
		parsed = urlparse(SWFNetPath)
		pathObj = Path(parsed.path)
		dirPath = pathObj.parent.as_posix()
		return f"{parsed.scheme}://{parsed.netloc}{dirPath}/" #必须以/结尾
	
	@staticmethod
	def getBatchDownloadValidName(fileName):
		if '?' in fileName:
			rtn=fileName.split('?', 1)[0]
		else:
			rtn=fileName
		# 绝对禁止..
		if '..' in fileName:
			return ""
		forbidden_chars = set('#[]@!$&\'()*+,;=\"<> |:`')
		for ch in rtn:
			if ch in forbidden_chars:
				return ""
		return rtn

	@staticmethod
	def getBatchDownloadRelativePath(base, target):
		# 如果 target 以 base 为目录开头，则返回 target 相对于 base 的路径（不包含 base 部分）；否则返回空字符串。
		# 路径分隔符自动适应系统，且能安全处理 '..' 等特殊成分。
		target2=HtmlAnalyse.getBatchDownloadValidName(target)
		if target2=="":
			return ""
		norm_base = os.path.normpath(base)
		norm_target = os.path.normpath(target2)
		try:
			common = os.path.commonpath([norm_base, norm_target])
		except ValueError:
			return ""
		if common != norm_base:
			return ""
		rel = os.path.relpath(norm_target, norm_base)
		rel=rel.replace('\\','/')
		return rel
	
	@staticmethod
	def BatchDownloadJoinNetPath(base,path):
		# path中的\会替换成/，path前的/绝对不能要（会有特殊逻辑），问号会没掉
		# base必须以/结尾！！！
		path2=HtmlAnalyse.getBatchDownloadValidName(path)
		if path2=="":
			return ""
		path2=path.replace('\\','/')
		if path2[0]=='/':
			path2=path2[1:]
		if path2[-1]=='/':
			path2=path2[:-1] #这个操作比较离谱，但我无法分清网站的主页是index.htm还是index.html，所以干脆不分了，拜拜
		return base+path2
	
	@staticmethod
	def BatchDownloadJoinLocalPath(localFolder,path):
		try:
			path2=unquote(path)
		except Exception:
			return ""
		# 绝对禁止..
		if '..' in path2:
			return ""
		forbidden_chars = set('?*\"<>|:')
		for ch in path2:
			if ch in forbidden_chars:
				return ""
		return os.path.join(localFolder,path2)

	@staticmethod
	def decodeWebContent(content):
		"""
		推断网页内容的编码，返回 (解码后的文本, 所用编码)。
		"""
		encoding=None
		text=None
		for enc in ['utf-8', 'gbk', 'gb2312']:
			try:
				text = content.decode(enc)
				encoding = enc
				break
			except UnicodeDecodeError:
				continue
		# 如果所有尝试都失败，使用 utf-8 并忽略错误
		if not encoding:
			encoding = 'utf-8'
			text = content.decode(encoding, errors='replace')
		return (text,encoding)

	@staticmethod
	def getNormPath(path):
		return os.path.normpath(path)
	
	@staticmethod
	def Page4399Replace(text):
		text1=text.replace('https://h.api.4399.com/h5mini-2.0/h5api-interface.php','/tool/substiH5WanApi.js')
		text2=re.sub(r"document.domain\s*=\s*['\"]4399.com['\"]\s*[,;]","",text1)
		return text2
	@staticmethod
	def Page7k7k17yyReplace(text):
		text2=re.sub(r"document.domain\s*=\s*['\"](7k7k|17yy).com['\"]\s*[,;]","",text)
		return text2
	