import scraper
import downloader


keywords_list = [
    "face with eyes closed",
    "frontal face",
]

dst_dir = "../images/"

for keywords in keywords_list:
    img_dir = dst_dir + "/" + keywords

    scraped_urls = scraper.scrape_image_urls(keywords, 100, face_only=True, safe_mode=True,
                                             proxy="192.168.205.1:1080", proxy_type="socks5")

    downloader.download_images(scraped_urls, img_dir, concurrency=50)
