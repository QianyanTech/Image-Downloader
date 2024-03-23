# Image Downloader

[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu)

## [中文说明](https://github.com/QianyanTech/Image-Downloader/blob/master/README_zh.md)

## 1. Introdoction

Crawl and download images using Selenium or API
Using python3 and PyQt5

## 2. Key features

+ Supported Search Engine: Google, Bing, Baidu
+ Keywords input from keyboard, or input from line seperated keywords list file for batch process.
+ Download image using customizable number of threads.
+ Fully supported conditional search (eg. filetype:, site:).
+ Switch for Google safe mode.
+ Proxy configuration (socks, http).
+ CMD and GUI ways of using are provided.

## 3. Usage

### 3.1 GUI

Run `image_downloader_gui.py` script to yank GUI:
```bash
python image_downloader_gui.py
```

![GUI](/GUI.png)

### 3.2 CMD

```bash
usage: image_downloader.py [-h] [--engine {Google,Bing,Baidu}]
                           [--driver {chrome_headless,chrome,api}]
                           [--max-number MAX_NUMBER]
                           [--num-threads NUM_THREADS] [--timeout TIMEOUT]
                           [--output OUTPUT] [--safe-mode] [--face-only]
                           [--proxy_http PROXY_HTTP]
                           [--proxy_socks5 PROXY_SOCKS5]
                           keywords
```

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=QianyanTech/Image-Downloader&type=Date)](https://star-history.com/#QianyanTech/Image-Downloader&Date)

## License

+ MIT License
+ 996ICU License
