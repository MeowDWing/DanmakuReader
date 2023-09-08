import time
import uuid
import bilibili_api

import iosetting as ios
import os
import re
import main
import multiprocessing
import initial
import liveget as lg
import reader as rd
from bilibili_api.login import login_with_password, login_with_sms, send_sms, PhoneNumber
from bilibili_api import login, sync, settings, exceptions
from bilibili_api.credential import Credential


def interface(proj_name: str, set_dict: dict, version: str, location: str, pflag: bool = False, eflag: bool = False):

    # 设置区
    items = len(set_dict.keys())
    line_int = int(items/3)
    line_rest = items % 3
    set_lines = []
    for key, value in set_dict.items():
        set_lines.append(f'{key.upper()}({key}).{value}')

    llen = len(set_lines)
    cpj_n = characters_num(proj_name)
    cver_n = characters_num(version)
    cloc_n = characters_num(location)

    # 显示区
    print(f"|*{'=' * 76}*|")
    print(f"|*|{proj_name.center(74-cpj_n)}|*|")
    print(f"|*|    {location.ljust(33-cloc_n)}{version.rjust(33-cver_n)}    |*|")
    print(f"|*{'=' * 76}*|")
    print(f"|*|{' ' * 74}|*|")

    tmp = 0
    if line_int != 0:
        for i in range(line_int):
            l1 = characters_num(set_lines[tmp])
            l2 = characters_num(set_lines[tmp+1])
            l3 = characters_num(set_lines[tmp+2])
            print(f"|*|        "
                  f"{set_lines[tmp].ljust(22-l1)}"
                  f"{set_lines[tmp+1].ljust(22-l2)}"
                  f"{set_lines[tmp+2].ljust(22-l3)}"
                  f"|*|")
            print(f"|*|{' ' * 74}|*|")
            tmp += 3
    if line_rest != 0:
        if line_rest == 1:
            print(f"|*|        {set_lines[tmp].ljust(66-characters_num(set_lines[tmp]))}|*|")
        else:
            ll2 = characters_num(set_lines[tmp])
            ll1 = characters_num(set_lines[tmp+1])
            print(f"|*|        "
                  f"{set_lines[tmp].ljust(22 - ll2)}"
                  f"{set_lines[tmp+1].ljust(44 - ll1)}"
                  f"|*|")
    print(f"|*|{' ' * 74}|*|")
    if eflag:
        if location == 'main':
            print(f"|*|        {'S(s).设置'.ljust(44-2)}{'E(e).退出'.ljust(22-2)}|*|")
            print(f"|*|{' ' * 74}|*|")
        elif pflag:
            print(f"|*|        {'P(p).上一级'.ljust(44-3)}{'E(e).退出'.ljust(22-2)}|*|")
            print(f"|*|{' ' * 74}|*|")
    print(f"|*{'=' * 76}*|")

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


def characters_num(rev: str) -> int:
    _m = re.findall("\\\\x[0-9a-f][0-9a-f]", str(rev.encode('utf-8')))
    _l = len(_m)
    return int(_l/3)


