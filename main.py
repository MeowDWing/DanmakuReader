# !/

import os
import time
import multiprocessing
from bilibili_api import settings
import interface
import iosetting as ios
import initial


__VERSION__ = 'v2.2-demo-PUSH10'
__PROJ_NAME__ = 'Danmaku  Reader'
__PREFIX = 'Mainc'


def sys_init():
    """

        系统全局变量设置初始化

    """

    settings.geetest_auto_open = True


def main():

    multiprocessing.freeze_support()
    print('正在检测初始化...')
    initial.initial()
    sys_init()
    while True:
        os.system('cls')
        interface.interface(
            proj_name=__PROJ_NAME__,
            set_dict={
                'b': '开始',
                'c': '查看',
                'l': '登录',
                'r': '重置',
                'u': '更新内容',
            },
            version=__VERSION__,
            location='main',
            eflag=True
        )
        # print('|*===================================================================*|\n'
        #       '|*|                       DANMAKU   READER                          |*|\n'
        #       f'|*|                                              {__VERSION__}    |*|\n'
        #       '|*===================================================================*|\n'
        #       '|*|                                                                 |*|\n'
        #       '|*|      A(a).初始化         B(b).启动         C(c).查看               |*|\n'
        #       '|*|                                                                 |*|\n'
        #       '|*|                                                                 |*|\n'
        #       '|*|      S(s).设置                             E(e):退出             |*|\n'
        #       '|*|                                                                 |*|\n'
        #       '|*===================================================================*|')
        ios.print_details('Tips:如果你想直接修改文件，只需在c.查看中打开对应文件并直接修改，本程序中的所有改动会在重启后生效',
                          tag='CTRL')
        ios.print_details('Tips:作者是搞机器学习的不会写QT，如果想帮助作者或者up，'
                          '欢迎来:https://github.com/MeowDWing/DanmakuReader'
                          '，或者b站私信：吾名喵喵之翼',
                          tag='CTRL')
        ios.print_details('Tips:设置只设置程序行为，如果想更改屏蔽词/最低读取等级等信息，请在c.查看中修改',
                          tag='CTRL')

        print('>>>', end='')
        get = input()
        get = get.strip()

        label = get.upper()
        match label:
            case 'B': interface.MFunc.begin()
            case 'C': interface.MFunc.check()
            case 'L': interface.MFunc.login()
            case 'R': interface.MFunc.reset()
            case 'U': interface.MFunc.updatec()
            case 'S': interface.MFunc.setting()
            case 'E': exit(0)
            case _:
                print(f'{label}没有在列表中')
                time.sleep(2)


if __name__ == '__main__':
    main()
