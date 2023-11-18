import sys

from PyQt5 import QtWidgets
from bilibili_api import settings

import global_setting
import initial
from funcs.file_func import redirect_print
from dr_window import DanmakuReaderMainWindow


def sys_init():
    """

        系统全局变量设置初始化

    """
    initial.initial()
    settings.geetest_auto_open = True
    global_setting.load_setting()
    global_setting.other_init()
    redirect_print()


if __name__ == '__main__':
    sys_init()

    app = QtWidgets.QApplication(sys.argv)
    mainwindow = DanmakuReaderMainWindow()
    mainwindow.display()

    sys.exit(app.exec_())
