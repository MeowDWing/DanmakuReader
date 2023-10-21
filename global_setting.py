"""

    全局变量

"""
from enum import Enum

from bilibili_api import Credential

import initial
import iosetting as ios
from funcs import file_func, login_func, launch_func


# 版本控制
version = 'v1.1-alpha'
proj_name = 'Danmaku Reader'

"""全局变量"""
settings: file_func.SettingsParser | None = None  # 设置
INITIAL: file_func.InitialParser | None = None  # INITIAL文件解释器
user_info: login_func.UserInfoParser | None = None  # 登陆用户信息解释器
offline = False  # 是否离线登录标记，后续优化如settings
credential: str | None | Credential = None  # 登陆证书

ban_word: file_func.BanWordParser | None = None  # 屏蔽词文件解释器


""" 讲述人初始化 """
narrator: launch_func.Narrator | None = None


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
    global narrator

    narrator = launch_func.Narrator()

