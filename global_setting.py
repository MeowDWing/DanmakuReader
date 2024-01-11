"""

    全局变量

"""
import os
from enum import Enum

from bilibili_api import Credential

import initial
import iosetting as ios
from funcs import file_func, login_func, launch_func


# 版本控制
version = 'v1.2-alpha'
proj_name = 'Danmaku Reader'


"""背景变量"""
settings: file_func.SettingsParser | None = None  # 设置
INITIAL: file_func.InitialParser | None = None  # INITIAL文件解释器
user_info: login_func.UserInfoParser | None = None  # 登陆用户信息解释器
offline = False  # 是否离线登录标记，后续优化如settings
credential: str | None | Credential = None  # 登陆证书

ban_word: file_func.BanWordParser | None = None  # 屏蔽词文件解释器


""" 讲述人初始化 """
narrator: launch_func.Narrator | None = None
volume_ctrl : launch_func.VolumeCtrl|None = None


""" 操作变量 """
read_pause = False

""" 进程锁定 """
thread_locked = False

""" print 重定向; 初始化位于/logging/file_func.py """
_origin_print = None
redirect_print = None


class FileState(Enum):
    right = 0
    notFound = 1
    dictKeyLost = 2


def load_setting():

    global settings, INITIAL, user_info, credential, ban_word

    try:
        settings = file_func.SettingsParser()
    except FileNotFoundError:
        settings = FileState.notFound
    except TypeError:
        settings = FileState.dictKeyLost

    try:
        INITIAL = file_func.InitialParser()
    except FileNotFoundError:
        INITIAL = FileState.notFound
    except TypeError:
        INITIAL = FileState.dictKeyLost

    try:
        ban_word = file_func.BanWordParser()
    except FileNotFoundError:
        ban_word = FileState.notFound
    except TypeError:
        ban_word = FileState.dictKeyLost

    if isinstance(settings, FileState):
        initial.settings_initial()
        settings = file_func.SettingsParser()
    if isinstance(INITIAL, FileState):
        initial.INITIAL_initial()
        INITIAL = file_func.InitialParser()
    if isinstance(ban_word, FileState):
        initial.ban_word_initial()
        ban_word = file_func.BanWordParser()





    credential = INITIAL.get_credential()
    if credential is not None:
        user_info = login_func.UserInfoParser(credential)


def other_init():
    global narrator, volume_ctrl
    pid = os.getpid()
    narrator = launch_func.Narrator()
    for i in range(3):
        narrator.txt2audio('正在执行初始化，请稍后')
        volume_ctrl = launch_func.VolumeCtrl(pid)
        if volume_ctrl.check is True:
            return True

    return False




