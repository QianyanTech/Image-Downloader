# -*- coding: utf-8 -*-
# author: Yabin Zheng
# Email: sczhengyabin@hotmail.com


def gen_valid_dir_name_for_keywords(keywords):
    keep = ["-", "_", "."]
    keywords = keywords.replace(" ", "_").replace(":", "-")
    return "".join(c for c in keywords if c.isalnum() or c in keep).rstrip()


class AppConfig(object):
    def __init__(self):
        self.engine = "Google"
        
        self.driver = "chrome_headless"

        self.keywords = ""

        self.max_number = 0

        self.face_only = False

        self.safe_mode = False

        self.proxy_type = None
        self.proxy = None

        self.num_threads = 50

        self.output_dir = "./output"

    def to_command_paras(self):
        str_paras = ""
 
        str_paras += ' -e ' + self.engine

        str_paras += ' -d ' + self.driver

        str_paras += ' -n ' + str(self.max_number)

        str_paras += ' -j ' + str(self.num_threads)

        str_paras += ' -o "' + self.output_dir + '/' + \
            gen_valid_dir_name_for_keywords(self.keywords) + '"'

        if self.face_only:
            str_paras += ' -F '

        if self.safe_mode:
            str_paras += ' -S '

        if self.proxy_type is "http":
            str_paras += ' -ph "' + self.proxy + '"'
        elif self.proxy_type is "socks5":
            str_paras += ' -ps "' + self.proxy + '"'

        str_paras += ' "' + self.keywords + '"'

        return str_paras


def gen_keywords_list_from_str(keywords_str, sep=","):
    return keywords_str.split(sep)


def gen_keywords_list_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.readlines()
