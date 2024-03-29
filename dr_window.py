"""

    dr_window: Danmaku Reader(dr) Window file

"""

import os
from collections import deque

import bilibili_api
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox

from bilibili_api import credential, sync

import initial
import global_setting
import iosetting as ios
from ui import danmakureaderwindow, updatecontent, login_qrcode, loginwindow, launchwindow, settingswindow
from funcs import launch_func, file_func, login_func

class DanmakuReaderMainWindow(QMainWindow):
    """
        主窗口
    """
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

        # 子窗口名初始化
        self.update_window = None
        self.login_window = None
        self.launch_window = None
        self.settings_window = None

        # 更新内容弹出
        self.update_auto_show = False
        if os.path.exists('./files/temp'):
            self.update_auto_show = True
            os.remove('./files/temp')

    def display(self) -> None:
        self.show()
        if self.update_auto_show:
            self.update_window = UpdateContentWindow()
            self.update_window.show()


    def login_update(self, state=0) -> None:
        """
            更新登录状态
        :param state: 0-初始化登录 1-登录成功后更新
        """
        online = sync(credential.check_cookies(global_setting.credential))

        if state == 1:
            online = True

        if online:
            global_setting.user_info.update(c=global_setting.credential)
            n = global_setting.user_info.nickname()
            self.ui.welcome.setText(
                f"<p style=\" font-weight:600; color:#0000ff; text-align:center\">欢迎回来：{n}</p>"
            )
        else:
            self.ui.welcome.setText(
                "<p style=\" font-weight:600; color:#0000ff; text-align:center\">未登录</p>"
            )

    def launch(self) -> None:
        """
            启动（名词）窗口
        """
        self.launch_window = LaunchWindow()
        self.launch_window.display()
        self.close()

    def settings(self) -> None:
        """
            设置窗口
        """
        self.settings_window = SettingsWindow()
        self.settings_window.display()

    def check(self, action: QtWidgets.QAction) -> None:
        """
            查看操作
        :param action: 选择的选项
        """
        act_name = action.text()
        if act_name == "更新内容":
            self.update_window = UpdateContentWindow()
            self.update_window.show()

    def login(self) -> None:
        """
            登录窗口
        """
        self.login_window = LoginWindow(self)
        self.login_window.display()

    @staticmethod
    def reset() -> None:
        """
            重置选项
        """

        # 确认框
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
    """
        启动窗口
    """
    def __init__(self) -> None:
        super().__init__()
        self.ui = launchwindow.Ui_Launch()
        self.ui.setupUi(self)

        self.__global_queue = None
        self.process_receiver: launch_func.RecThread | None = None
        self.process_reader: launch_func.RecThread | None = None

        self.ui.lvl_combox.setCurrentText(str(global_setting.settings.min_lvl))

        # 音量调节部分初始化
        '''
            音量滑块文档：
                按下 - 记录位置，按下标记
                移动 - 如果已按下，则操作
                释放 - 清除按下标记
            简写：
                n -> normalize
                p -> pos -> position
                x, y, w, h -> x, y, width, height
        '''
        # - 初始值设置
        self.volume_bar = self.ui.volume_bar
        self.volume_bar.setValue(int(global_setting.settings.vol))
        # - 事件捕获
        self.volume_bar.mousePressEvent = self.slider_mouse_press_event
        self.volume_bar.mouseReleaseEvent = self.slider_mouse_realise_event
        self.volume_bar.mouseMoveEvent = self.slider_mouse_move_event
        # - 事件变量整理
        self.volume_bar_pressed = False


    '''  ------ 音量调节函数部分 起始 -------- '''
    def slider_mouse_press_event(self, a0: QtGui.QMouseEvent) -> None:

        self.volume_bar_pressed = True

    def slider_mouse_realise_event(self, a0: QtGui.QMouseEvent) -> None:

        self.volume_bar_pressed = False
        w = self.volume_bar.width()
        p = a0.pos()
        px = p.x()

        now_x = int((self.volume_bar.value()/100)*w)

        if (now_x - 40) < px < (now_x + 40):
            pass
        else:
            px = int((px / w) * 100)
            self.volume_bar.setValue(px)
            global_setting.volume_ctrl.set_volume(px)


    def slider_mouse_move_event(self, a0: QtGui.QMouseEvent) -> None:
        if self.volume_bar_pressed is True:
            w = self.volume_bar.width()
            p = a0.pos()
            px = p.x()
            npx = int((px/w)*100)
            self.volume_bar.setValue(npx)
            global_setting.volume_ctrl.set_volume(npx)
        else:
            pass

    '''  ------ 音量调节函数部分 结束 -------- '''

    def display(self) -> None:
        """
            显示界面，并初始化接受机制和读取机制
        """
        self.show()
        self.init_reader_and_receiver()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        s_vol = global_setting.settings.vol
        now_vol = self.volume_bar.value()
        if s_vol != now_vol:
            run_dict = global_setting.settings.run_dict_constructor(vol=now_vol)
            global_setting.settings.update_conform_and_dump(run_dict=run_dict)

        super().closeEvent(a0)

    def init_reader_and_receiver(self) -> None:
        self.__global_queue = deque()
        print('正在读取房间号...')

        print('正在初始化弹幕获取器...')
        self.process_receiver = launch_func.RecThread(_g_queue=self.__global_queue)

        print("正在初始化阅读器...")
        self.process_reader = launch_func.RdThread(_g_queue=self.__global_queue, _ui=self.ui)

        self.process_reader.start()
        self.process_receiver.start()

    def temp_lvl_limit(self):
        if isinstance(self.process_receiver, launch_func.RecThread):
            temp_lvl_str = self.ui.lvl_combox.currentText()
            if len(temp_lvl_str)<5:
                temp_lvl = int(temp_lvl_str)
            else:
                temp_lvl = -1

            if temp_lvl>0:
                self.process_receiver.x.min_lvl = temp_lvl
                self.process_receiver.x.read_any_lvl = False
            elif temp_lvl==0:
                self.process_receiver.x.min_lvl = 0
                self.process_receiver.x.read_any_lvl = True


    def pause_read(self):
        pause = global_setting.read_pause

        if pause:
            self.ui.pause_btn.setText('暂停')
            pause = not pause
        else:
            self.ui.pause_btn.setText('继续')
            pause = not pause

        global_setting.read_pause = pause

    def join2txt_browser(self, which, txt) -> None:
        pass

    def test(self) -> None:
        """
            定时器测试用例，无实际用处
        :return:
        """
        self.startTimer(100)

    def timerEvent(self, a0) -> None:
        pass


