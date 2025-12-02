""" Download image according to given urls and automatically rename them in order. """
# -*- coding: utf-8 -*-
# author: Yabin Zheng
# Email: sczhengyabin@hotmail.com

from __future__ import print_function
from urllib.parse import unquote
from pathlib import Path
from hashlib import sha256

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
# default tests:
# test_bmp
# test_exr
# test_gif
# test_jpeg
# test_pbm
# test_pgm
# test_png
# test_ppm
# test_rast
# test_rgb
# test_tiff
# test_webp
# test_xbm

def test_html(h, f):
    if b"<html" in h:
        return "html"
    if b"<HTML" in h:
        return "html"
    if b"<!DOCTYPE " in h: # "<!DOCTYPE HTML" or "<!DOCTYPE html"
        return "html"
    if b"<!doctype html" in h:
        return "html"
    return None 

imghdr.tests.append(test_html)


def test_xml(h, f):
    if b"<xml" in h:
        return "xml"
    if b"<?xml " in h:
        return "xml"
    return None 

imghdr.tests.append(test_xml)


# imghdr checks for JFIF specifically, ignoring optional markers including metadata
def test_jpg(h, f):
    if h.startswith(b"\xff\xd8\xff"):
        return "jpg"
    return None 

imghdr.tests.append(test_jpg)


# https://stackoverflow.com/questions/8032642/how-can-i-obtain-the-image-size-using-a-standard-python-class-without-using-an
def test_jpeg2(h, f):
    # SOI APP2 + ICC_PROFILE
    if h[0:4] == '\xff\xd8\xff\xe2' and h[6:17] == b'ICC_PROFILE':
        return 'jpeg'
    # SOI APP14 + Adobe
    if h[0:4] == '\xff\xd8\xff\xee' and h[6:11] == b'Adobe':
        return 'jpeg'
    # SOI DQT
    if h[0:4] == '\xff\xd8\xff\xdb':
        return 'jpeg'
    return None 

imghdr.tests.append(test_jpeg2)


def download_image(image_url, dst_dir, file_name, timeout=20, proxy_type=None, proxy=None):
    proxies = None
    if proxy_type is not None:
        proxies = {
            "http": proxy_type + "://" + proxy,
            "https": proxy_type + "://" + proxy
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

            if len(response.content) < 1:
                break;

            hash_string = sha256(response.content).hexdigest()

            file_name = get_filename(file_name, response.content)
            file_path = os.path.join(dst_dir, file_name)
            base_file_path = file_path

            file_attempts = 0
            while file_attempts < 50:
                file_attempts += 1
                try:
                    # open for exclusive creation, failing if the file already exists
                    with open(file_path, "xb") as f:
                        f.write(response.content)
                    break
                except FileExistsError:
                    file_name = "{}_{}{}".format(Path(base_file_path).stem, file_attempts, Path(base_file_path).suffix)
                    file_path = os.path.join(dst_dir, file_name)
                except Exception as e:
                    file_name = "unknown" + Path(file_name).suffix
                    file_path = os.path.join(dst_dir, file_name)

        except Exception as e:
            if try_times < 3:
                continue
            if response:
                response.close()
            print("## Fail:  {}  {}".format(image_url, e.args))
        break

def get_filename(file_name, content):

    #TODO: use python-magic

    # just in case
    if "/" in file_name:
        file_name = split_string(file_name, "/", -1) 

    if file_name.endswith(".jpeg"):
        file_name = file_name.replace(".jpeg", ".jpg")

    file_type = imghdr.what('', content)

    if file_type == "jpeg":
        file_type = "jpg"

    if file_type is None:
        # os.remove(file_path)
        print("## Err: TYPE({})  {}".format(file_type, file_name))
        return file_name

    elif file_type in ["jpg", "jpeg", "png", "bmp", "webp", 'gif', 'xml', 'html']:
        if file_name.endswith("." + file_type):
            new_file_name = file_name
            print("## OK:  {}".format(new_file_name))
        else:
            file_name = Path(file_name).stem
            new_file_name = "{}.{}".format(file_name, file_type)
            print("## OK:  {} => {}".format(file_name, new_file_name))
        return new_file_name

    else:
        # os.remove(file_path)
        print("## Err: TYPE({})  {}".format(file_type, file_name))
        return file_name


def download_images(image_urls, dst_dir, file_prefix="img", concurrency=50, timeout=20, proxy_type=None, proxy=None):
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
        concurrent.futures.wait(future_list, timeout=90)

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