def update_content(version: str):
    with open(f'{version}.md', mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        ios.print_details(line, tag='CTRL')


class MFunc:

    @staticmethod
    def reset():

        ios.print_details('执行指令将重置所有文件（如屏蔽词，登录信息等），你确定要继续吗(y/n)?', tag='WARNING', end='')
        key = input("").strip().upper()
        if key == 'Y':
            file_clearer('./files')
            if os.path.exists('ban_word.txt'):
                os.remove('ban_word.txt')
            initial.initial()
        else:
            return

    @staticmethod
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

    @staticmethod
    def check():
        while True:
            os.system('cls')
            interface(
                proj_name=main.__PROJ_NAME__,
                location='main -> 查看',
                version=main.__VERSION__,
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
                case 'B':
                    os.system('ban_word.txt')
                case 'S':
                    cwd = os.getcwd()
                    os.chdir(cwd + '/files')
                    os.system('settings.txt')
                    os.chdir(cwd)
                case 'P':
                    return
                case 'E':
                    exit()
                case _:
                    print(f'{label}没有在列表中')

    @staticmethod
    def login():
        credentials: Credential = Credential()
        sign = pw = 'False'
        settings.geetest_auto_open = True
        while True:
            os.system('cls')
            interface(
                proj_name=main.__PROJ_NAME__,
                version=main.__VERSION__,
                location='main->登录',
                set_dict={
                    'a': '验证码',
                    'b': '账号密码',
                    'c': '二维码'
                },
                pflag=True, eflag=True,
            )
            ios.print_details('选择账号密码登陆后，即自动保存至本地，几天内即无需再次登录，之后若无法使用，请再次登录', tag='TIPS', head='TIPS')
            ios.print_details('本程序所有输入与保存均为明文形式，切勿泄露，并在确保网络安全的情况下（私人或可信的公共网络下）使用', tag='UP', head='TIPS')
            get = input('>>>').strip().upper()
            match get:
                case 'A': credentials = LoginFunc.login_by_sms()
                case 'B': credentials, sign, pw = LoginFunc.login_by_pw()
                case 'C': credentials = LoginFunc.qrcode()
                case 'P': return
                case 'E': exit(0)

            if credentials is not None:
                if sign != 'False' and pw != 'False':
                    with open('./files/INITIAL', mode='w', encoding='utf-8') as f:
                        credentials.generate_buvid3()
                        lines = [
                            '本文件行对应，请勿以任何方式更改本文件\n',
                            f'sign={sign}\n',
                            f'pw={pw}\n',
                            f'sessdate={credentials.sessdata}\n',
                            f'bili_jct={credentials.bili_jct}\n',
                            f'buvid3={credentials.buvid3}\n',
                            f'ac_time_value={credentials.ac_time_value}\n'
                        ]
                        f.writelines(lines)
                    ios.print_simple(f'sessdate:...{credentials.sessdata[-6:]}\n'
                                     f'bili_jct:...{credentials.bili_jct[-6:]}\n'
                                     f'buvid3:...{credentials.buvid3[-6:]}\n'
                                     f'ac_time_value:...{credentials.ac_time_value[-6:]}\n'
                                     '如果上述内容中出现规则内容或者buvid3中没有infoc字样，请重新登陆', base='CTRL')
                    ios.print_simple('保存完毕', base='CTRL')
                    time.sleep(5)
                    return

                else:
                    with open('./files/INITIAL', mode='r', encoding='utf-8') as f:
                        lines = f.readlines()
                        if len(lines) > 0:
                            if len(lines[1]) > 7 and len(lines[2]) > 5:
                                sign = lines[1][5:-1]
                                pw = lines[2][3:-1]
                            else:
                                sign = ''
                                pw = ''

                    with open('./files/INITIAL', mode='w', encoding='utf-8') as f:
                        credentials.generate_buvid3()
                        lines = [
                            '本文件行对应，除非理解程序逻辑，否则请勿以任何方式更改本文件\n',
                            f'sign={sign}\n',
                            f'pw={pw}\n',
                            f'sessdate={credentials.sessdata}\n',
                            f'bili_jct={credentials.bili_jct}\n',
                            f'buvid3={credentials.buvid3}\n',
                            f'ac_time_value={credentials.ac_time_value}\n'
                        ]
                        f.writelines(lines)
                    ios.print_simple(f'sessdate:...{credentials.sessdata[-6:]}\n'
                                     f'bili_jct:...{credentials.bili_jct[-6:]}\n'
                                     f'buvid3:...{credentials.buvid3[-6:]}\n'
                                     f'ac_time_value:...{credentials.ac_time_value[-6:]}\n'
                                     '如果上述内容中出现规则内容或者buvid3中没有infoc字样，请重新登陆', base='CTRL')
                    ios.print_simple('保存完毕', base='CTRL')
                    time.sleep(5)

    @staticmethod
    def updatec():
        update_content(main.__VERSION__)
        input("很好，我知道了！（Enter退出）")

    @staticmethod
    def setting():

        if os.path.exists('./files/login'):
            login_flag = 'Y'
        else:
            login_flag = 'N'

        while True:
            os.system('cls')
            interface(
                proj_name=main.__PROJ_NAME__,
                version=main.__VERSION__,
                location='main->设置',
                set_dict={
                    'a': f'自动登录 {login_flag}',
                },
                eflag=True, pflag=True
            )

            get = input('>>>').strip().upper()
            match get:
                case 'A': login_flag = SetFunc.auto_login(login_flag)
                case 'P': return
                case 'E': exit()


class LoginFunc:

    @staticmethod
    def login_by_pw():
        username = input("请输入手机号/邮箱：")
        password = input("请输入密码：")
        print("正在登录。")
        try:
            c = login_with_password(username, password)
        except exceptions.LoginError as el:
            c = None
            ios.print_details(el.msg, tag='WRONG', head='WRONG', prefix='LOGIN')
            time.sleep(1)
            return None, 'False', 'False'
        if isinstance(c, login.Check):
            # 还需验证
            print("需要进行验证。请考虑使用验证码登录")
            return None, username, password
        else:
            credential = c
            with open('./files/login', mode='w'):
                pass
            return credential, username, password

    @staticmethod
    def login_by_sms():
        phone = input("请输入手机号：")
        print("正在登录。")
        send_sms(PhoneNumber(phone, country="+86"))  # 默认设置地区为中国大陆
        code = input("请输入验证码：")
        c = login_with_sms(PhoneNumber(phone, country="+86"), code)
        if isinstance(c, login.Check):
            # 还需验证
            print("需要进行验证。请考虑使用二维码登录")
            return None
        else:
            credential = c
            return credential

    @staticmethod
    def qrcode():
        print("请登录：")
        credential = login.login_with_qrcode_term()  # 在终端扫描二维码登录
        # credential = login.login_with_qrcode() # 使用窗口显示二维码登录
        try:
            credential.raise_for_no_bili_jct()  # 判断是否成功
            credential.raise_for_no_sessdata()  # 判断是否成功
            return credential
        except:
            print("登陆失败。。。")
            time.sleep(3)
            return None




class SetFunc:
    @staticmethod
    def auto_login(login_flag):
        if login_flag == 'Y':
            login_flag = 'N'
            pathnow = os.getcwd()
            os.remove('files/login')
        else:
            with open('./files/login', mode='w'):
                login_flag = 'Y'

        return login_flag



def receiver(_g_queue: multiprocessing.Queue, rid: int = 34162):
    x = lg.LiveInfoGet(rid=rid, g_queue=_g_queue)
    x.living_on()


def reader(_queue):
    read = rd.Reader(_queue)
    read.reader()


def file_clearer(path):
    if os.path.exists(path):
        archive = os.listdir(path)
        for file in archive:
            os.remove(path + f'/{file}')


if __name__ == '__main__':
    interface(
        proj_name='DanmakuReader',
        version=main.__VERSION__,
        set_dict={
            'a': '初始化',
            'b': '启动',
            'c': '查看',
            'd': '22',
            'e': '33'
        },
        location='查看',
        eflag=True,
        pflag=True
    )

