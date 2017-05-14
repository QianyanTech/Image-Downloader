# -*- coding: utf-8 -*-
# author: Yabin Zheng
# Email: sczhengyabin@hotmail.com

from __future__ import print_function
import sys
from mainwindow import MainWindow
from PyQt5.Qt import QApplication


def main():
    app = QApplication(sys.argv)

    font = app.font()
    if sys.platform.startswith("win"):
        font.setFamily("Microsoft YaHei")
    else:
        font.setFamily("Ubuntu")
    app.setFont(font)

    main_window = MainWindow()
    main_window.setWindowTitle("Image Downloader")
    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
