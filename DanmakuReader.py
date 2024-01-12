import sys
import logging
import time

from PyQt5 import QtWidgets, sip
from bilibili_api import settings

import global_setting
import initial
from dr_window import DanmakuReaderMainWindow

class InitialMethod:
    @classmethod
    def sys_init(cls):
        """
            系统全局初始化
        """
        initial.initial()

        cls.self_settings_init()
        cls.bilibili_api_init()
        cls.log_init()

    @staticmethod
    def self_settings_init():
        """设置初始化"""
        global_setting.load_setting()
        tof = global_setting.other_init()
        print(tof)

    @staticmethod
    def bilibili_api_init():
        """外部库初始化"""
        settings.geetest_auto_open = True

    @staticmethod
    def log_init():
        """日志与输出初始化"""
        f = open('./logging/print_cmd_logging.txt', 'a')
        f.write(f'---{time.time()}---\n')
        sys.stdout = f
        logging.basicConfig(level=logging.INFO, stream=sys.stdout, force=True)




if __name__ == '__main__':
    InitialMethod.sys_init()

    app = QtWidgets.QApplication(sys.argv)
    mainwindow = DanmakuReaderMainWindow()
    mainwindow.display()

    sys.exit(app.exec_())
