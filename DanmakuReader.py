import sys

from PyQt5 import QtWidgets
from dr_window import DanmakuReaderMainWindow, LoginWindow




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = DanmakuReaderMainWindow()
    mainwindow.display()

    sys.exit(app.exec_())