class LoginWindow(QWidget):
    """
        登录窗口类
    """

    def __init__(self, main_window: DanmakuReaderMainWindow):
        super().__init__()
        self.save_password_flag: bool = False
        self.ui = loginwindow.Ui_LoginWindow()
        self.ui.setupUi(self)

        account = global_setting.INITIAL.id
        self.ui.nnl.setText(account)

        self.save_password_flag = global_setting.settings.save_account
        if self.save_password_flag:
            self.ui.checkBox.setChecked(True)
            self.ui.pwl.setText(global_setting.INITIAL.pw)

        self.login_func_index = self.ui.comboBox.currentIndex()
        self.main_window = main_window
        self.__self_login_func_choice(self.login_func_index)


    def display(self) -> None:
        self.show()
        self.main_window.hide()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.main_window.display()
        super().closeEvent(a0)

    def close(self) -> bool:
        ret = super().close()
        return ret

    def loginwindow_login(self) -> None:
        """
            ”登录“按钮槽
        """

        sign: login_func.LoginState | None = None
        idx = self.login_func_index
        """ idx: 0->账号密码 1->验证码 2->二维码 """
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
            try:
                sign = login_func.login_by_sms(phone, code)
            except:
                sign = login_func.LoginState.fail

        if sign == login_func.LoginState.success:
            self.main_window.login_update(1)
            self.close()
        elif sign is None:
            pass  # raise 登录状态错误
        else:
            pass  # 显示错误数据

    def get_sms(self) -> None:
        """ 验证码发送 """
        phone = self.ui.nnl.text()
        login_func.get_sms_code(phone)

    def loginwindow_save_password(self, save: bool) -> None:
        """
            是否保存账号密码（not yet finished）
        :param save: True or False
        """
        self.save_password_flag = save
        global_setting.settings.save_account = save
        global_setting.settings.update_conform_and_dump()

    def loginwindow_loginfunc_combox(self, idx) -> None:
        """
            登录方式选择
        :param idx: 0-账号密码 1-验证码 2-二维码
        """
        self.__self_login_func_choice(idx)

    def __self_login_func_choice(self, idx) -> None:
        """
            方式选择导致的界面变更
        :param idx: 0-账号密码 1-验证码 2-二维码
        """
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
            self.ui.pushButton_2.hide()
            self.qrcode_window = QRCodeWindow(self.main_window)
            self.qrcode_window.display()


