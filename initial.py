"""

    系统初始化-》 包含各种文件的初始化与重置函数

"""

import os
import time
from iosetting import JsonParser


def initial():

    try:
        with open('./files/INITIAL', mode='r'):
            pass
    except FileNotFoundError:
        print('正在初始化')
        _initial()


def _initial():
    if not os.path.exists('./files'):
        print('正在创建files文件夹')
        os.mkdir('./files')

    if not os.path.exists('./logging'):
        print('正在创建logging文件夹')
        os.mkdir('./logging')

    with open('./files/INITIAL', mode='x'):
        pass

    initial_dict = {
        'what': '登录信息',
        'id': None,
        'pw': None,
        'sessdata': None,
        'bili_jct': None,
        'buvid3': None,
        'ac_time_value': None,
    }

    JsonParser.dump('./files/INITIAL', initial_dict, mode='w')

    try:
        with open('ban_word.txt', mode='r'):
            pass
    except FileNotFoundError:
        print('正在初始化屏蔽词文件')
        with open('ban_word.txt', mode='w', encoding='utf-8') as f:
            ban_word_init_lines = [
                '$ 在该文件下写入的所有词会被屏蔽,每行只写一个词,只屏蔽完全一致的弹幕',
                '$ 本文件中$（美元）符号开头的句子会被视为注释',
                '$ 更改屏蔽词需要重启应用（如果已经启动的话）',
                '$ 更多操作请参看README.MD文件（可以直接以文本形式打开）',
                '。',
                '赞',
                "$ '-'(减号)开头的会作为匹配词屏蔽。",
                "$ 系统会屏蔽所有包含匹配词的弹幕，请谨慎选择",
                '-红包',
            ]
            f.writelines(ban_word_init_lines)

    try:
        print('正在初始化设置文件')
        with open('./files/settings.txt', mode='r'):
            pass
    except FileNotFoundError:
        settings_initial()


def settings_initial():

    dicts = {
        'basic_setting': {
            'what': '直播间主属性',
            'rid': 34162,
            'min_level': 1,
        },
        'sys_setting': {
            'what': '系统行为设置',
            'login': False,
            'save_account': False,
            'debug': False,
        }
    }

    JsonParser.dump('./files/settings.txt', dicts, mode='w')




