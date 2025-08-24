# FlashGameDownloader

一个能下载4399、7k7k、17yy的flash小游戏的工具。这是源码。你需要找一个flash独立播放器放到tool/FlashPlayer.exe处，来运行下载的swf文件。

代码分为几个类：

**CONST**：工具类，存放一些常数

**PHPTool**：工具类，用于调用网站的php

**HtmlAnalyse**：工具类，用于分析html内容，找到相应的swf路径

**GameDownloader**：实例类，用于下载工作。
- 变量setSwfpathVariable的设置是因为主界面有个“找到的SWF地址是：xxxxxx”信息框，我不得不把这个框的变量传递给它，方便即时修改
- 主swf文件的寻找和下载：用setInfo告诉它：网络地址、要创建的文件名后缀、网站类型'4399''7k7k''17yy'，接着就能用downloadSWF()下载了。
- 关联文件的下载：用setSWFNetPath告诉它主swf文件的地址；用setHeader3再告诉它一次主swf文件的地址，填入请求头的Referer中，就可以使用relateDownload(XXX)下载了。

**Application**：用于界面控件的显示和事件。

**RelatedDownloader**：用于界面控件的显示和事件。

**EditNetPathDialog**：用于界面控件的显示和事件。

