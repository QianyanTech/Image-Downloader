# -*- coding: utf-8 -*-


class AppConfig(object):
    def __init__(self):
        self.engine = "Google"

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

        str_paras += ' -n ' + str(self.max_number)

        str_paras += ' -t ' + str(self.num_threads)

        str_paras += ' -o "' + self.output_dir + '/' + self.keywords + '"'

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

    pass


def gen_keywords_list_from_str(keywords_str, sep=","):
    return keywords_str.split(sep)


def gen_keywords_list_from_file(filepath):
    with open(filepath, "r") as f:
        return f.readlines()
