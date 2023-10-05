import sys
import initial
from PyQt5 import QtWidgets
from bilibili_api import settings, Credential
import global_setting
from dr_window import DanmakuReaderMainWindow
from funcs import login_func


def sys_init():
    """

        系统全局变量设置初始化

    """
    initial.initial()
    settings.geetest_auto_open = True
    global_setting.load_setting()


if __name__ == '__main__':
    sys_init()

    app = QtWidgets.QApplication(sys.argv)
    mainwindow = DanmakuReaderMainWindow()
    mainwindow.display()

    sys.exit(app.exec_())
