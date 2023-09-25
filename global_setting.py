"""

    全局变量

"""
from bilibili_api import Credential
import iosetting as ios

# 版本控制

version = 'v1.0-alpha'
proj_name = 'Danmaku  Reader'

"""全局变量"""
settings = {}
offline = False
credential: str | None | Credential = None


def load_setting():

    global settings
    settings = ios.JsonParser.load('./files/settings.txt')


def update_setting():

    global settings
    set_backup = ios.JsonParser.load('./files/settings.txt')
    ios.JsonParser.dump('./files/settings_backup.txt', set_backup, mode='w')
    ios.JsonParser.dump('./files/settings.txt', settings, mode='w')
