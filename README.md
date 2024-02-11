
I have moved to using [https://github.com/hellock/icrawler] icrawler.  It has some bugs but the code seems more mature.

Image-Downloader executes a browser with JavaScript, using chromedriver or similar, which seems to be the 2024 way to understand the web.  But the code is more difficult to re-use.

icrawler uses BeautifulSoup to parse the text response, which still works.  It is a text-based library, but easy to subclass and modify just the relevant parts.
