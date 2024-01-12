import json
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from bilibili_api import user, sync
from bilibili_api import login_func as api_login_func
from funcs import login_func, file_func

import global_setting


# 二维码登录窗口类
class Ui_Login(object):
    def setupUi(self, Login) -> int:
        Login.setObjectName("Login")
        Login.setFixedSize(180, 210)
        icon = QtGui.QIcon()
        Login.setWindowIcon(icon)
        self.label_5 = QtWidgets.QLabel(Login)
        self.label_5.setGeometry(QtCore.QRect(10, 40, 161, 161))
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_2 = QtWidgets.QLabel(Login)
        self.label_2.setGeometry(QtCore.QRect(35, 10, 85, 21))
        self.label_2.setObjectName("label_2")
        self.pushButton_2 = QtWidgets.QPushButton(Login)
        self.pushButton_2.setGeometry(QtCore.QRect(120, 0, 50, 40))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Login)

        qrcode_data = api_login_func.get_qrcode()
        self.pixmap = QtGui.QPixmap()
        self.pixmap.loadFromData(qrcode_data[0].content, qrcode_data[0].imageType)
        self.label_5.setPixmap(self.pixmap)
        self.label_5.setScaledContents(True)
        self.qrcode_sec = qrcode_data[1]

        self.pushButton_2.setIcon(QtGui.QIcon(QtGui.QPixmap("update.jpg")))

        def update_qrcode():
            qrcode_data = api_login_func.get_qrcode()
            self.label_5.setPixmap(QtGui.QPixmap(qrcode_data[0]))
            self.label_5.setScaledContents(True)
            self.label_5.update()
            self.qrcode_sec = qrcode_data[1]

        self.pushButton_2.clicked.connect(update_qrcode)

        timer_id:int = Login.startTimer(1000)
        def timerEvent(*args, **kwargs):
            _translate = QtCore.QCoreApplication.translate
            try:
                events = api_login_func.check_qrcode_events(self.qrcode_sec)
            except Exception as e:
                print(e)
                self.label_2.setText(_translate("Login", "⚫️二维码登录"))
                return
            else:
                if events == None: return
                if events[0] == api_login_func.QrCodeLoginEvents.SCAN:
                    self.label_2.setText(_translate("Login", "🔴二维码登录"))
                elif events[0] == api_login_func.QrCodeLoginEvents.CONF:
                    self.label_2.setText(_translate("Login", "🟡二维码登录"))
                elif events[0] == api_login_func.QrCodeLoginEvents.DONE:
                    self.label_2.setText(_translate("Login", "🟢二维码登录"))
                    credential = events[1]
                    if credential.buvid3 is None:
                        credential.buvid3 = file_func.InitialParser.get_buvid3()
                    global_setting.credential = credential
                    global_setting.INITIAL.credential_consist(credential)
                    global_setting.INITIAL.update_and_dump()
                    global_setting.user_info = login_func.UserInfoParser(credential)
                    reply = QtWidgets.QMessageBox.information(
                        Login,
                        "已成功登录到你的帐号",
                        "欢迎：" + global_setting.user_info.nickname(),
                        QtWidgets.QMessageBox.Ok
                    )
                    Login.main_window.login_update(1)
                    Login.close()
        Login.timerEvent = timerEvent

        QtCore.QMetaObject.connectSlotsByName(Login)

        return timer_id

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "登录"))
        self.label_2.setText(_translate("Login", "🔴二维码登录"))