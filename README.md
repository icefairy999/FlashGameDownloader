# FlashGameDownloader

一个能下载4399、7k7k、17yy的flash小游戏的工具。这是源码。你需要找一个flash独立播放器放到tool/FlashPlayer.exe处，来运行下载的swf文件。

代码分为几个类：

**CONST**：工具类，存放一些常数

**PHPTool**：工具类，用于调用网站的php

**HtmlAnalyse**：工具类，用于分析html内容，找到相应的swf路径

**GameDownloader**：实例类，用于下载工作。它做两件事：寻找并下载主swf文件、下载关联swf文件
- 变量setSwfpathVariable：主界面有个“找到的SWF地址是：xxxxxx”信息框，我不得不把这个框的变量传递给它，方便它修改
- setInfo(url,appendix,site)：设置网络地址、文件名后缀、网站类型（'4399','7k7k','17yy'）（必须一次都设置好）
- downloadSWF()：寻找下载swf文件，返回文件名。需要先setInfo
- setSWFNetPath(SWFNetPath)：设置主swf文件的网络路径，用于关联文件下载时与相对路径的拼接
- setHeader3：设置请求头的Referer。Referer不对时，网站会重定向
- relateDownload(path)：通过相对路径下载关联文件。需要先setSWFNetPath和setHeader3

**Application**：用于界面控件的显示和事件。

**RelatedDownloader**：用于界面控件的显示和事件。

**EditNetPathDialog**：用于界面控件的显示和事件。

