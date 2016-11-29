# -*- coding: utf-8 -*-

from ui_mainwindow import Ui_MainWindow

import utils

from PyQt4.Qt import *
from PyQt4.QtTest import QTest


script_image_download = "python3 image_downloader.py"


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setupUi(self)

        self.state = "stop"

        self.pushButton_load_file.clicked.connect(
            lambda: self.lineEdit_path2file.setText(QFileDialog.getOpenFileName(
                self, "Load keywords from file", "./", "Text files (*.txt)")))
        self.pushButton_output.clicked.connect(
            lambda: self.lineEdit_output.setText(QFileDialog.getExistingDirectory(
                self, "Set output directory", "./")))

        self.pushButton_start.clicked.connect(self.start_download)
        self.pushButton_cancel.clicked.connect(self.cancel_download)

    def log(self, text):
        self.plainTextEdit_log.appendPlainText("[" + QTime.currentTime().toString() + "]  " + text)

    def reset_ui(self):
        self.progressBar_current.setFormat("")
        self.progressBar_current.reset()
        self.progressBar_total.setFormat("")
        self.progressBar_total.reset()
        self.label_time_elapsed.clear()

    def gen_config_from_ui(self):

        config = utils.AppConfig()

        """ Engine """
        if self.radioButton_google.isChecked():
            config.engine = "Google"
        elif self.radioButton_bing.isChecked():
            config.engine = "Bing"
        elif self.radioButton_baidu.isChecked():
            config.engine = "Baidu"

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
            keywords_list = utils. gen_keywords_list_from_file(str_path)
        else:
            str_keywords = self.lineEdit_keywords.text()
            keywords_list = utils.gen_keywords_list_from_str(str_keywords, ",")

        return config, keywords_list

    def start_download(self):
        self.plainTextEdit_log.clear()
        if self.checkBox_from_file.isChecked() and self.lineEdit_path2file.text() == "" \
                or not self.checkBox_from_file.isChecked() and self.lineEdit_keywords.text() == "":
            self.log("Keywords is empty!")
            self.lineEdit_keywords.setFocus()
            return

        if self.lineEdit_output.text() == "":
            self.log("Output directory is empty!")
            self.lineEdit_output.setFocus()
            return

        self.state = "run"
        self.pushButton_start.setEnabled(False)
        self.pushButton_cancel.setEnabled(True)

        config, keywords_list = self.gen_config_from_ui()

        elapsed_timer = QElapsedTimer()
        elapsed_timer.start()

        self.reset_ui()
        num_keywords = len(keywords_list)

        self.progressBar_total.setMaximum(num_keywords)

        for index in range(num_keywords):
            if self.state != "run":
                break
            keywords = keywords_list[index].strip()
            self.progressBar_total.setValue(index+1)
            self.progressBar_total.setFormat("%p%, %v/%m")
            if keywords == "":
                continue
            config.keywords = keywords
            str_paras = config.to_command_paras()
            str_paras = script_image_download + " " + str_paras

            self.log(str_paras)

            self.progressBar_current.setMaximum(config.max_number)
            self.progressBar_current.setValue(0)
            self.progressBar_current.setFormat(keywords + ", %p%, %v/%m")

            process_download = QProcess(self)
            process_download.start(str_paras)

            num_downloaded = 0
            while True:
                if self.state != "run":
                    break
                if process_download.state() == QProcess.NotRunning:
                    break

                elapsed_total = elapsed_timer.elapsed() / 1000
                elapsed_hour = elapsed_total / 3600
                elapsed_minutes = (elapsed_total % 3600) / 60
                elapsed_secs = elapsed_total % 60
                str_elapsed_time = "%02d:%02d:%02d" % (elapsed_hour, elapsed_minutes, elapsed_secs)
                self.label_time_elapsed.setText(str_elapsed_time)
                QTest.qWait(100)

                if process_download.bytesAvailable():
                    str_debug = process_download.readAllStandardOutput()
                    str_debug += process_download.readAllStandardError()
                    logs = bytes(str_debug).decode("utf-8").splitlines()
                    for a_log in logs:
                        self.log(a_log)
                        if a_log.startswith("=="):
                            num_to_download = int(a_log.split()[1])
                            self.progressBar_current.setMaximum(num_to_download)
                        if a_log.startswith("##"):
                            num_downloaded += 1
                            self.progressBar_current.setValue(num_downloaded)

            if process_download.state() != QProcess.NotRunning:
                process_download.kill()

        if self.state == "run":
            self.cancel_download()

        pass

    def cancel_download(self):
        self.state = "stop"
        self.pushButton_cancel.setEnabled(False)
        self.pushButton_start.setEnabled(True)

        self.log("stopped")

    pass
