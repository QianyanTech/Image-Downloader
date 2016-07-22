from __future__ import print_function
from future.moves.urllib.parse import unquote
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import time
import re


dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/51.0.2704.106 Safari/537.36"
)


def scrape_image_urls(keywords, number=None, face_only=False, safe_mode=False, proxy=None, proxy_type="http"):
    print("\nScraping From Google Image Search ...\n")
    print("Keywords:\t" + keywords)
    base_url = "https://www.google.com/search?tbm=isch"
    keywords_str = "&q=" + "+".join(keywords.split())

    query_url = base_url + keywords_str

    if number is None:
        print("Number:\t\tNo limit")
    else:
        print("Number:\t\t" + str(number))

    if face_only is True:
        query_url += "&tbs=itp:face"
        print("Face Only:\tYes")
    else:
        print("Face Only:\tNo")

    if safe_mode is True:
        query_url += "&safe=on"
        print("Safe Mode:\tOn")
    else:
        query_url += "&safe=off"
        print("Safe Mode:\tOff")

    print("Query URL:\t" + query_url)

    phantomjs_args = list()

    if proxy is not None:
        phantomjs_args = [
            "--proxy=" + proxy,
            "--proxy-type=" + proxy_type,
            ]
    driver = webdriver.PhantomJS(executable_path="phantomjs",
                                 service_args=phantomjs_args, desired_capabilities=dcap)
    driver.set_window_size(10000, 7500)
    driver.get(query_url)

    last_image_count = 0
    retry_times = 0

    time.sleep(3)

    while True:
        img_count = driver.find_elements_by_class_name("rg_l").__len__()
        if img_count > last_image_count:
            if retry_times > 5:
                break
            else:
                retry_times += 1
        else:
            last_image_count = img_count
            retry_times = 0
        time.sleep(0.5)

    image_elements = driver.find_elements_by_class_name("rg_l")

    image_urls = list()

    url_pattern = "imgurl=\S*&amp;imgrefurl"

    for image_element in image_elements:
        outer_html = image_element.get_attribute("outerHTML")
        re_group = re.search(url_pattern, outer_html)
        if re_group is not None:
            image_url = unquote(re_group.group()[7:-14])
            image_urls.append(image_url)

    if number is not None and number > image_urls.__len__():
        number = image_urls.__len__()

    print("\nTotal {0} images scraped, {1} will be used.\n".format(image_urls.__len__(), number))

    return image_urls[0:number]
