import os
import time

import global_setting
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget
from ui import danmakureaderwindow, updatecontent, login_qrcode, loginwindow, launchwindow
from bilibili_api import login_func, login, settings, exceptions, Credential

import liveget as lg
from funcs import launch_func
import multiprocessing



cred : Credential | None = None

class DanmakuReaderMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = danmakureaderwindow.Ui_DanmakuReader()
        self.ui.setupUi(self)
        self.update_window = None
        self.login_window = None
        self.launch_window = None

    def display(self):
        self.show()

    def launch(self):
        self.launch_window = LaunchWindow()
        self.display()

    def settings(self):
        pass

    def check(self, action: QtWidgets.QAction):
        act_name = action.text()
        if act_name == "屏蔽词列表":
            os.system("ban_word.txt")
        elif act_name == "更新内容":
            self.update_window = UpdateContentWindow()
            self.update_window.show()



    def login(self):
        self.login_window = LoginWindow()
        self.login_window.show()


class LaunchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = launchwindow.Ui_Launch()
        self.ui.setupUi(self)
        self.__global_queue = None
        self.process_receiver: multiprocessing.Process | None = None
        self.process_reader: multiprocessing.Process | None = None

    def display(self):
        self.show()

    def init_reader_and_receiver(self):
        self.__global_queue = multiprocessing.Queue(233)
        print('正在读取房间号...')

        print('正在初始化弹幕获取器...')
        self.process_receiver = multiprocessing.Process(target=launch_func.receiver, args=(self.__global_queue,self.ui))

        print("正在初始化阅读器...")
        self.process_reader = multiprocessing.Process(target=launch_func.reader, args=(self.__global_queue,self.ui))

    def start_process(self):
        self.process_receiver.start()
        self.process_reader.start()

    def join2txt_browser(self, which, txt):
        pass

    def test(self):
        self.startTimer(100)

    def timerEvent(self, a0) -> None:
        self.ui.readtext.append("<font color=\"#00FFFF\"> WOW <\\font>")

class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.save_password_flag : bool = False
        self.loginwindow_ui = loginwindow.Ui_LoginWindow()
        self.loginwindow_ui.setupUi(self)
        self.login_func_index = self.loginwindow_ui.comboBox.currentIndex()

        self.__self_login_func_choice(self.login_func_index)

        self.button_click_behavior = 0

    def display(self):
        self.show()

    def loginwindow_login(self):
        idx = self.login_func_index
        if idx == 0:
            account = self.loginwindow_ui.nnl.text()
            pw = self.loginwindow_ui.pwl.text()
            self.login_by_pw(account, pw)
            if self.loginwindow_ui.checkBox.isChecked():
                pass

    def loginwindow_save_password(self, save):
        self.save_password_flag = save

    def loginwindow_loginfunc_combox(self, idx):
        self.__self_login_func_choice(idx)

    def __self_login_func_choice(self, idx):

        self.login_func_index = idx

        if idx == 0:
            self.loginwindow_ui.pw.setText("密码")
            self.loginwindow_ui.pushButton.setText("登录")
        elif idx == 1:
            self.loginwindow_ui.pw.setText("验证码")
            self.loginwindow_ui.pushButton.setText("获取验证码")
            self.button_click_behavior = 1
        elif idx == 2:
            self.loginwindow_ui.checkBox.hide()
            self.loginwindow_ui.pushButton.hide()
            self.newui = QRCodeWindow()
            self.newui.display()


    @staticmethod
    def login_by_pw(account, password):
        global cred
        settings.geetest_auto_open = True
        try:
            cred = login.login_with_password(account, password)
        except exceptions.LoginError as el:
            cred = None
            # ios.print_details(el.msg, tag='WRONG', head='WRONG', prefix='LOGIN')
            # time.sleep(1)
            return 'False', 'False'
        if isinstance(cred, login.Check):
            # 还需验证
            pass
            return account, password
        else:
            return account, password


class QRCodeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = login_qrcode.Ui_Login()
        self.ui.setupUi(self)

    def display(self):
        self.show()


class UpdateContentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = updatecontent.Ui_UpdateContent()
        self.ui.setupUi(self)
        self.set_content()

    def set_content(self):
        with open(f"{global_setting.version}.md", mode='r', encoding='utf-8') as f:
            lines = f.readlines()
        content = "".join(lines)
        print(content)
        self.ui.textBrowser.setMarkdown(content)

