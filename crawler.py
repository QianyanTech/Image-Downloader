# -*- coding: utf-8 -*-
from __future__ import print_function
from urllib.parse import unquote, quote
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import re
import time

""" Scrape image urls of keywords from Google Image Search """

__author__ = "Yabin Zheng ( sczhengyabin@hotmail.com )"


dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100"
)


def google_gen_query_url(keywords, face_only=False, safe_mode=False):
    base_url = "https://www.google.com/search?tbm=isch"
    keywords_str = "&q=" + quote(keywords)
    query_url = base_url + keywords_str
    if face_only is True:
        query_url += "&tbs=itp:face"
    if safe_mode is True:
        query_url += "&safe=on"
    else:
        query_url += "&safe=off"
    return query_url


def google_image_url_from_webpage(driver):
    time.sleep(10)
    image_elements = driver.find_elements_by_class_name("rg_l")
    image_urls = list()
    url_pattern = "imgurl=\S*&amp;imgrefurl"

    for image_element in image_elements:
        outer_html = image_element.get_attribute("outerHTML")
        re_group = re.search(url_pattern, outer_html)
        if re_group is not None:
            image_url = unquote(re_group.group()[7:-14])
            image_urls.append(image_url)
    return image_urls


def bing_gen_query_url(keywords, face_only=False, safe_mode=False):
    base_url = "https://www.bing.com/images/search?"
    keywords_str = "&q=" + quote(keywords)
    query_url = base_url + keywords_str
    if face_only is True:
        query_url += "&qft=+filterui:face-face"
    return query_url


def bing_image_url_from_webpage(driver):
    time.sleep(10)
    parents = driver.find_elements_by_class_name("dg_u")
    image_elements = []
    for parent in parents:
        image_elements.append(parent.find_element_by_tag_name("a"))
    image_urls = list()
    url_pattern = 'imgurl:&quot;\S*&quot;,tid'

    for image_element in image_elements:
        outer_html = image_element.get_attribute("outerHTML")
        re_group = re.search(url_pattern, outer_html)
        if re_group is not None:
            image_url = unquote(re_group.group()[13:-10])
            image_urls.append(image_url)
    return image_urls


def baidu_gen_query_url(keywords, face_only=False, safe_mode=False):
    base_url = "https://image.baidu.com/search/index?tn=baiduimage"
    keywords_str = "&word=" + quote(keywords)
    query_url = base_url + keywords_str
    if face_only is True:
        query_url += "&face=1"
    return query_url


def baidu_image_url_from_webpage(driver):
    time.sleep(10)
    image_elements = driver.find_elements_by_class_name("imgitem")
    image_urls = list()

    for image_element in image_elements:
        image_url = image_element.get_attribute("data-objurl")
        image_urls.append(image_url)
    return image_urls


def crawl_image_urls(keywords, engine="Google", max_number=0,
                     face_only=False, safe_mode=False, proxy=None, proxy_type="http"):
    """
    Scrape image urls of keywords from Google Image Search
    :param keywords: keywords you want to search
    :param engine: search engine used to search images
    :param max_number: limit the max number of image urls the function output, equal or less than 0 for unlimited
    :param face_only: image type set to face only, provided by Google
    :param safe_mode: switch for safe mode of Google Search
    :param proxy: proxy address, example: socks5 192.168.0.91:1080
    :param proxy_type: socks5, http
    :return: list of scraped image urls
    """

    print("\nScraping From {0} Image Search ...\n".format(engine))
    print("Keywords:  " + keywords)
    if max_number <= 0:
        print("Number:  No limit")
    else:
        print("Number:  {}".format(max_number))
    print("Face Only:  {}".format(str(face_only)))
    print("Safe Mode:  {}".format(str(safe_mode)))

    if engine == "Google":
        query_url = google_gen_query_url(keywords, face_only, safe_mode)
    elif engine == "Bing":
        query_url = bing_gen_query_url(keywords, face_only, safe_mode)
    elif engine == "Baidu":
        query_url = baidu_gen_query_url(keywords, face_only, safe_mode)
    else:
        return

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

    if engine == "Google":
        image_urls = google_image_url_from_webpage(driver)
    elif engine == "Bing":
        image_urls = bing_image_url_from_webpage(driver)
    elif engine == "Baidu":
        image_urls = baidu_image_url_from_webpage(driver)

    driver.close()

    if max_number > len(image_urls):
        output_num = len(image_urls)
    else:
        output_num = max_number

    print("\n== {0} out of {1} crawled images urls will be used.\n".format(output_num, len(image_urls)))

    return image_urls[0:output_num]
