import time
from collections import deque

from PyQt5.QtCore import QThread
from pycaw.pycaw import AudioUtilities
import pyttsx3

from ui import launchwindow

import distribution as lg
import event_handler


class DistributeThread(QThread):
    """
        分发线程
    """
    def __init__(self, danmu:deque, gift:deque, others:deque):
        super().__init__()
        self.danmu = danmu
        self.gift = gift
        self.others = others

        self.distributor = None

    def run(self):
        self.distributor = lg.ReceiveAndDistribution(danmaku=self.danmu, gift=self.gift, others=self.others)
        self.distributor.living_on()

class EventHandlerThread(QThread):
    def __init__(self, danmu:deque, gift:deque, others:deque, to_thread_reader:deque):
        super().__init__()
        self._event_handler = None
        self.danmu = danmu
        self.gift = gift
        self.others = others
        self.to_thread_reader = to_thread_reader

    def run(self) -> None:
        self._event_handler = event_handler.EventProcessor(
            danmu=self.danmu, gift=self.gift, others=self.others, to_thread_reader=self.to_thread_reader
        )
        self._event_handler.processor()

class RdThread(QThread):
    """
        读线程
    """
    def __init__(self, _g_queue: deque, _ui: launchwindow):
        super().__init__()
        self._g_queue = _g_queue
        self.read = None
        self.ui = _ui

    def run(self):
        self.read = event_handler.Reader(self._g_queue, self.ui)
        self.read.reader()


class Narrator:
    """ 文本读取器（pyttsx3） """
    def __init__(self):
        # tts zone
        self.say_engin = pyttsx3.init()
        self.say_engin.setProperty('rate', 250)
        self.say_engin.setProperty('volume', 1.0)
        voices = self.say_engin.getProperty('voices')
        self.say_engin.setProperty('voice', voices[0].id)

    def txt2audio(self, message: str) -> None:
        self.say_engin.say(message)
        self.say_engin.runAndWait()
        self.say_engin.stop()


class VolumeCtrl:
    """ 音量调整器（pycaw） """
    def __init__(self, pid):

        # volume ctrl zone
        self.pid = pid
        self.process_name = None

        self.interface = None

        self.check = False

        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.ProcessId == self.pid:
                self.interface = session.SimpleAudioVolume
                self.check = True

    def get_all_sessions_name(self):
        sessions_name = []
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            sessions_name.append(session.Process.name())
            if session.ProcessId == self.pid:
                self.process_name = session.Process.name()
        return sessions_name

    def now_volume(self):

        return self.interface.GetMasterVolume()

    def set_volume(self, vol: int):
        norm_vol = max(0.0, min(1.0, vol / 100.0))
        self.interface.SetMasterVolume(norm_vol, None)





