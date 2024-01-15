"""

    弹幕的接收部分，由于界面里显示部分删了，所以很多变量已经没有实际用处了
    不过考虑到之后会做新的弹幕界面，所以先保留着，据作者毫无根据的想象，这些应该占不了多少性能

"""
import random
from collections import deque

from bilibili_api import live, sync, credential

import global_setting
import iosetting as ios


# Exception Zone
class UserInfoError(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class ReceiveAndDistribution:
    """

        弹幕接收与分发线程，追踪所有事件，分发到指定队列

    """

    def __init__(self, danmaku: deque, gift: deque, others:deque,
                 ctrl_name: str = '吾名喵喵之翼',
                 ):
        """


        :param ctrl_name: 控制名，永远都是作者，改变弹幕显示颜色，如果以后有其他贡献者，会做成集合
        """
        # 基本参数设置区 basic initial zone
        self.ctrl_name = ctrl_name

        self.danmu_queue = danmaku
        self.gift_queue = gift
        self.others_queue = others

        # 设置信息获取区 settings initial zone
        self.room_id = global_setting.settings.rid

        # 登录信息设置区 login info initial zone
        self.credentials: credential = global_setting.credential

        sessdata = self.credentials.sessdata
        bili_jct = self.credentials.bili_jct
        buvid3 = self.credentials.buvid3
        ac_time_value = self.credentials.ac_time_value

        if sessdata is None or bili_jct is None or ac_time_value is None:
            raise UserInfoError('UserInfoError:出现了不应该出现的错误，请发送logging文件给作者处理,位置:live get-credentials检测')
        elif buvid3 is None:
            self.credentials.buvid3 = global_setting.INITIAL.get_buvid3()
        else:
            pass


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
        """
        Events：
        + DANMU_MSG: 用户发送弹幕
        + SEND_GIFT: 礼物
        + COMBO_SEND：礼物连击
        + GUARD_BUY：续费大航海
        + SUPER_CHAT_MESSAGE：醒目留言（SC）
        + SUPER_CHAT_MESSAGE_JPN：醒目留言（带日语翻译？）
        + WELCOME: 老爷进入房间
        + WELCOME_GUARD: 房管进入房间
        + NOTICE_MSG: 系统通知（全频道广播之类的）
        + PREPARING: 直播准备中
        + LIVE: 直播开始
        + ROOM_REAL_TIME_MESSAGE_UPDATE: 粉丝数等更新
        + ENTRY_EFFECT: 进场特效
        + ROOM_RANK: 房间排名更新
        + INTERACT_WORD: 用户进入直播间
        + ACTIVITY_BANNER_UPDATE_V2: 好像是房间名旁边那个
        xx
        小时榜
        + == == == == == == == == == == == == == =
        + bilibili api 自定义事件：
        + == == == == == == == == == == == == ==
        + VIEW: 直播间人气更新
        + ALL: 所有事件
        + DISCONNECT: 断开连接（传入连接状态码参数）
        + TIMEOUT: 心跳响应超时
        + VERIFICATION_SUCCESSFUL: 认证成功
        """

        @self.room_event_stream.on('ALL')
        async def event_monitor(event):  # event -> dictionary
            self.event_distribution(event)

        sync(self.room_event_stream.connect())

    def event_distribution(self, event: dict = None):
        ctrl_type = event['type']
        match ctrl_type:
            case 'DANMU_MSG': self.danmu_queue.append(event['data'])
            case 'SEND_GIFT': self.gift_queue.append(event['data'])
            case 'SUPER_CHAT_MESSAGE': self.gift_queue.append(event['data'])
            case 'GUARD_BUY': self.gift_queue.append(event['data'])
            case _: self.others_queue.append(event['data'])


