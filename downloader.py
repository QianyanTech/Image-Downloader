""" Download image according to given urls and automatically rename them in order. """
# -*- coding: utf-8 -*-
# author: Yabin Zheng
# Email: sczhengyabin@hotmail.com

from __future__ import print_function
from urllib.parse import unquote

import shutil
import imghdr
import os
import concurrent.futures
import requests
import socket

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, sdch",
    # 'Connection': 'close',
}

# additional checks for imghdr.what()

def test_html(h, f):
    if b"<html" in h:
        return "html"
    if b"<HTML" in h:
        return "html"
    if b"<!DOCTYPE " in h: # "<!DOCTYPE HTML" or "<!DOCTYPE html"
        return "html"
    if b"<!doctype html" in h:
        return "html"


imghdr.tests.append(test_html)


def test_xml(h, f):
    if b"<xml" in h:
        return "xml"
    if b"<?xml " in h:
        return "xml"


imghdr.tests.append(test_xml)

# imghdr checks for JFIF specifically, ignoring optional markers including metadata
def test_jpg(h, f):
    if (h[:3] == "\xff\xd8\xff"):
        return "jpg"


imghdr.tests.append(test_jpg)


def download_image(
    image_url, dst_dir, file_name, timeout=20, proxy_type=None, proxy=None
):
    proxies = None
    if proxy_type is not None:
        proxies = {
            "http": proxy_type + "://" + proxy,
            "https": proxy_type + "://" + proxy,
        }

    file_name = unquote(file_name)
    response = None
    file_path = os.path.join(dst_dir, file_name)
    try_times = 0
    while True:
        try:
            try_times += 1
            # https://github.com/pablobots/Image-Downloader/commit/5bdbe076589459b9d0c41a563b92993cac1a892e
            image_url = image_url.split('&amp;')[0] 
            response = requests.get(
                image_url, headers=headers, timeout=timeout, proxies=proxies
            )
            
            # TODO: handle 429 Too Many Requests, set a timer to slow down request frequency
            # handle 401 Unauthorized (don't even save the content)
            # handle 404 not found (don't even save the content)
            # handle 403 Forbidden (don't even save the content)
            
            if response.status_code in [ 404,403,401 ]:
                print("## Err: STATUS CODE({})  {}".format(response.status_code, image_url))
                return False
            
            with open(file_path, "wb") as f:
                f.write(response.content)
            response.close()

            file_type = imghdr.what(file_path)

            if file_name.endswith(".jpeg"):
                file_name = file_name.replace(".jpeg", ".jpg")

            if file_type == "jpeg":
                file_type = "jpg"

            if file_type is None:
                # os.remove(file_path)
                print("## Err: TYPE({})  {}".format(file_type, file_name))
                return False
            elif file_type == "html" or file_type == "xml":
                os.remove(file_path)
                print("## Err: TYPE({})  {}".format(file_type, image_url))
                return False
            elif file_type in ["jpg", "jpeg", "png", "bmp", "webp", 'gif']:
                if len(file_name) >= 200:
                    print("Truncating:  {}".format(file_name))
                    file_name = file_name[:200]

                if file_name.endswith("." + file_type):
                    new_file_name = file_name
                else:
                    new_file_name = "{}.{}".format(file_name, file_type)

                new_file_path = os.path.join(dst_dir, new_file_name)
                shutil.move(file_path, new_file_path)
                print("## OK:  {}  {}".format(new_file_name, image_url))
                return True
            else:
                # os.remove(file_path)
                print("## Err: TYPE({})  {}".format(file_type, image_url))
                return False
            break

        except Exception as e:
            if try_times < 3:
                file_name = file_name + "a"
                continue
            if response:
                response.close()
            print("## Fail:  {}  {}".format(image_url, e.args))
            return False
            break


def download_images(
    image_urls,
    dst_dir,
    file_prefix="img",
    concurrency=50,
    timeout=20,
    proxy_type=None,
    proxy=None,
):
    """
    Download image according to given urls and automatically rename them in order.
    :param timeout:
    :param proxy:
    :param proxy_type:
    :param image_urls: list of image urls
    :param dst_dir: output the downloaded images to dst_dir
    :param file_prefix: if set to "img", files will be in format "img_xxx.jpg"
    :param concurrency: number of requests process simultaneously
    :return: the number of successful downloads
    """

    socket.setdefaulttimeout(timeout)

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        future_list = list()
        count = 0
        success_downloads = 0

        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for image_url in image_urls:
            # file_name = file_prefix + "_" + "%04d" % count
            print("## URL :  {}".format(image_url))
            file_name = image_url
            file_name = split_string(file_name, "?", 0)
            file_name = split_string(file_name, "&amp;", 0)
            file_name = split_string(file_name, "/", -1)
            print("## FILE:  {}".format(file_name))
            future_list.append(
                executor.submit(
                    download_image,
                    image_url,
                    dst_dir,
                    file_name,
                    timeout,
                    proxy_type,
                    proxy,
                )
            )
            count += 1
        concurrent.futures.wait(future_list, timeout=180)

        # Count the number of successful downloads
        for future in future_list:
            if future.result():
                success_downloads += 1

    return success_downloads


def split_string(str, delimiter, index):
    s = str
    while delimiter in s:
        s, _, t = s.partition(delimiter)
        if index == 0:
            break
        if t == "":
            break
        index = index - 1
        s = t

    if s == "":
        s = str

    return s
