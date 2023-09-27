
import os
import time
from collections import deque
import random

import global_setting
import iosetting as ios
from bilibili_api import live, sync, credential
from ui import launchwindow
from funcs import login_func


# Exception Zone
class UserInfoError(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class LiveInfoGet:

    def __init__(self, g_queue: deque, ui: launchwindow.Ui_Launch,
                 up_name: str = '资深小狐狸', ctrl_name: str = '吾名喵喵之翼',
                 ):
        """

        :param g_queue: 全局队列，多进程通信
        :param up_name: up的名字，用于标记弹幕显示颜色，无别的用处
        :param ctrl_name: 控制名，永远都是作者，改变弹幕显示颜色，如果以后有其他贡献者，会做成集合
        """
        # 一次性参数区
        need_login = False

        # 基本参数设置区 basic initial zone
        self.up_name = up_name
        self.ctrl_name = ctrl_name

        self.__PREFIX = 'Rec'

        self._queue = g_queue

        self.ui = ui.recivetext

        if not os.path.exists('./files'):
            os.mkdir('./files')

        # 设置信息获取区 settings initial zone
        self.room_id = global_setting.settings['basic_setting']['rid']
        self.min_lvl = global_setting.settings['basic_setting']['min_level']
        self.login_flag = global_setting.settings['sys_setting']['login']
        self.debug_flag = global_setting.settings['sys_setting']['debug']

        if self.min_lvl == 0:
            self.read_any_lvl = True
        else:
            self.read_any_lvl = False

        if not global_setting.offline:
            # 登录信息设置区 login info initial zone
            sessdate, bili_jct, buvid3, ac_time_value = self.get_credentials()

            if sessdate is None and bili_jct is None and buvid3 is None and ac_time_value is None:
                self.credentials = None
                ios.display_details('请检查INITIAL文件确保登录信息正确', tag='WARNING', ui=self.ui)
                time.sleep(3)
            elif sessdate is None and buvid3 is None:
                ios.display_details('关键信息配置有误，请检查sessdate和buvid3信息是否已配置', tag='WARNING', ui=self.ui)
                time.sleep(3)
            elif buvid3 is None:
                buvid3 = login_func.get_buvid3()

            self.credentials = credential.Credential(sessdata=sessdate, bili_jct=bili_jct, buvid3=buvid3,
                                                     ac_time_value=ac_time_value)

            # cookie 刷新与自动登录区 cookie refresh and login Zone
            need_login = not sync(self.credentials.check_valid())

            if self.login_flag and need_login:
                self.credentials = login_func.semi_autologin()
                login_func.login_info_save(self.credentials)
            elif need_login:
                ios.display_simple('登录cookie需要更新，如需登录请重启程序并登录', base='WARNING', ui=self.ui)

        else:  # if offline
            self.credentials = None

        # 房间信息获取区 room info initial zone
        if self.room_id > 0:
            self.room = live.LiveRoom(room_display_id=self.room_id)
            self.room_info = sync(self.room.get_room_info())
            self.user_id = self.room_info['room_info']['uid']
            self.up_name = self.room_info['anchor_info']['base_info']['uname']
            if self.room_info['anchor_info']['medal_info'] is not None:
                self.fans_badge = self.room_info['anchor_info']['medal_info']['medal_name']
            else:
                self.fans_badge = 'NO FANS BADGE'
        else:
            raise UserInfoError("User_id maybe wrong, please check again")

        self.room_event_stream = live.LiveDanmaku(self.room_id, credential=self.credentials)

    @staticmethod
    def get_credentials():
        c_dict = ios.JsonParser.load('./files/INITIAL')

        s = c_dict['sessdate']
        b = c_dict['bili_jct']
        b3 = c_dict['buvid3']
        a = c_dict['ac_time_value']

        return s, b, b3, a

    def living_on(self):

        @self.room_event_stream.on('DANMU_MSG')
        async def on_danmaku(event):  # event -> dictionary
            if self.debug_flag:
                ios.logging_simple(filename='./logging.txt', txt='danmaku'+str(random.randint(0, 50000))+'='+str(event))
            self.danmaku_processing(event)
        ios.display_details('弹幕开启', tag='SYSTEM', ui=self.ui)

        sync(self.room_event_stream.connect())

    def danmaku_processing(self, event: dict = None):

        user_fans_lvl = 0
        print_flag = 'NORMAL'
        if_read = False

        # main information processing Zone
        live_info = event['data']['info']  # list[Unknown, Msg, user_info, fans_info, Unknown:]
        danmaku_content = live_info[1]
        user_main_info = live_info[2]  # list[uid, Nickname, Unknown:]
        nickname = user_main_info[1]
        user_fans_info = live_info[3]  # list[lvl, worn_badge, Unknown:]

        if len(user_fans_info) > 0:
            if user_fans_info[1] == self.fans_badge:
                print_flag = 'FANS'
                user_fans_lvl = user_fans_info[0]
                if user_fans_lvl > 19:
                    print_flag = 'CAPTAIN'
                if user_fans_lvl >= self.min_lvl:
                    if_read = True

        if len(danmaku_content) > 0 and (self.read_any_lvl or if_read):
            self._queue.append(danmaku_content)

        match nickname:
            case self.ctrl_name:
                print_flag = 'CTRL'
            case self.up_name:
                print_flag = 'UP'

        # 方案
        # [lvl|nickname]says
        # display_content = ios.display_details(f"[{user_fans_lvl}|{nickname}]{danmaku_content}")
        ios.display_details(f"[{user_fans_lvl}|{nickname}]{danmaku_content}", tag=print_flag, ui=self.ui)