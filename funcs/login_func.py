"""

    登录函数

"""
import urllib.parse
import uuid
import os
import time
from enum import Enum

import bilibili_api
from bilibili_api import login, login_func, exceptions, sync, user
from bilibili_api.credential import Credential
from bilibili_api.login import login_with_password, login_with_sms, send_sms, PhoneNumber

import iosetting as ios
import global_setting


class LoginState(Enum):
    """
        登录状态类
    """
    lack = "未输入账号或密码"
    success = "登陆成功"
    need_qrcode = "请使用二维码登录"
    need_sms = "请使用验证码登录"
    fail = "登陆错误"


class UserInfoParser:
    """ 用户信息解释器 """
    def __init__(self, c: Credential | None = None):
        if c.sessdata is not None:
            try:
                self.info = sync(user.get_self_info(c))
            except Exception as e:
                print(e)
        else:
            self.info = {
                'name': None,
                'mid': None
            }

    def nickname(self):
        return self.info['name']

    def uid(self):
        return self.info['mid']


def login_check(c: Credential) -> (bool, UserInfoParser):
    """
    :return: 登录状态， 用户信息
    """
    success = False
    self_info = None
    try:
        self_info = UserInfoParser(c)
        success = True
    except Exception as e:
        err = e.__str__()

    return success, self_info


def get_buvid3() -> str:
    """
    :return: 临时buvid3
    """
    return str(uuid.uuid1()).lower() + 'infoc'


def login_info_save(c: Credential) -> bool:
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


def login_by_pw(username: str | None = None, password: str | None = None, save=False) -> LoginState:
    """
        账号密码登录
    :param username: 账号， 邮箱或者手机
    :param password: 密码
    :param save: 是否保存
    :return: 登录状态
    """
    check = False
    if username is None or password is None:
        return LoginState.lack

    try:
        c = login_with_password(username, password)
    except exceptions.LoginError as el:
        c = None
        ios.print_details(el.msg, tag='WRONG', head='WRONG', prefix='LOGIN')

    if isinstance(c, login.Check):
        # 还需验证
        c = None
        check = True
    else:
        global_setting.settings.login = True
        global_setting.settings.update_conform_and_dump()

    if save:
        global_setting.INITIAL.pw = password
    else:
        global_setting.INITIAL.id = username
    global_setting.INITIAL.update_and_dump()

    if c is not None:
        if save:
            global_setting.INITIAL.id = username
            global_setting.INITIAL.pw = password
        if c.buvid3 is None:
            c.buvid3 = get_buvid3()
        c.sessdata = urllib.parse.quote(c.sessdata)
        global_setting.INITIAL.credential_consist(c)
        global_setting.INITIAL.update_and_dump()

        login_success, self_info = login_check(c)

        if login_success:
            global_setting.user_info = self_info
            return LoginState.success
        else:
            return LoginState.fail

    else:
        if check:
            return LoginState.need_sms
        else:
            return LoginState.fail


def get_sms_code(phone: str):
    """
        验证码登录->验证码获取
    :param phone: 手机号（仅限国内，不包含港澳台）
    """
    send_sms(PhoneNumber(phone, country="+86"))  # 默认设置地区为中国大陆


def login_by_sms(phone, code) -> LoginState:
    """
        验证码登录
    :param phone: 手机号
    :param code: 验证码
    :return: 登陆状态
    """
    c = login_with_sms(PhoneNumber(phone, country="+86"), code)
    if isinstance(c, login.Check):
        # 还需验证
        c = None
        print("需要进行验证。请考虑使用二维码登录")

    if c is None:
        return LoginState.need_qrcode
    else:
        if c.buvid3 is None:
            c.buvid3 = get_buvid3()
        c.sessdata = urllib.parse.quote(c.sessdata)
        print(c.sessdata)
        global_setting.INITIAL.credential_consist(c)
        global_setting.INITIAL.update_and_dump()

        login_success, self_info = login_check(c)
        if login_success:
            global_setting.user_info = self_info
            return LoginState.success
        else:
            return LoginState.fail


def get_from_web():
    """
        已废弃，正在找时间删除
    """
    os.system('cls')
    ios.print_details('你可以通过以下方式登录：\n'
                      '图文步骤见：https://nemo2011.github.io/bilibili-api/#/get-credential\n'
                      '1.打开网页版bilibili，登录账号，并按F12检查元素\n'
                      '2.在标签栏选择应用（application）-> cookies -> https://xxx.bilibili.com(xxx可为live或www)\n'
                      '3.以文本形式打开files文件夹中的INITIAL，并在对应位置填入名称对应的值\n'
                      '[Tips]截至版本更新时，只需填入sessdate和buvid3即可\n'
                      '4.确保在s.设置里打开自动登录（显示Y即为打开，输入对应字母切换开启/关闭状态）', tag='UP')
    input('好的,我知道了(enter)')
