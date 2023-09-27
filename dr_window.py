import os
from collections import deque

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox

from bilibili_api import login, settings, exceptions, credential, sync

import initial
import global_setting
import iosetting as ios
from ui import danmakureaderwindow, updatecontent, login_qrcode, loginwindow, launchwindow
from funcs import launch_func, file_func, login_func


class DanmakuReaderMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = danmakureaderwindow.Ui_DanmakuReader()
        self.ui.setupUi(self)
        if sync(global_setting.credential.check_valid()):
            n = global_setting.user_info.nickname()
            self.ui.welcome.setText(
                f"<p style=\" font-weight:600; color:#0000ff; text-align:center\">欢迎回来：{n}</p>"
            )
        else:
            self.ui.welcome.setText(
                "<p style=\" font-weight:600; color:#0000ff; text-align:center\">未登录</p>"
            )
        self.update_window = None
        self.login_window = None
        self.launch_window = None

    def display(self):
        self.show()

    def login_update(self):
        if credential.check_cookies(global_setting.credential):
            n = global_setting.user_info.nickname()
            self.ui.welcome.setText(
                f"<p style=\" font-weight:600; color:#0000ff; text-align:center\">欢迎回来：{n}</p>"
            )
        else:
            self.ui.welcome.setText(
                "<p style=\" font-weight:600; color:#0000ff; text-align:center\">未登录</p>"
            )

    def launch(self):
        self.launch_window = LaunchWindow()
        self.launch_window.display()
        self.close()

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
        self.login_window = LoginWindow(self)
        self.login_window.show()

    def reset(self):

        confirm = QMessageBox()
        confirm.setIcon(QMessageBox.Question)
        confirm.setWindowTitle("重置确认")
        confirm.setText("<b>重置将删除所有已设置数据，你确定吗</b>")
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setDefaultButton(QMessageBox.No)

        choice = confirm.exec_()

        if choice == QMessageBox.Yes:
            save_initial_dict = ios.JsonParser.load('./files/INITIAL')

            file_func.file_clearer('./files')
            if os.path.exists('ban_word.txt'):
                os.remove('ban_word.txt')
            initial.initial()
            ios.JsonParser.dump('./files/INITIAL', save_initial_dict, mode='w')

        else:
            pass


class LaunchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = launchwindow.Ui_Launch()
        self.ui.setupUi(self)
        self.__global_queue = None
        self.process_receiver: QtCore.QThread | None = None
        self.process_reader: QtCore.QThread | None = None

        self.ui.readtext.setStyleSheet('''
            QTextBrowser 
            {
                color: white;
                background: black;
                font-family:Times New Roman
            }
        ''')
        self.ui.recivetext.setStyleSheet('''
            QTextBrowser 
            {
                color: white;
                background: black;
                font-family:Times New Roman
            }
        ''')

    def display(self):

        self.show()
        self.init_reader_and_receiver()

    def init_reader_and_receiver(self):
        self.__global_queue = deque()
        print('正在读取房间号...')

        print('正在初始化弹幕获取器...')
        self.process_receiver = launch_func.RecThread(_g_queue=self.__global_queue, _ui=self.ui)

        print("正在初始化阅读器...")
        self.process_reader = launch_func.RdThread(_g_queue=self.__global_queue, _ui=self.ui)
        print(1)

        self.process_reader.start()
        self.process_receiver.start()

    def join2txt_browser(self, which, txt):
        pass

    def test(self):
        self.startTimer(100)

    def timerEvent(self, a0) -> None:
        self.ui.readtext.append("<font color=\"#00FFFF\"> WOW <\\font>")


class LoginWindow(QWidget):

    def __init__(self, main_window: DanmakuReaderMainWindow):
        super().__init__()
        self.save_password_flag: bool = False
        self.ui = loginwindow.Ui_LoginWindow()
        self.ui.setupUi(self)
        self.save_password_flag = global_setting.settings['sys_setting']['save_account']
        if self.save_password_flag:
            self.ui.checkBox.setChecked(True)
        self.login_func_index = self.ui.comboBox.currentIndex()
        self.main_window = main_window
        self.__self_login_func_choice(self.login_func_index)


    def display(self):
        self.show()

    def loginwindow_login(self):
        sign: login_func.LoginState | None = None
        idx = self.login_func_index
        if idx == 0:
            account = self.ui.nnl.text()
            pw = self.ui.pwl.text()
            save = False
            if self.ui.checkBox.isChecked():
                save = True
            sign = login_func.login_by_pw(account, pw, save=save)

        elif idx == 1:
            phone = self.ui.nnl.text()
            code = self.ui.pwl.text()
            sign = login_func.login_by_sms(phone, code)

        if sign == login_func.LoginState.success:
            self.main_window.update_window()
            self.close()
        elif sign is None:
            pass  # raise 登录状态错误
        else:
            pass  # 显示错误数据

    def get_sms(self):
        phone = self.ui.nnl.text()
        login_func.get_sms_code(phone)

    def loginwindow_save_password(self, save):
        self.save_password_flag = save
        global_setting.settings['sys_setting']['save_account'] = save
        global_setting.update_setting()

    def loginwindow_loginfunc_combox(self, idx):
        self.__self_login_func_choice(idx)

    def __self_login_func_choice(self, idx):

        self.login_func_index = idx

        if idx == 0:
            self.ui.checkBox.show()
            self.ui.pushButton_2.hide()
            self.ui.pw.setText("密码")
            self.ui.pwl.setEchoMode(2)
        elif idx == 1:
            self.ui.pushButton_2.show()
            self.ui.checkBox.hide()
            self.ui.pw.setText("验证码")
            self.ui.pwl.setEchoMode(0)
        elif idx == 2:
            self.ui.checkBox.hide()
            self.ui.pushButton.hide()
            self.qrcode_window = QRCodeWindow(self.main_window)
            self.qrcode_window.display()


class QRCodeWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
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
