# -*- coding: utf-8 -*-
# author: Yabin Zheng
# Email: sczhengyabin@hotmail.com

from __future__ import print_function
from urllib.parse import unquote, quote
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import re
import time
import sys
import os
import json
import requests
import ujson

""" Scrape image urls of keywords from Google Image Search """

__author__ = "Yabin Zheng ( sczhengyabin@hotmail.com )"

if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

if sys.platform.startswith("win"):
    phantomjs_path = os.path.join(bundle_dir + "/bin/phantomjs.exe")
else:
    phantomjs_path = "phantomjs"

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100"
)


def my_print(msg, quiet=False):
    if not quiet:
        print(msg)


def google_gen_query_url(keywords, face_only=False, safe_mode=False):
    base_url = "https://www.google.com/search?tbm=isch&hl=en"
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
    # time.sleep(10)
    try:
        show_more = driver.find_element_by_id("smb")
        show_more.click()
        time.sleep(3)
    except Exception as e:
        pass
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
    image_urls = list()

    time.sleep(10)
    img_count = 0

    while True:
        image_elements = driver.find_elements_by_class_name("iusc")
        if len(image_elements) > img_count:
            img_count = len(image_elements)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        else:
            smb = driver.find_elements_by_class_name("btn_seemore")
            if len(smb) > 0 and smb[0].is_displayed():
                smb[0].click()
            else:
                break
        time.sleep(3)
    for image_element in image_elements:
        m_json_str = image_element.get_attribute("m")
        m_json = json.loads(m_json_str)
        image_urls.append(m_json["murl"])
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


def baidu_get_image_url_using_api(keywords, max_number=10000, face_only=False,
                                  proxy=None, proxy_type=None):
    base_url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592"\
               "&fp=result&ie=utf-8&oe=utf-8&st=-1"
    keywords_str = "&word={}&queryWord={}".format(quote(keywords), quote(keywords))
    query_url = base_url + keywords_str
    query_url += "&face={}".format(1 if face_only else 0)

    init_url = query_url + "&pn=0&rn=30"

    init_json = json.loads(requests.get(init_url).text, encoding='utf-8')
    total_num = init_json['listNum']

    target_num = min(max_number, total_num)
    print(total_num, target_num)

    crawled_urls = list()
    batch = 30
    for i in range(0, int((total_num + batch - 1) / batch)):
        url = query_url + "&pn={}&rn={}".format(i * batch, batch)
        if proxy and proxy_type:
            proxies = {"http": "{}://{}".format(proxy_type, proxy),
                       "https": "{}://{}".format(proxy_type, proxy)}
            response = requests.get(url, proxies=proxies)
        else:
            response = requests.get(url)
        response.encoding = 'utf-8'
        try:
            res_json = json.loads(response.text, encoding='utf-8')
            image_urls = [data['replaceUrl'][1]['ObjURL'] for data in res_json['data']
                          if 'replaceUrl' in data.keys() and len(data['replaceUrl']) == 2]
            crawled_urls += image_urls
            if len(crawled_urls) >= target_num:
                break
        except Exception as e:
            # print(e)
            pass

    return crawled_urls[:target_num]


def crawl_image_urls(keywords, engine="Google", max_number=10000,
                     face_only=False, safe_mode=False, proxy=None, proxy_type="http", quiet=False):
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

    my_print("\nScraping From {0} Image Search ...\n".format(engine), quiet)
    my_print("Keywords:  " + keywords, quiet)
    if max_number <= 0:
        my_print("Number:  No limit", quiet)
    else:
        my_print("Number:  {}".format(max_number), quiet)
    my_print("Face Only:  {}".format(str(face_only)), quiet)
    my_print("Safe Mode:  {}".format(str(safe_mode)), quiet)

    if engine == "Google":
        query_url = google_gen_query_url(keywords, face_only, safe_mode)
    elif engine == "Bing":
        query_url = bing_gen_query_url(keywords, face_only, safe_mode)
    elif engine == "Baidu":
        query_url = baidu_gen_query_url(keywords, face_only, safe_mode)
    else:
        return

    my_print("Query URL:  " + query_url, quiet)

    phantomjs_args = []
    if proxy is not None:
        phantomjs_args += [
            "--proxy=" + proxy,
            "--proxy-type=" + proxy_type,
            ]
    driver = webdriver.PhantomJS(executable_path=phantomjs_path,
                                 service_args=phantomjs_args, desired_capabilities=dcap)

    if engine == "Google":
        driver.set_window_size(10000, 7500)
        driver.get(query_url)
        image_urls = google_image_url_from_webpage(driver)
    elif engine == "Bing":
        driver.set_window_size(1920, 1080)
        driver.get(query_url)
        image_urls = bing_image_url_from_webpage(driver)
    else:   # Baidu
        # driver.set_window_size(10000, 7500)
        # driver.get(query_url)
        # image_urls = baidu_image_url_from_webpage(driver)
        image_urls = baidu_get_image_url_using_api(keywords, max_number=max_number, face_only=face_only,
                                                   proxy=proxy, proxy_type=proxy_type)

    driver.close()

    if max_number > len(image_urls):
        output_num = len(image_urls)
    else:
        output_num = max_number

    my_print("\n== {0} out of {1} crawled images urls will be used.\n".format(output_num, len(image_urls)), quiet)

    return image_urls[0:output_num]
