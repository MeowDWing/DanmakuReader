# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'danmakureaderwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DanmakuReader(object):
    def setupUi(self, DanmakuReader):
        DanmakuReader.setObjectName("DanmakuReader")
        DanmakuReader.resize(260, 300)
        DanmakuReader.setMinimumSize(QtCore.QSize(260, 300))
        DanmakuReader.setMaximumSize(QtCore.QSize(260, 300))
        self.centralwidget = QtWidgets.QWidget(DanmakuReader)
        self.centralwidget.setObjectName("centralwidget")
        self.Launch = QtWidgets.QPushButton(self.centralwidget)
        self.Launch.setGeometry(QtCore.QRect(55, 55, 150, 30))
        self.Launch.setMinimumSize(QtCore.QSize(150, 30))
        self.Launch.setMaximumSize(QtCore.QSize(150, 30))
        self.Launch.setIconSize(QtCore.QSize(16, 16))
        self.Launch.setObjectName("Launch")
        self.Login = QtWidgets.QPushButton(self.centralwidget)
        self.Login.setGeometry(QtCore.QRect(40, 210, 75, 23))
        self.Login.setObjectName("Login")
        self.Settings = QtWidgets.QPushButton(self.centralwidget)
        self.Settings.setGeometry(QtCore.QRect(145, 210, 75, 23))
        self.Settings.setObjectName("Settings")
        self.Reset = QtWidgets.QPushButton(self.centralwidget)
        self.Reset.setGeometry(QtCore.QRect(145, 160, 75, 23))
        self.Reset.setObjectName("Reset")
        self.welcome = QtWidgets.QLabel(self.centralwidget)
        self.welcome.setGeometry(QtCore.QRect(55, 100, 150, 30))
        self.welcome.setObjectName("welcome")
        DanmakuReader.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(DanmakuReader)
        self.statusbar.setObjectName("statusbar")
        DanmakuReader.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(DanmakuReader)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 260, 23))
        self.menuBar.setObjectName("menuBar")
        self.checklist = QtWidgets.QMenu(self.menuBar)
        self.checklist.setObjectName("checklist")
        DanmakuReader.setMenuBar(self.menuBar)
        self.banword = QtWidgets.QAction(DanmakuReader)
        self.banword.setObjectName("banword")
        self.update = QtWidgets.QAction(DanmakuReader)
        self.update.setObjectName("update")
        self.checklist.addAction(self.banword)
        self.checklist.addAction(self.update)
        self.menuBar.addAction(self.checklist.menuAction())

        self.retranslateUi(DanmakuReader)
        self.Launch.clicked.connect(DanmakuReader.launch) # type: ignore
        self.Settings.clicked.connect(DanmakuReader.settings) # type: ignore
        self.Login.clicked.connect(DanmakuReader.login) # type: ignore
        self.menuBar.triggered['QAction*'].connect(DanmakuReader.check) # type: ignore
        self.Reset.clicked.connect(DanmakuReader.reset) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DanmakuReader)

    def retranslateUi(self, DanmakuReader):
        _translate = QtCore.QCoreApplication.translate
        DanmakuReader.setWindowTitle(_translate("DanmakuReader", "MainWindow"))
        self.Launch.setText(_translate("DanmakuReader", "狐神！启动！"))
        self.Login.setText(_translate("DanmakuReader", "登录"))
        self.Settings.setText(_translate("DanmakuReader", "设置"))
        self.Reset.setText(_translate("DanmakuReader", "重置"))
        self.welcome.setText(_translate("DanmakuReader", "<html><head/><body><p style=\" font-weight:600; color:#0000ff; text-align:center\">未登录</p></body></html>"))
        self.checklist.setTitle(_translate("DanmakuReader", "查看"))
        self.banword.setText(_translate("DanmakuReader", "屏蔽词列表"))
        self.update.setText(_translate("DanmakuReader", "更新内容"))
