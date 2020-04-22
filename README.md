# Image Downloader

[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu)

## [中文说明](https://github.com/sczhengyabin/Image-Downloader/blob/master/README_zh.md)

## 1. Introdoction

Crawl and download images using Selenium
Using python3 and PyQt5

## 2. Key features

+ Supported Search Engine: Google, Bing, Baidu
+ Keywords input from keyboard, or input from line seperated keywords list file for batch process.
+ Download image using customizable number of threads.
+ Fully supported conditional search (eg. filetype:, site:).
+ Switch for Google safe mode.
+ Proxy configuration (socks, http).
+ CMD and GUI ways of using are provided.

## 3. Install

### 3.1 Download and install Python3.5+

+ Download Latest version of Python3.5 installer from [here](https://www.python.org/downloads/)

### 3.2 Download and setup chromedriver [recommend]

+ Require Google Chrome Browser or Chromium Browser installed.
+ Download the corresponding version of chromedriver from [here](https://chromedriver.chromium.org/downloads)
+ Copy `chromedriver` binary to ${project_directory}/bin/ or add it to PATH.

### 3.3 Download and setup phantomjs [deprecated]

+ Official phantomjs prebuilt executable can be downloaded from [here](https://bitbucket.org/ariya/phantomjs/downloads)
+ Copy `phantomjs` to ${project_directory}/bin/ or add it to PATH.

### 3.4 Install python packages

```bash
pip3 install -r requirements.txt
```

## 4. Usage

### 4.1 GUI

Run `image_downloader_gui.py` script to yank GUI:
```bash
python image_downloader_gui.py
```

![GUI](/GUI.png)

### 4.2 CMD

```bash
usage: image_downloader.py [-h] [--engine {Google,Bing,Baidu}]
                           [--driver {chrome_headless,chrome,phantomjs}]
                           [--max-number MAX_NUMBER]
                           [--num-threads NUM_THREADS] [--timeout TIMEOUT]
                           [--output OUTPUT] [--safe-mode] [--face-only]
                           [--proxy_http PROXY_HTTP]
                           [--proxy_socks5 PROXY_SOCKS5]
                           keywords
```

## License

+ MIT License
+ 996ICU License
