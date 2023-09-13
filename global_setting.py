"""

    全局变量

"""
import iosetting as ios

# 版本控制

version = 'v2.2-demo-PUSH10'
proj_name = 'Danmaku  Reader'

"""全局变量"""
settings = {}
offline = False


def load_setting():

    global settings
    settings = ios.JsonParser.load('./files/settings.txt')


def update_setting():

    global settings
    ios.JsonParser.dump('./files/settings.txt', settings, mode='w')
