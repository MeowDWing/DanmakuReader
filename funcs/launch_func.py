from PyQt5.QtCore import QThread
from collections import deque
import pyttsx3
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


class Narrator:
    """ 文本读取器（pyttsx3） """
    def __init__(self):
        self.say_engin = pyttsx3.init()
        self.say_engin.setProperty('rate', 250)
        self.say_engin.setProperty('volume', 0.9)
        voices = self.say_engin.getProperty('voices')
        self.say_engin.setProperty('voice', voices[0].id)

    def txt2audio(self, message: str) -> None:
        self.say_engin.say(message)
        self.say_engin.runAndWait()
        self.say_engin.stop()

