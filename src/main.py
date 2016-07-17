import scraper
import downloader
import global_variables as gv


keywords_list = [
    "face with eyes closed",
    "frontal face",
]

dst_dir = "/images/eye/"

for keywords in keywords_list:
    img_dir = gv.root_dir + dst_dir + keywords

    scraped_urls = scraper.scrape_image_urls(keywords, 100, face_only=True, safe_mode=True,
                                             proxy="192.168.0.92:1080", proxy_type="socks5")

    downloader.download_images(scraped_urls, img_dir, concurrency=50)
