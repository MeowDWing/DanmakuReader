"""

    全局变量

"""
from bilibili_api import Credential
import iosetting as ios
from funcs import file_func, login_func

# 版本控制

version = 'v1.0-alpha'
proj_name = 'Danmaku  Reader'

"""全局变量"""
settings = {}
INITIAL = None
user_info = None
offline = False
credential: str | None | Credential = None


def load_setting():

    global settings, INITIAL, user_info, credential

    settings = ios.JsonParser.load('./files/settings.txt')
    INITIAL = file_func.InitialParser()

    credential = INITIAL.get_credential()

    user_info = login_func.UserInfoParser(credential)


def update_setting():

    global settings
    set_backup = ios.JsonParser.load('./files/settings.txt')
    ios.JsonParser.dump('./files/settings_backup.txt', set_backup, mode='w')
    ios.JsonParser.dump('./files/settings.txt', settings, mode='w')
