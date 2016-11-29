# -*- coding: utf-8 -*-

from __future__ import print_function

from mainwindow import MainWindow

from PyQt4.Qt import *
import sys

app = QApplication(sys.argv)

""" Initialize User Interface """
main_window = MainWindow()
main_window.setWindowTitle("Image Downloader")
main_window.show()

sys.exit(app.exec_())
