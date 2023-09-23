"""

    全局变量

"""
import iosetting as ios

# 版本控制

version = 'v2.3-demo-PUSH11'
proj_name = 'Danmaku  Reader'

"""全局变量"""
settings = {}
offline = False


def load_setting():

    global settings
    settings = ios.JsonParser.load('./files/settings.txt')


def update_setting():

    global settings
    set_backup = ios.JsonParser.load('./files/settings.txt')
    ios.JsonParser.dump('./files/settings_backup.txt', set_backup, mode='w')
    ios.JsonParser.dump('./files/settings.txt', settings, mode='w')
