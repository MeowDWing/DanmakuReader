"""

    弹幕的接收部分，由于界面里显示部分删了，所以很多变量已经没有实际用处了
    不过考虑到之后会做新的弹幕界面，所以先保留着，据作者毫无根据的想象，这些应该占不了多少性能

"""
import random
from collections import deque

import global_setting
from bilibili_api import live, sync, credential


# Exception Zone
class UserInfoError(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class LiveInfoGet:

    def __init__(self, g_queue: deque,
                 up_name: str = '资深小狐狸', ctrl_name: str = '吾名喵喵之翼',
                 ):
        """

        :param g_queue: 全局队列，多进程通信
        :param up_name: up的名字，用于标记弹幕显示颜色，无别的用处
        :param ctrl_name: 控制名，永远都是作者，改变弹幕显示颜色，如果以后有其他贡献者，会做成集合
        """
        # 基本参数设置区 basic initial zone
        self.up_name = up_name
        self.ctrl_name = ctrl_name

        self._queue = g_queue

        # 设置信息获取区 settings initial zone
        self.room_id = global_setting.settings.rid
        self.min_lvl = global_setting.settings.min_lvl
        self.login_flag = global_setting.settings.login
        self.debug_flag = global_setting.settings.debug

        if self.min_lvl == 0:
            self.read_any_lvl = True
        else:
            self.read_any_lvl = False

        # 登录信息设置区 login info initial zone
        self.credentials = global_setting.credential

        sessdata = self.credentials.sessdata
        bili_jct = self.credentials.bili_jct
        buvid3 = self.credentials.buvid3
        ac_time_value = self.credentials.ac_time_value

        if sessdata is None and bili_jct is None and buvid3 is None and ac_time_value is None:
            self.credentials = credential.Credential()
            # ios.display_details('请检查INITIAL文件确保登录信息正确', tag='WARNING', ui=self.ui)
        elif sessdata is None and buvid3 is None:
            self.credentials = credential.Credential()
            # ios.display_details('关键信息配置有误，请检查sessdata和buvid3信息是否已配置', tag='WARNING', ui=self.ui)
        else:
            raise UserInfoError('UserInfoError:出现了不应该出现的错误，请发送logging文件给作者处理,位置:live get-credentials检测')


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

    def living_on(self):

        @self.room_event_stream.on('DANMU_MSG')
        async def on_danmaku(event):  # event -> dictionary
            self.danmaku_processing(event)

        sync(self.room_event_stream.connect())

    def danmaku_processing(self, event: dict = None):

        user_fans_lvl = 0
        print_flag = 'NORMAL'
        if_read = False

        if self.debug_flag:
            r = random.randrange(0,100,1)
            if r > 94:
                with open('./logging/sample_danmaku.txt', 'a') as f:
                    f.write(str(event))

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
        # ios.display_details(f"[{user_fans_lvl}|{nickname}]{danmaku_content}", tag=print_flag, ui=self.ui)