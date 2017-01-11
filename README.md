# Google Image Downloader

## 1. Introdoction

Crawl and download images using Selenium + PhantomJS
Using python3 and PyQt4

## 2. Key features
+ Search Engine: Google, Bing, Baidu
+ Keywords input from keyboard, or input from line seperated keywords list file for batch process.
+ Download image using customizable number of threads.
+ Fully supported conditional search (eg. filetype:, site:).
+ Switch for Google safe mode.
+ Proxy configuration (socks, http).
+ CMD and GUI ways of using are provided.
+ Windows prebuilt executable release from [release page](https://github.com/sczhengyabin/Google-Image-Downloader/releases).

## 3. Solve dependencies under Linux

### 3.1 Setup Phantomjs
#### 3.1.1 Download Phantomjs
phantomjs prebuilt executable can be downloaded from [here](https://bitbucket.org/ariya/phantomjs/downloads)

#### 3.1.2 For Windows users:
Copy phantomjs.exe to ${project_directory}/bin/.

#### 3.1.3 For Linux users:
Add the path of phantomjs executable to $PATH, or simply copy it to /usr/local/bin/.

## 3.2 Install python packages
pip install -r requirements.txt
