# Image Downloader

## 1. 简介

+ 从图片搜索引擎，爬取关键字搜索的原图URL并下载
+ 开发语言python，采用Requests、Selenium、Phantomjs等库进行开发

## 2. 功能
+ 支持的搜索引擎: Google, 必应, 百度
+ 提供GUI及CMD版本
+ GUI版本支持关键词键入，以及通过关键词列表文件（行分隔,**使用UTF-8编码**）输入进行批处理爬图下载
+ 可配置线程数进行并发下载，提高下载速度
+ 支持搜索引擎的条件查询（如 :site）
+ 支持Google的安全模式开启和关闭
+ 支持socks5和http代理的配置，方便科学上网用户
+ **提供预编译的windows单文件可执行exe下载, 推荐非开发者用户使用。[点此下载](https://github.com/sczhengyabin/Google-Image-Downloader/releases)**

## 3. 解决依赖
### 3.1 Windows环境
#### 3.1.1 下载并安装python3.5
+ [下载地址](https://www.python.org/ftp/python/3.5.3/python-3.5.3.exe)
+ 安装时请注意勾选"add to PATH"
#### 3.1.2 下载并安装PyQt5
+ [下载地址](https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.6/PyQt5-5.6-gpl-Py3.5-Qt5.6.0-x32-2.exe/download)
#### 3.1.3 下载phantomjs并配置
+ [下载地址](https://bitbucket.org/ariya/phantomjs/downloads)
+ 选择最新的windows版本下载即可
+ 下载完成后将phantomjs.exe拷贝到 "本项目文件夹/bin/"
#### 3.1.4 安装相关python库
```
pip3.exe install -r requirements.txt
```
#### 3.1.5 [可选] 打包成单个可执行文件
确保 3.1.3 步骤完成后，CMD进到项目文件夹，执行如下命令：
```
pip3.exe install pyinstaller
pyinstaller image_downloader_gui.spec
```
命令完成后，exe文件在 ./dist 文件夹中
### 3.2 Linux环境（debian系列）
#### 3.2.1 安装依赖库
```
apt-get install python3-pip python3-pyqt5 pyqt5-dev-tools
```
#### 3.2.2 下载Phantomjs并配置
+ [x86 PC用户下载地址](https://bitbucket.org/ariya/phantomjs/downloads) （官方）
+ [树莓派用户下载地址](https://github.com/fg2it/phantomjs-on-raspberry/releases)（无官方版本，第三方通过源码编译）

**[警告]: 通过apt-get安装的phantomjs为非完整版，无法在本项目中使用.**

下载完成后，将phantomjs文件路径添加至PATH环境变量，或者将其拷贝到/usr/local/bin文件夹。
## 4. 如何使用
### 4.1 图形界面
![](http://p1.bqimg.com/567571/2d72755a4d3fc319.png)
### 4.2 命令行
```
usage: image_downloader.py [-h] [--engine {Google,Bing,Baidu}]
                           [--max-number MAX_NUMBER]
                           [--num-threads NUM_THREADS] [--timeout TIMEOUT]
                           [--output OUTPUT] [--safe-mode] [--face-only]
                           [--proxy_http PROXY_HTTP]
                           [--proxy_socks5 PROXY_SOCKS5]
                           keywords
```
