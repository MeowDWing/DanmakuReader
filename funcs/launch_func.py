import time
from collections import deque

from PyQt5.QtCore import QThread
from pycaw.pycaw import AudioUtilities
import pyttsx3

from ui import launchwindow

import liveget as lg
import event_handler


class RecThread(QThread):
    """
        接收线程
    """
    def __init__(self, _g_queue: deque):
        super().__init__()
        self._g_queue = _g_queue

        self.x = None

    def run(self):
        self.x = lg.LiveInfoGet(g_queue=self._g_queue)
        self.x.living_on()


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

# 弹幕计数功能实现，暂时没用，将于以后加入时段弹幕量后加入主程序（注释编写时间：v1.2-alpha)

class Linkedlist(object):
    def __init__(self, value, succeed=None):
        self.value = value
        self.succeed = succeed

    def __len__(self):
        if self.succeed is not None:
            i = self.succeed.__len__() + 1
        else:
            i = 1

        return i

    def cut(self):
        ret = self.succeed
        self.succeed = None
        return ret


class DanmakuCountNode(Linkedlist):
    def __init__(self, succeed=None):
        t = int(time.time())
        super().__init__(t, succeed)

    def cut(self):
        ret = super().cut()
        if ret.succeed is not None:
            former = ret.succeed
            former.succeed.cut()
        del ret

class Counter:
    """

        弹幕计数器

    """
    def __init__(self):
        # [danmaku content] : DanmakuCountNode
        self.count = dict()
        self.common_preserve = []
        self.common_preserve_min_len = 0

    def append(self, danmaku_content):
        if danmaku_content in self.count.keys():
            p: DanmakuCountNode = self.count[danmaku_content]
            newp = DanmakuCountNode(p)
        else:
            newp = DanmakuCountNode(None)

        self.count[danmaku_content] = newp
        self.update_maintain(newp)
        if l:=newp.__len__()>self.common_preserve_min_len:
            self.common_preserve.append((danmaku_content,l))

    def common_maintain(self):
        temp_cp = [] # temp common preserve list
        for tup in self.common_preserve:
            if tup[0] in self.count.keys():
                self.update_maintain(self.count[tup[0]])
                l = len(self.count[tup[0]])
                temp_cp.append((tup[0],l))
            else:
                pass

        new_cp = sorted(temp_cp,key=lambda x:x[1],reverse=True)
        if len(new_cp) > 10:
            self.common_preserve = new_cp[0:10]
        else:
            self.common_preserve = new_cp

        self.common_preserve_min_len = new_cp[-1][1]

    def update_maintain(self, p:DanmakuCountNode):
        if p.value+600<int(time.time()):
            p.cut()
        else:
            if p.succeed is not None:
                self.update_maintain(p.succeed)
            else:
                pass

    def absolutely_maintain(self):
        for key in self.count.keys():
            self.update_maintain(self.count[key])
            if (l := len(self.count[key]))>self.common_preserve_min_len:
                self.common_preserve.append((self.count[key],l))

        new_cp = sorted(self.common_preserve, key=lambda x: x[1], reverse=True)
        if len(new_cp) > 10:
            self.common_preserve = new_cp[0:10]
        else:
            pass

        self.common_preserve_min_len = self.common_preserve[-1][1]


