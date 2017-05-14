# -*- coding: utf-8 -*-
# author: Yabin Zheng
# Email: sczhengyabin@hotmail.com

import sys


class Logger(object):
    def __init__(self):
        self.log_hooks = []
        self.saved_stderr = sys.stderr
        sys.stdout = self
        sys.stderr = self

    def log(self, log_str):
        # self.saved_stderr.write(log_str)
        logs = log_str.splitlines()
        for a_log in logs:
            for log_hook in self.log_hooks:
                log_hook(a_log)

    def write(self, text):
        self.log(text)

    def flush(self):
        pass


logger = Logger()
