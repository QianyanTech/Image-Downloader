# -*- coding: utf-8 -*-
from __future__ import print_function
from urllib.parse import unquote, quote
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import re

""" Scrape image urls of keywords from Google Image Search """

__author__ = "Yabin Zheng ( sczhengyabin@hotmail.com )"


dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100"
)


def crawl_image_urls(keywords, engine="Google", max_number=0,
                     face_only=False, safe_mode=False, proxy=None, proxy_type="http"):
    """
    Scrape image urls of keywords from Google Image Search
    :param keywords: keywords you want to search
    :param max_number: limit the max number of image urls the function output, equal or less than 0 for unlimited
    :param face_only: image type set to face only, provided by Google
    :param safe_mode: switch for safe mode of Google Search
    :param proxy: proxy address, example: socks5 192.168.0.91:1080
    :param proxy_type: socks5, http
    :return: list of scraped image urls
    """

    print("\nScraping From Google Image Search ...\n")
    print("Keywords:  " + keywords)
    base_url = "https://www.google.com/search?tbm=isch"
    keywords_str = "&q=" + quote(keywords)

    query_url = base_url + keywords_str

    if max_number <= 0:
        print("Number:  No limit")
    else:
        print("Number:  {}".format(max_number))

    if face_only is True:
        query_url += "&tbs=itp:face"
        print("Face Only:  Yes")
    else:
        print("Face Only:  No")

    if safe_mode is True:
        query_url += "&safe=on"
        print("Safe Mode:  On")
    else:
        query_url += "&safe=off"
        print("Safe Mode:  Off")

    print("Query URL:  " + query_url)

    phantomjs_args = []
    if proxy is not None:
        phantomjs_args = [
            "--proxy=" + proxy,
            "--proxy-type=" + proxy_type,
            ]
    driver = webdriver.PhantomJS(executable_path="phantomjs",
                                 service_args=phantomjs_args, desired_capabilities=dcap)
    driver.set_window_size(10000, 7500)
    driver.get(query_url)

    # last_image_count = 0
    # retry_times = 0

    # while True:
    #     img_count = driver.find_elements_by_class_name("rg_l").__len__()
    #     print("count = ", img_count)
    #     if img_count > last_image_count:
    #         last_image_count = img_count
    #         retry_times = 0
    #     else:
    #         if retry_times > 5:
    #             break
    #         else:
    #             retry_times += 1
    #     time.sleep(0.5)

    image_elements = driver.find_elements_by_class_name("rg_l")

    image_urls = list()

    url_pattern = "imgurl=\S*&amp;imgrefurl"

    for image_element in image_elements:
        outer_html = image_element.get_attribute("outerHTML")
        re_group = re.search(url_pattern, outer_html)
        if re_group is not None:
            image_url = unquote(re_group.group()[7:-14])
            image_urls.append(image_url)

    if max_number > image_urls.__len__():
        output_num = image_urls.__len__()
    else:
        output_num = max_number

    print("\n== {0} out of {1} crawled images urls will be used.\n".format(output_num, len(image_urls)))

    return image_urls[0:output_num]
