from PyQt5.QtCore import QThread
from collections import deque
from ui import launchwindow
import liveget as lg
import reader as rd


class RecThread(QThread):
    """
        接收线程
    """
    def __init__(self, _g_queue: deque, _ui: launchwindow.Ui_Launch):
        super().__init__()
        self._g_queue = _g_queue
        self._ui = _ui

    def run(self):
        x = lg.LiveInfoGet(g_queue=self._g_queue, ui=self._ui)
        x.living_on()


class RdThread(QThread):
    """
        读线程
    """
    def __init__(self, _g_queue: deque, _ui: launchwindow.Ui_Launch):
        super().__init__()
        self._g_queue = _g_queue
        self._ui = _ui

    def run(self):
        read = rd.Reader(self._g_queue, ui=self._ui)
        read.reader()

