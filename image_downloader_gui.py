
# -*- coding: utf-8 -*-

from __future__ import print_function

from mainwindow import MainWindow

from PyQt5.Qt import *
import sys, os


def main():
    app = QApplication(sys.argv)

    font = app.font()
    if sys.platform.startswith("win"):
        font.setFamily("Microsoft YaHei")
    else:
        font.setFamily("Ubuntu")
    app.setFont(font)

    """ Initialize User Interface """
    main_window = MainWindow()
    main_window.setWindowTitle("Image Downloader")
    main_window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
