import multiprocessing
from ui import launchwindow
import liveget as lg
import reader as rd


def receiver(_g_queue: multiprocessing.Queue, _ui: launchwindow.Ui_Launch):
    x = lg.LiveInfoGet(g_queue=_g_queue, ui=_ui)
    x.living_on()


def reader(_queue:multiprocessing.Queue, _ui: launchwindow.Ui_Launch):
    read = rd.Reader(_queue, ui=_ui)
    read.reader()