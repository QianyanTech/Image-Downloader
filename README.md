# Image Downloader

### [中文版本点此](https://github.com/sczhengyabin/Image-Downloader/blob/master/README_zh.md)

## 1. Introdoction

Crawl and download images using Selenium + PhantomJS
Using python3 and PyQt5

## 2. Key features
+ Supported Search Engine: Google, Bing, Baidu
+ Keywords input from keyboard, or input from line seperated keywords list file for batch process.
+ Download image using customizable number of threads.
+ Fully supported conditional search (eg. filetype:, site:).
+ Switch for Google safe mode.
+ Proxy configuration (socks, http).
+ CMD and GUI ways of using are provided.
+ **Windows prebuilt executable release from [release page](https://github.com/sczhengyabin/Google-Image-Downloader/releases).**

## 3. Solve dependencies
### 3.1 Windows
#### 3.1.1 Download and install Python3.5
Download Latest version of Python3.5 installer from [here](https://www.python.org/ftp/python/3.5.3/python-3.5.3.exe)
#### 3.1.2 Download and install PyQt5
Download latest version of PyQt5 install from [here](https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.6/PyQt5-5.6-gpl-Py3.5-Qt5.6.0-x32-2.exe/download)
#### 3.1.3 Download and setup phantomjs
Official phantomjs prebuilt executable can be downloaded from [here](https://bitbucket.org/ariya/phantomjs/downloads)

Then copy phantomjs.exe to ${project_directory}/bin/
#### 3.1.4 Install python packages
```
pip3.exe install -r requirements.txt
```
#### 3.1.5 Build one-file .exe bundle
```
pip3.exe install pyinstaller
mkdir bin
```
copy the downloaded phantomjs.exe from 3.1.3 into ./bin folder.
```
pyinstaller image_downloader_gui.spec
```
The bundle will be built in ./dist folder.
### 3.2 Linux
#### 3.2.1 Install dependent packages
```
apt-get install python3-pip python3-pyqt5 pyqt5-dev-tools
```
#### 3.2.2 Download and setup phantomjs
+ **For PC users**

Official phantomjs prebuilt executable can be downloaded from [here](https://bitbucket.org/ariya/phantomjs/downloads)  
**[Warning]: PhantomJS installed from ubuntu source by apt-get do not work in this project.**
+ **For Raspberry Pi Users**

Unofficial phantomjs prebuilt executable or .deb for raspberry pi can be downloaded from [here](https://github.com/fg2it/phantomjs-on-raspberry/releases)

Add the path of phantomjs executable to $PATH, or simply copy it to /usr/local/bin/.
### 3.2.3 Install python packages
```
pip3 install -r requirements.txt
```
## 4. Usage
### 4.1 GUI
![](http://p1.bqimg.com/567571/2d72755a4d3fc319.png)
### 4.2 CMD
```
usage: image_downloader.py [-h] [--engine {Google,Bing,Baidu}]
                           [--max-number MAX_NUMBER]
                           [--num-threads NUM_THREADS] [--timeout TIMEOUT]
                           [--output OUTPUT] [--safe-mode] [--face-only]
                           [--proxy_http PROXY_HTTP]
                           [--proxy_socks5 PROXY_SOCKS5]
                           keywords
```
