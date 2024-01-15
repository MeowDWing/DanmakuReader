import re
import time
import random
from collections import deque

from bilibili_api import live, sync

import global_setting
import iosetting as ios
from ui import launchwindow


class Reader:

    def __init__(self, global_queue: deque, _ui: launchwindow):
        self.danmaku_queue = deque()
        self.danmaku_len = 0
        self.tmp = 0
        self._queue = global_queue
        self.ui = _ui
        self.__PREFIX = 'Reader'

        self.force_chasing_10 = 0  # 20
        self.force_chasing_20 = 0  # 15
        self.force_chasing_30 = 0  # 10
        self.force_chasing_40 = 0  # 5
        self.force_reset_limit = 50

        ban_word_set, self.re_ban_str = global_setting.ban_word.ban_list_creator()
        self.ban_word_set = set("1234567890")
        self.ban_word_set.update(ban_word_set)


        self.search_common_symbol = re.compile("[^?？.。,，（）()]").search
        # self.ui.append(f"<font color=cyan>本项目基于bilibili_api， 如有任何需要，请联系作者</font>"
        #                "<p></p>")

        self.player = global_setting.narrator

    def reader(self) -> None:

        """

            hint : 加入读取礼物，舰长等信息后，会启用竞争队列模式，新的高亮优先读取
        :return:
        """

        former = ''
        time.sleep(5)
        while True:

            if self.tmp > 50:
                self.tmp = 0

            # 队列加入与预处理机制
            if self.danmaku_len < 50:
                '''
                    这里在取值时，我们保证只有这里在取值并且判断了队列大于0，所以取值是不会取到不存在的地址的，
                    所以认为这里线程安全是合理的。
                '''
                while len(self._queue) > 0:
                    c: str = self._queue.popleft()
                    c = c.strip()
                    re_flag = re.search(self.re_ban_str, c)

                    if re_flag is None:
                        if c not in self.ban_word_set:
                            if self.search_common_symbol(c):
                                self.danmaku_queue.append(c)
                                self.danmaku_len += 1
                    else:
                        pass

                '''
                    当弹幕量大于60时会清空队列，而大于50时会自动删掉10个弹幕，所以弹幕队列的长度在绝大部分时间是必定小于50的，
                    暂停判断放在这里也是合理的
                '''
                if global_setting.read_pause:
                    self._queue.clear()
                    self.danmaku_queue.clear()
                    self.danmaku_len = 0

            # 追赶机制实现
            self.chasing_scheme()
            # 界面显示剩余弹幕量
            self.ui.rest_quantity.setText(f'{self.danmaku_len}')

            # 处理与读取机制
            if self.danmaku_len != 0:
                now = self.danmaku_queue.popleft()
                if now == former:
                    self.danmaku_len -= 1
                else:
                    self.player.txt2audio(now)
                    self.danmaku_len -= 1
                    former = now

            else:
                # 队列为0时等待3s累计弹幕
                time.sleep(3)

            if int(time.time()) % 100 == 0:
                self.danmaku_len = len(self.danmaku_queue)

    def chasing_scheme(self):
        self.tmp += 1
        # 追赶机制
        if self.danmaku_len > self.force_reset_limit:
            self.danmaku_queue.clear()
            self.danmaku_len = 0

        elif self.danmaku_len > 40:
            self.tmp = 0
            self.popleft_n(4)
            self.force_chasing_40 += 1
            if self.force_chasing_40 > 5:
                self.force_chasing_40 = 0
                self.popleft_n(10)
        elif self.danmaku_len > 30:
            self.tmp = 0
            self.popleft_n(3)
            self.force_chasing_30 += 1
            if self.force_chasing_30 > 10:
                self.force_chasing_30 = 0
                self.popleft_n(10)
        elif self.danmaku_len > 20:
            self.tmp = 0
            self.popleft_n(2)
            self.force_chasing_20 += 1
            if self.force_chasing_20 > 15:
                self.force_chasing_20 = 0
                self.popleft_n(10)

        elif self.danmaku_len > 10:
            self.tmp = 0
            self.popleft_n(1)
            self.force_chasing_10 += 1
            if self.force_chasing_10 > 20:
                self.force_chasing_10 = 0
                self.popleft_n(5)

        elif self.danmaku_len > 5 and self.tmp % 3 == 0:
            self.tmp = 0
            self.popleft_n(1)

    def popleft_n(self, n) -> None:
        """
            从队列中去除 n个值
        :param n:
        :return:
        """
        for _ in range(n):
            self.danmaku_queue.popleft()
        self.danmaku_len = len(self.danmaku_queue)


class DanmakuCounterAndHandler:
    pass

class EventProcessor:

    def __init__(self, danmu:deque, gift:deque, others:deque, to_thread_reader:deque):
        # 队列获取
        self.danmu = danmu
        self.gift = gift
        self.others = others

        self.to_thread_read = to_thread_reader

        # 设置信息获取区 settings initial zone
        #     |
         #    -----> 弹幕处理需求获取
        self.room_id = global_setting.settings.rid
        self.min_lvl = global_setting.settings.min_lvl
        self.debug_flag = global_setting.settings.debug

        if self.min_lvl == 0:
            self.read_any_lvl = True
        else:
            self.read_any_lvl = False


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
            raise Exception("User_id maybe wrong, please check again")

    def processor(self):
        counter = range(8)
        while True:
            # 每处理8个弹幕检查一次礼物队列
            for _ in counter:
                if len(self.danmu)<1:
                    break


            if len(self.gift)>0:
                pass

    def danmaku_processor(self, event):
        user_fans_lvl = 0
        print_flag = 'NORMAL'
        if_read = False

        if self.debug_flag:
            r = random.randrange(0, 100, 1)
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
            self.to_thread_read.append(danmaku_content)

        match nickname:
            case self.up_name:
                print_flag = 'UP'

        ios.print_for_log(f'[{user_fans_lvl}|{nickname}]{danmaku_content}', tag=print_flag)
        # 方案
        # [lvl|nickname]says
        # display_content = ios.display_details(f"[{user_fans_lvl}|{nickname}]{danmaku_content}")
        # ios.display_details(f"[{user_fans_lvl}|{nickname}]{danmaku_content}", tag=print_flag, ui=self.ui)


if __name__ == '__main__':
    pass
