# -*- coding: utf-8 -*-
# author: Yabin Zheng
# Email: sczhengyabin@hotmail.com

from ui_mainwindow import Ui_MainWindow
from ui_about import Ui_Dialog_about
import utils

from PyQt5.Qt import *
from PyQt5.QtTest import QTest
from threading import Thread
import shlex
import os

import image_downloader
from logger import logger


class DialogAbout(QDialog, Ui_Dialog_about):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        logger.log_hooks.append(self.log)
        self.log_queue = []

        QMainWindow.__init__(self)

        self.setupUi(self)

        self.dialog_about = DialogAbout()

        self.state = "stop"

        self.elapsed_timer = QElapsedTimer()

        self.update_timer = QTimer()
        self.update_timer.setInterval(100)
        self.update_timer.timeout.connect(self.update_elapsed_time)

        self.process_log_timer = QTimer()
        self.process_log_timer.setInterval(100)
        self.process_log_timer.timeout.connect(self.progress_log)
        self.process_log_timer.start()

        self.actionAbout.triggered.connect(self.dialog_about.show)

        self.pushButton_load_file.clicked.connect(
            lambda: self.lineEdit_path2file.setText(QFileDialog.getOpenFileName(
                self, "Load keywords from file", "./", "Text files (*.txt)")[0]))
        self.pushButton_output.clicked.connect(
            lambda: self.lineEdit_output.setText(QFileDialog.getExistingDirectory(
                self, "Set output directory", "./")))

        self.pushButton_start.clicked.connect(self.start_download)
        self.pushButton_cancel.clicked.connect(self.cancel_download)

    def log(self, text):
        if text.strip(" \n") == "":
            return
        self.log_queue.append(text)

    def progress_log(self):
        while len(self.log_queue) > 0:
            log_str = self.log_queue.pop(0)
            if log_str.startswith("=="):
                self.progressBar_current.setMaximum(int(log_str.split()[1]))
            if log_str.startswith("##"):
                self.progressBar_current.setValue(
                    self.progressBar_current.value() + 1)
            log_str = "[" + QTime.currentTime().toString() + "]  " + log_str
            self.plainTextEdit_log.appendPlainText(log_str)

    def reset_ui(self):
        self.progressBar_current.setFormat("")
        self.progressBar_current.reset()
        self.progressBar_total.setFormat("")
        self.progressBar_total.reset()
        self.label_time_elapsed.setText("00:00:00")
        self.plainTextEdit_log.clear()

    def update_elapsed_time(self):
        elapsed_total = self.elapsed_timer.elapsed() / 1000
        elapsed_hour = elapsed_total / 3600
        elapsed_minutes = (elapsed_total % 3600) / 60
        elapsed_secs = elapsed_total % 60
        str_elapsed_time = "%02d:%02d:%02d" % (
            elapsed_hour, elapsed_minutes, elapsed_secs)
        self.label_time_elapsed.setText(str_elapsed_time)

    def gen_config_from_ui(self):

        config = utils.AppConfig()

        """ Engine """
        if self.radioButton_google.isChecked():
            config.engine = "Google"
        elif self.radioButton_bing.isChecked():
            config.engine = "Bing"
        elif self.radioButton_baidu.isChecked():
            config.engine = "Baidu"

        """ Driver """
        if self.radioButton_chrome_headless.isChecked():
            config.driver = "chrome_headless"
        elif self.radioButton_chrome.isChecked():
            config.driver = "chrome"
        elif self.radioButton_phantomjs.isChecked():
            config.driver = "phantomjs"

        """ Output directory """
        config.output_dir = self.lineEdit_output.text()

        """ Switches """
        config.face_only = self.checkBox_face_only.isChecked()
        config.safe_mode = self.checkBox_safe_mode.isChecked()

        """ Numbers """
        config.max_number = self.spinBox_max_number.value()
        config.num_threads = self.spinBox_num_threads.value()

        """ Proxy """
        if self.checkBox_proxy.isChecked():
            if self.radioButton_http.isChecked():
                config.proxy_type = "http"
            elif self.radioButton_socks5.isChecked():
                config.proxy_type = "socks5"
            config.proxy = self.lineEdit_proxy.text()
        else:
            config.proxy_type = None
            config.proxy = None

        """ Keywords List """
        if self.checkBox_from_file.isChecked():
            str_path = self.lineEdit_path2file.text()
            keywords_list = utils.gen_keywords_list_from_file(str_path)
        else:
            str_keywords = self.lineEdit_keywords.text()
            keywords_list = utils.gen_keywords_list_from_str(str_keywords, ",")

        return config, keywords_list

    def start_download(self):
        if self.checkBox_from_file.isChecked() and self.lineEdit_path2file.text() == "" \
                or not self.checkBox_from_file.isChecked() and self.lineEdit_keywords.text() == "":
            print("Keywords is empty!")
            self.lineEdit_keywords.setFocus()
            return

        if self.lineEdit_output.text() == "":
            print("Output directory is empty!")
            self.lineEdit_output.setFocus()
            return

        self.state = "run"
        self.pushButton_start.setEnabled(False)
        self.pushButton_cancel.setEnabled(True)

        config, keywords_list = self.gen_config_from_ui()

        self.elapsed_timer.restart()
        self.update_timer.start()

        self.reset_ui()
        num_keywords = len(keywords_list)

        self.progressBar_total.setMaximum(num_keywords)
        self.progressBar_total.setFormat("%p%, %v/%m")
        self.progressBar_total.setValue(0)

        for index in range(num_keywords):
            if self.state != "run":
                break
            keywords = keywords_list[index].strip()
            if keywords == "":
                continue

            config.keywords = keywords
            str_paras = config.to_command_paras()

            print(str_paras)

            self.progressBar_current.setMaximum(config.max_number)
            self.progressBar_current.setValue(0)
            self.progressBar_current.setFormat(keywords + ", %p%, %v/%m")

            thread_download = Thread(target=image_downloader.main, args=[
                                     shlex.split(str_paras)])
            thread_download.start()

            while thread_download.is_alive():
                QTest.qWait(1000)
                if self.isHidden():
                    os._exit(0)

            self.progressBar_total.setValue(index + 1)

        if self.state == "run":
            self.state = "stop"
        self.pushButton_cancel.setEnabled(False)
        self.pushButton_start.setEnabled(True)
        self.update_timer.stop()
        print("stopped")
        pass

    def cancel_download(self):
        self.state = "stop"
        self.pushButton_cancel.setEnabled(False)

    pass
