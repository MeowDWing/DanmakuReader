"""

    全局变量

"""
from bilibili_api import Credential

import iosetting as ios
from funcs import file_func, login_func

# 版本控制
version = 'v1.1-alpha'
proj_name = 'Danmaku Reader'

"""全局变量"""
settings: file_func.SettingsParser | None = None  # 设置
INITIAL: file_func.InitialParser | None = None  # INITIAL文件解释器
user_info: login_func.UserInfoParser | None = None  # 登陆用户信息解释器
offline = False  # 是否离线登录标记，后续优化如settings
credential: str | None | Credential = None  # 登陆证书


def load_setting():

    global settings, INITIAL, user_info, credential

    settings = file_func.SettingsParser()
    INITIAL = file_func.InitialParser()

    credential = INITIAL.get_credential()
    if credential is not None:
        user_info = login_func.UserInfoParser(credential)

