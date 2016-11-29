# -*- coding: utf-8 -*-
from __future__ import print_function
import concurrent.futures
import requests
import shutil
import imghdr
import os

""" Download image according to given urls and automatically rename them in order. """

__author__ = "Yabin Zheng ( sczhengyabin@hotmail.com )"


headers = {
    'Connection': 'close',
    'User-Agent': 'Chrome/54.0.2840.100'
}


def download_image(image_url, dst_dir, file_name, proxy_type=None, proxy=None, timeout=20):
    proxies = None
    if proxy_type is not None:
        proxies = {
            "http": proxy_type + "://" + proxy,
            "https": proxy_type + "://" + proxy
        }

    r = None
    file_path = os.path.join(dst_dir, file_name)
    try:
        r = requests.get(image_url, headers=headers, timeout=timeout, proxies=proxies)
        with open(file_path, 'wb') as f:
            f.write(r.content)
        r.close()
        file_type = imghdr.what(file_path)
        if file_type is not None:
            new_file_name = "{0}.{1}".format(file_name, file_type)
            new_file_path = os.path.join(dst_dir, new_file_name)
            shutil.move(file_path, new_file_path)
            print("## OK:  {0}  {1}".format(new_file_name, image_url))
        else:
            os.remove(file_path)
            print("## Err:  {0}".format(image_url))
    except Exception as e:
        if r:
            r.close()
        print("## Fail:  ", image_url, e.args)


def download_images(image_urls, dst_dir, file_prefix="img", concurrency=50, proxy_type=None, proxy=None, timeout=20):
    """
    Download image according to given urls and automatically rename them in order.
    :param image_urls: list of image urls
    :param dst_dir: output the downloaded images to dst_dir
    :param file_prefix: if set to "img", files will be in format "img_xxx.jpg"
    :param concurrency: number of requests process simultaneously
    :return: none
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = list()
        count = 0
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for image_url in image_urls:
            file_name = file_prefix + "_" + "%03d" % count
            futures.append(executor.submit(
                download_image, image_url, dst_dir, file_name, proxy_type, proxy, timeout))
            count += 1
