import multiprocessing
import os
import time
from collections import deque
import random
import bilibili_api

import iosetting as ios
from bilibili_api import live, sync, user, credential


# Exception Zone
class UserInfoError(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class LiveInfoGet:

    def __init__(self, g_queue: multiprocessing.Queue,
                 up_name: str = '资深小狐狸', ctrl_name: str = '吾名喵喵之翼',
                 debug_flag: bool = False, login_flag: bool = False):
        """

        :param g_queue: 全局队列，多进程通信
        :param up_name: up的名字，用于标记弹幕显示颜色，无别的用处
        :param ctrl_name: 控制名，永远都是作者，改变弹幕显示颜色，如果以后有其他贡献者，会做成集合
        :param debug_flag: 是否debug，打包好后没有更改接口，以后会做接口
        :param login_flag: 是否登录标记，用于检测登录
        """

        # parameter initial zone
        self.up_name = up_name
        self.ctrl_name = ctrl_name
        self.debug_flag = debug_flag

        self.__PREFIX = 'Rec'
        if os.path.exists('./files/login') or login_flag:
            sessdate, bili_jct, buvid3, ac_time_value = self.get_credentials()
            self.credentials = credential.Credential(sessdata=sessdate, bili_jct=bili_jct, buvid3=buvid3,
                                                     ac_time_value=ac_time_value)
        else:
            self.credentials = None
        self._queue = g_queue
        self.local_queue = deque()
        self.local_queue_len = len(self.local_queue)

        if not os.path.exists('./files'):
            os.mkdir('./files')

        # dictionary & list initial zone
        self.settings_dict = {}
        self.read_any_lvl = False
        self.get_settings()
        self.room_id = self.settings_dict['rid']
        self.min_lvl = self.settings_dict['min_level']

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

    def get_settings(self):

        self.settings_dict = ios.JsonParser.load('./files/settings.txt')['basic_setting']

        if self.settings_dict['min_level'] == '0':
            self.read_any_lvl = True

    def get_credentials(self):
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
                ios.print_details('danmaku'+str(random.randint(0, 50000))+'='+str(event), debug_flag=True)
            self.danmaku_processing(event)
        ios.print_details('弹幕开启', tag='SYSTEM')

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
            if not self._queue.full():
                if self.local_queue_len != 0:
                    while True:
                        if not self._queue.full() and self.local_queue_len != 0:
                            c = self.local_queue.popleft()
                            self.local_queue_len -= 1
                            self._queue.put(c)
                        else:
                            break
                else:
                    self._queue.put(danmaku_content)
            else:
                self.local_queue.append(danmaku_content)

        match nickname:
            case self.ctrl_name:
                print_flag = 'CTRL'
            case self.up_name:
                print_flag = 'UP'

        # 方案
        # [lvl|nickname]says

        ios.print_simple(f'[{user_fans_lvl}|{nickname}]{danmaku_content}', base=print_flag)
