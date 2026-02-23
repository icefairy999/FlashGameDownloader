import requests

print("请输入要下载的网址:")
url=input()
print("请输入包含它的上一个页面的网址:")
ref=input()
headers={
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 
	'Referer': ref
}
while True:
	print("请输入保存到的文件名:")
	fileName=input()
	if '..' in fileName:
		print("文件名禁止出现“..”")
		continue
	forbidden_chars = set('?*\"<>|:')
	for ch in fileName:
		if ch in forbidden_chars:
			print("文件名禁止出现 ? * \" < > | : ")
			continue
	break
try:
	response = requests.get(url, headers=headers)
	with open(fileName, "wb") as f:
		f.write(response.content)
	print("下载成功!")
except Exception as e:
	print(f"下载失败，{str(e)}")
while True:
	input()