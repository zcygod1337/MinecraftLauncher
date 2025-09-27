### 严禁在Readme吵架

------
由于本项目团队有人过于傻逼，不会去看release，我就给本程序新版（以后也会是这样）的命令写一下

'''
main -run {version} --username {name}
'''
以{name}为用户名，启动{version}的版本。（前提是要有，没有主程序就自动爆炸）

{目前只支持1.12.2的因为1.13mojang把minecraft大重写，我的硬编码无法识别，预计在1.0.3中修复这个问题，并添加JRE17支持}

举例： main -run 1.8.9 --username zcygod

以zcygod为名字启动1.8.9版本

'''
main -download {version}
'''

下载（如果下载过就是重新下载）版本为{version}的版本

举例:

main -download 1.9

下载1.9版本的mc(from mojang API)


main -help

我不用解释了吧

------


# MinecraftLauncher
> This is a Minecraft Launcher by C++,Python（python即将消失),java

Updating Log

------
> version 1.0.0

[+]这个项目的第一个release版本，只是一个简单的命令行启动工具，安装包里塞了一整个Minecraft和java

> version 1.0.1

[+]本项目的第二个release版本（由于zcygod很脑残不会添加多个release，删除了1.0.0的release）

使用了github作为源从云端下载 Minecraft和java，本质上还是命令行

> version 1.0.2

[+]mojang 官方API当做下载源

[+]json解析

> version 1.0.3 (Future)

[-]python的爬虫爬取文件

[+]使用Cpp原生的WindowsAPI作为下载方式。
~~[+]使用Cpp原生的WindowsAPI作为下载方式~~暂时无法实现，WindowsAPI没有解析文件

[+]JavaGUI

[+]添加下载过的版本记录在.\version.txt的功能

[+]识别系统已下载的Java进行启动而不是在.7z中添加文件而变得更臃肿

-------
就这样
本程序基于GPL-V3.0

-----
