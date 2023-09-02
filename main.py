import os
import time
import multiprocessing
from multiprocessing.pool import Pool
import reader as rd
import interface
import iosetting as ios
import liveget as lg
import initial


__VERSION__ = 'v2.0-demo-PUSH8'
__PROJ_NAME__ = 'Danmaku  Reader'
__PREFIX = 'Mainc'


def init():

    ios.print_details('执行初始化将重置所有文件，你确定要继续吗(y/n)?', tag='WARNING', end='')
    key = input("").strip().upper()
    if key == 'Y':
        file_clearer('./files')
        if os.path.exists('ban_word.txt'):
            os.remove('ban_word.txt')
        initial.initial()
    else:
        return


def file_clearer(path):
    if os.path.exists(path):
        archive = os.listdir(path)
        for file in archive:
            os.remove(path + f'/{file}')


def begin():

    __global_queue = multiprocessing.Queue(233)
    print('正在读取房间号...')
    rid = 34162
    with open('./files/settings.txt', mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip().split('=')
        if line[0] == 'rid':
            rid = int(line[1])

    print('正在初始化弹幕获取器...')
    process_receiver = multiprocessing.Process(target=receiver, args=(__global_queue, rid,))

    print("正在初始化阅读器...")
    process_reader = multiprocessing.Process(target=reader, args=(__global_queue,))

    print("正在启动弹幕获取器与读取器...")
    process_receiver.start()
    process_reader.start()

    process_receiver.join()
    process_reader.join()


def receiver(_g_queue: multiprocessing.Queue, rid: int = 34162):
    x = lg.LiveInfoGet(rid=rid, g_queue=_g_queue)
    x.living_on()


def reader(_queue):
    read = rd.Reader(_queue)
    read.reader()


def check():
    while True:
        os.system('cls')
        interface.interface(
            proj_name=__PROJ_NAME__,
            location='main -> 查看',
            version=__VERSION__,
            set_dict={
                'b': '禁读词列表',
                's': '设置'
            },
            pflag=True,
            eflag=True
        )
        # print('|*===================================================================*|\n'
        #       '|*|                       DANMAKU   READER                          |*|\n'
        #       f'|*|  main -> 查看                                  {__VERSION__}   |*|\n'
        #       '|*===================================================================*|\n'
        #       '|*|                                                                 |*|\n'
        #       '|*|      B(b).禁读词列表        S(s).设置文件                          |*|\n'
        #       '|*|                                                                 |*|\n'
        #       '|*|                                                                 |*|\n'
        #       '|*|      P(p).返回上一级                         E(e):退出             |*|\n'
        #       '|*|                                                                 |*|\n'
        #       '|*===================================================================*|'
        #       )
        print('>>>', end='')
        get = input()
        get = get.strip()
        label = get[0].upper()
        match label:
            case 'B': os.system('ban_word.txt')
            case 'S':
                cwd = os.getcwd()
                os.chdir(cwd+'/files')
                os.system('settings.txt')
                os.chdir(cwd)
            case 'P': return
            case 'E': exit()
            case _:
                print(f'{label}没有在列表中')


def updatec():
    interface.update_content(__VERSION__)
    input("很好，我知道了！（Enter退出）")


def main():

    f = False
    multiprocessing.freeze_support()
    print('正在检测初始化...')
    initial.initial()
    while True:
        os.system('cls')
        interface.interface(
            proj_name=__PROJ_NAME__,
            set_dict={
                'a': '初始化',
                'b': '开始',
                'c': '查看',
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
        ios.print_details('Tips:作者是搞机器学习的不会写QT不会搞协程，如果想帮助作者或者up，'
                      '欢迎来:https://github.com/MeowDWing/DanmakuReader'
                      '，或者b站私信：吾名喵喵之翼',
                          tag='CTRL')
        ios.print_details('Tips:设置的内容还没做好，建议所有更改现在查看里看',
                          tag='CTRL')

        print('>>>', end='')
        get = input()
        get = get.strip()

        label = get[0].upper()
        match label:
            case 'A': init()
            case 'B': begin()
            case 'C': check()
            case 'U': updatec()
            case 'E': exit(0)
            case _:
                print(f'{label}没有在列表中')
                time.sleep(2)


if __name__ == '__main__':
    main()