class QRCodeWindow(QWidget):
    """ 二维码登录界面（ui复制自bilibili-api-python项目）"""
    def __init__(self, main_window) -> None:
        """
        :param main_window: 主界面实例
        """
        super().__init__()
        self.main_window = main_window
        self.ui = login_qrcode.Ui_Login()
        self.qrcode_timer_id = self.ui.setupUi(self)

    def display(self) -> None:
        self.qrcode_timer_id = self.startTimer(1000)
        self.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.killTimer(self.qrcode_timer_id)
        super().closeEvent(a0)


class UpdateContentWindow(QWidget):
    """ ”更新“按钮界面 """
    def __init__(self):
        super().__init__()
        self.ui = updatecontent.Ui_UpdateContent()
        self.ui.setupUi(self)
        self.set_content()

    def set_content(self) -> None:
        """ markdown文本内容设置 """
        with open(f"{global_setting.version}.md", mode='r', encoding='utf-8') as f:
            lines = f.readlines()
        content = "".join(lines)
        print(content)
        self.ui.textBrowser.setMarkdown(content)


class SettingsWindow(QWidget):
    """ 设置界面 """
    def __init__(self):
        super().__init__()
        self.ui = settingswindow.Ui_settings_window()
        self.ui.setupUi(self)
        self.ui.ban_word_intro.setText(global_setting.ban_word.info)
        self.cookie_changed = False
        self.basic_changed = False
        self.sys_changed = False
        self.ban_changed = False
        self.refresh()

    def ban_word_content_change(self):
        self.ban_changed = True

    def ban_word_content_set(self):

        self.ui.matching_edit.clear()
        for what_banned in global_setting.ban_word.all_match:
            self.ui.matching_edit.append(what_banned)
        for what_banned in global_setting.ban_word.regex_match:
            self.ui.matching_edit.append('-'+what_banned)

    def refresh(self) -> None:
        self.ban_word_content_set()

        self.ui.sessdate_line.setText(global_setting.INITIAL.sessdate)
        self.ui.bili_jct_line.setText(global_setting.INITIAL.bili_jct)
        self.ui.buvid3_line.setText(global_setting.INITIAL.buvid3)

        self.ui.rid_line.setText(str(global_setting.settings.rid))
        self.ui.lvl_combox.setCurrentText(str(global_setting.settings.min_lvl))

        self.ui.auto_login_check.setChecked(global_setting.settings.login)
        self.ui.debug_check.setChecked(global_setting.settings.debug)

    def display(self) -> None:
        self.cookie_changed = False
        self.basic_changed = False
        self.sys_changed = False
        self.ban_changed = False
        self.refresh()
        self.show()

    def save_and_close(self) -> None:
        """ 保存并关闭按钮行为 """
        if self.cookie_changed:
            sessdata = self.ui.sessdate_line.text()
            bili_jct = self.ui.bili_jct_line.text()
            buvid3 = self.ui.buvid3_line.text()
            ac_time_value = global_setting.INITIAL.ac_time_value
            c = bilibili_api.Credential(sessdata=sessdata, bili_jct=bili_jct, buvid3=buvid3, ac_time_value=ac_time_value)

            global_setting.INITIAL.credential_consist(c)
            global_setting.INITIAL.update_and_dump()

        if self.basic_changed or self.sys_changed:
            basic_dict = None
            sys_dict = None
            if self.basic_changed:
                basic_dict = global_setting.settings.basic_settings_dict_constructor(
                    rid=self.ui.rid_line.text(), min_lvl=self.ui.lvl_combox.currentText()
                )
            if self.sys_changed:
                sys_dict = global_setting.settings.sys_settings_dict_constructor(
                    login=self.ui.auto_login_check.isChecked(), debug=self.ui.debug_check.isChecked()
                )
            global_setting.settings.update_conform_and_dump(basic_dict=basic_dict, sys_dict=sys_dict)

        if self.ban_changed:
            lines = self.ui.matching_edit.toPlainText().split()
            all_match = []
            regex_match = []
            for line in lines:
                line = line.strip()
                if line[0] == '-':
                    regex_match.append(line[1:])
                elif line[0] == '$':
                    pass
                else:
                    all_match.append(line)
            global_setting.ban_word.word_conform_update_and_dump(all_match_add=all_match, regex_match_add=regex_match)

        self.close()

    def cookie_change(self) -> None:
        """ 是否更新 """
        self.cookie_changed = True

    def sys_change(self) -> None:
        self.sys_changed = True

    def basic_change(self) -> None:
        self.basic_changed = True