import uuid
import os
import time

from bilibili_api import login, login_func, exceptions
from bilibili_api.credential import Credential
from bilibili_api.login import login_with_password, login_with_sms, send_sms, PhoneNumber

import iosetting as ios
import global_setting

def get_buvid3() -> str:
    """
    :return: 临时buvid3
    """
    return str(uuid.uuid1()).lower() + 'infoc'


class LoginFunc:

    @staticmethod
    def login_by_pw(username: str | None = None, password: str | None = None, from_sys=False):
        if from_sys:
            print('系统登录')
        else:
            username = input("请输入手机号/邮箱：")
            password = input("请输入密码：")
            print("正在登录。")
        try:
            c = login_with_password(username, password)
        except exceptions.LoginError as el:
            c = None
            ios.print_details(el.msg, tag='WRONG', head='WRONG', prefix='LOGIN')
            time.sleep(1)
            return c, 'False', 'False'
        if isinstance(c, login.Check):
            # 还需验证
            print("需要进行验证。请考虑使用验证码登录")
            return None, username, password
        else:
            credential = c
            global_setting.settings['sys_setting']['login'] = True
            global_setting.update_setting()
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

    @staticmethod
    def semi_autologin(in_run: bool = False):
        login_info = ios.JsonParser.load('./files/INITIAL')
        username = login_info['id']
        pw = login_info['pw']
        if username is not None and pw is not None:
            credentials, _, _ = LoginFunc.login_by_pw(username=username, password=pw, from_sys=True)
        else:
            credentials = None

        if credentials is None:
            ios.print_details('自动登录失败，请尝试手动登录', tag='SYSTEM', head='ERROR')
            time.sleep(3)
            if in_run:
                exit()
            else:
                return credentials  # None
        else:
            return credentials

    @staticmethod
    def get_from_web():
        os.system('cls')
        ios.print_details('你可以通过以下方式登录：\n'
                          '图文步骤见：https://nemo2011.github.io/bilibili-api/#/get-credential\n'
                          '1.打开网页版bilibili，登录账号，并按F12检查元素\n'
                          '2.在标签栏选择应用（application）-> cookies -> https://xxx.bilibili.com(xxx可为live或www)\n'
                          '3.以文本形式打开files文件夹中的INITIAL，并在对应位置填入名称对应的值\n'
                          '[Tips]截至版本更新时，只需填入sessdate和buvid3即可\n'
                          '4.确保在s.设置里打开自动登录（显示Y即为打开，输入对应字母切换开启/关闭状态）', tag='UP')
        input('好的,我知道了(enter)')

    @staticmethod
    def save_credentials(c: Credential | None = None) -> bool:
        if c is None:
            return False
        else:
            cdict = ios.JsonParser.load('./files/INITIAL')
            cdict['sessdate'] = c.sessdata
            cdict['bili_jct'] = c.bili_jct
            cdict['buvid3'] = c.buvid3
            cdict['ac_time_value'] = c.ac_time_value
            ios.JsonParser.dump('./files/INITIAL', cdict, mode='w')
            return True
