from __future__ import print_function
import concurrent.futures
import requests
import shutil
import imghdr
import os


headers = {
    'Connection': 'close',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
}


def download_image(image_url, dst_dir, file_name):
    r = None
    file_path = os.path.join(dst_dir, file_name)
    try:
        r = requests.get(image_url, headers=headers, timeout=30)
        with open(file_path, 'wb') as f:
            f.write(r.content)
        r.close()
        file_type = imghdr.what(file_path)
        if file_type is not None:
            new_file_name = "{0}.{1}".format(file_name, file_type)
            new_file_path = os.path.join(dst_dir, new_file_name)
            shutil.move(file_path, new_file_path)
            print("Download succeeded:\t{0}\t{1}".format(new_file_name, image_url))
        else:
            os.remove(file_path)
            print("Error format:\t\t{0}\t\t\t{1}".format(file_name, image_url))
    except Exception as e:
        if r:
            r.close()
        print("Download failed:\t" + file_name + "\t\t\t" + image_url)


def download_images(image_urls, dst_dir, file_prefix="img", concurrency=50):
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = list()
        count = 0
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for image_url in image_urls:
            file_name = file_prefix + "_" + "%03d" % count
            futures.append(executor.submit(
                download_image, image_url, dst_dir, file_name))
            count += 1
