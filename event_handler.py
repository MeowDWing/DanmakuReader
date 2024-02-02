import re
import time
import random
from collections import deque
from enum import Enum

from bilibili_api import live, sync

import global_setting
import iosetting as ios
from ui import launchwindow

class MessageType(Enum):
    DANMU = 0
    WEALTHY_GIFT = 1
    SC = 2
    CAPTAIN_BUY = 4


class Counter:
    """

        弹幕计数器

    """
    def __init__(self):
        # [danmaku content] : DanmakuCountNode
        self.count = dict()
        self.common_preserve = [('initial', 0)]
        self.common_preserve_min_len = 0

    def append(self, danmaku_content):
        t = int(time.time())

        if danmaku_content in self.count.keys():
            q: deque = self.count[danmaku_content]
            q.append(t)
        else:
            q = deque()
            q.append(t)
            self.count[danmaku_content] = q

        self.update_maintain(q)
        flag = True
        for i in range(len(self.common_preserve)):
            if self.common_preserve[i][0] == danmaku_content:
                tup = self.common_preserve[i]
                self.common_preserve[i] = (danmaku_content, tup[1]+1)
                flag = False

        if flag and (l:=len(q))>self.common_preserve_min_len:
            self.common_preserve.append((danmaku_content,l))

    def common_maintain(self):
        temp_cp = [] # temp common preserve list
        for tup in self.common_preserve:
            if tup[0] in self.count.keys():
                self.update_maintain(self.count[tup[0]])
                l = len(self.count[tup[0]])
                temp_cp.append((tup[0],l))
            else:
                pass

        new_cp = sorted(temp_cp,key=lambda x:x[1],reverse=True)
        if len(new_cp) > 10:
            self.common_preserve = new_cp[0:10]
        else:
            self.common_preserve = new_cp

        if len(self.common_preserve)<10:
            self.common_preserve_min_len = 0
        else:
            self.common_preserve_min_len = new_cp[-1][1]

    def update_maintain(self, q: deque):
        self.cut(q, int(time.time())-600)


    def absolutely_maintain(self):
        for key in self.count.keys():
            self.update_maintain(self.count[key])
            if (l := len(self.count[key]))>self.common_preserve_min_len:
                self.common_preserve.append((self.count[key],l))

        new_cp = sorted(self.common_preserve, key=lambda x: x[1], reverse=True)
        if len(new_cp) > 10:
            self.common_preserve = new_cp[0:10]
        else:
            pass

        if len(self.common_preserve)<10:
            self.common_preserve_min_len = 0
        else:
            self.common_preserve_min_len = self.common_preserve[-1][1]

    @staticmethod
    def cut(queue: deque, threshold_t: int):
        if len(queue) < 1:
            return
        while True:
            create_t = queue.popleft()
            if create_t > threshold_t:
                queue.appendleft(create_t)
                break
            elif len(queue) < 1:
                break
            else:
                pass
        return


class Reader:

    def __init__(self, preprocessing_queue: deque, _ui: launchwindow):
        self.danmaku_queue = deque()
        self.danmaku_len = 0
        self.tmp = 0
        self._queue = preprocessing_queue
        self.ui = _ui
        self.__PREFIX = 'Reader'

        self.base_queue = deque()
        self.priority_queue = deque()

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
                    msg: tuple = self._queue.popleft()
                    if msg[0]>0:
                        self.priority_queue.append(msg)
                        continue
                    else:
                        c = msg[1].strip()
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

            # 优先队列处理
            while len(self.priority_queue)>0:
                msg: tuple = self.priority_queue.popleft()
                c = msg[1]
                self.player.txt2audio(c)

            else:

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
    """

        弹幕计数器与计数处理器

    """
    def __init__(self, from_danmu_processor:deque, ui: launchwindow):
        self.counter = Counter()
        self.danmu = from_danmu_processor

        self._ui:launchwindow.Ui_Launch = ui

    def count(self):
        """
            每120秒做常规维护，每15次常规维护做全弹幕维护，每次弹幕加入做对应弹幕维护
            每录入10个弹幕做一次界面更新
        :return:
        """
        common_maintain_timer = 120
        absolutely_maintain_counter = 15
        last_maintain = int(time.time())
        i = 10

        while True:
            t = int(time.time())
            while i > 1:
                if len(self.danmu)>0:
                    i -= 1
                    danmaku_content = self.danmu.popleft()
                    self.counter.append(danmaku_content)
                else:
                    time.sleep(3)

            if t-last_maintain > common_maintain_timer:
                if absolutely_maintain_counter > 1:
                    self.counter.common_maintain()
                    absolutely_maintain_counter -= 1
                else:
                    self.counter.absolutely_maintain()
                    absolutely_maintain_counter = 15

            self.update()
            i = 10

    def update(self):
        """
            ui更新

        :return:
        """
        if global_setting.settings.debug: print(self.counter.common_preserve)
        self.counter.common_preserve.sort(key=lambda x:x[1], reverse=True)

        if len(self.counter.common_preserve)>10:
            self.counter.common_preserve = self.counter.common_preserve[0:10]
            self.counter.common_preserve_min_len = self.counter.common_preserve[-1][1]

        tips = ''
        cp = self.counter.common_preserve
        for i in range(len(cp)):
            tips = tips + f'{i+1}:{cp[i][0]} - {cp[i][1]}\n'

        first = f'{cp[0][0]}'
        self._ui.major_danmaku_content.setText(first)
        self._ui.major_danmaku_content.setToolTip(tips)



class EventProcessor:

    def __init__(self, danmu:deque, gift:deque, others:deque, to_thread_reader:deque, to_counter:deque):
        # 队列获取
        self.danmu = danmu
        self.gift = gift
        self.others = others

        self.to_counter = to_counter
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
                else:
                    event = self.danmu.popleft()
                    self.danmaku_processor(event)

            if len(self.gift)>0:
                while True:
                    if len(self.gift)<1:
                        break
                    else:
                        event = self.gift.popleft()
                        self.gift_processor(event)

    def danmaku_processor(self, event):

        cmd = event['cmd']
        match cmd:
            case 'DANMU_MSG': self.single_danmaku_processor(event)
            case 'DM_INTERACTION': self.multi_danmaku_processor(event)

    def single_danmaku_processor(self, event):
        user_fans_lvl = 0
        print_flag = 'NORMAL'
        if_read = False

        if self.debug_flag:
            r = random.randrange(0, 100, 1)
            if r > 94:
                with open('./logging/sample_danmaku.txt', 'a') as f:
                    f.write(str(event))

        # main information processing Zone
        live_info = event['info']  # list[Unknown, Msg, user_info, fans_info, Unknown:]
        danmaku_content = live_info[1]
        user_main_info = live_info[2]  # list[uid, Nickname, Unknown:]
        nickname = user_main_info[1]
        user_fans_info = live_info[3]  # list[lvl, worn_badge, Unknown:]

        self.to_counter.append(danmaku_content)

        if len(user_fans_info) > 0:
            if user_fans_info[1] == self.fans_badge:
                print_flag = 'FANS'
                user_fans_lvl = user_fans_info[0]
                if user_fans_lvl > 19:
                    print_flag = 'CAPTAIN'
                if user_fans_lvl >= self.min_lvl:
                    if_read = True

        if len(danmaku_content) > 0 and (self.read_any_lvl or if_read):
            package = (0,danmaku_content) #(类型， 内容)
            self.to_thread_read.append(package)

        match nickname:
            case self.up_name:
                print_flag = 'UP'

        ios.print_for_log(f'[{user_fans_lvl}|{nickname}]{danmaku_content}', tag=print_flag)
        # 方案
        # [lvl|nickname]says
        # display_content = ios.display_details(f"[{user_fans_lvl}|{nickname}]{danmaku_content}")
        # ios.display_details(f"[{user_fans_lvl}|{nickname}]{danmaku_content}", tag=print_flag, ui=self.ui)

    def multi_danmaku_processor(self, event):

        if self.debug_flag:
            r = random.randrange(0, 100, 1)
            if r > 94:
                with open('./logging/sample_danmaku.txt', 'a') as f:
                    f.write('multi：'+str(event))

            print('multi_danmu:'+str(event))




    def gift_processor(self, event):
        cmd = event['cmd']
        match cmd:
            case 'SEND_GIFT': self.gift_processor_part_gift(event)
            case 'COMBO_SEND': pass
            case 'SUPER_CHAT_MESSAGE': self.gift_processor_part_SC(event)
            case 'GUARD_BUY': self.gift_processor_part_captain(event)

    def gift_processor_part_gift(self, event):
        if global_setting.settings.debug: print(f'[GIFT]{event}')

    def gift_processor_part_SC(self, event):
        SC_info = event['data']

        price = SC_info['price']

        message = SC_info['message']
        user_info = SC_info['user_info']
        nickname = user_info['uname']

        says = f'{nickname}发来价值{price}的醒目留言说：{message}'
        package = (2,says)
        self.to_thread_read.append(package)

    def gift_processor_part_captain(self, event):
        purchase_info = event['data']

        # captain_name = purchase_info['username']
        # price = purchase_info['price']
        # lvl_name = purchase_info['gift_name']
        # lvl = purchase_info['guard_level']
        # tag = 'CAPTAIN_BUY_3'
        # match lvl:
        #     case 3:
        #         tag = 'CAPTAIN_BUY_3'
        #     case 2:
        #         tag = 'CAPTAIN_BUY_2'
        #     case 1:
        #         tag = 'CAPTAIN_BUY_1'

        if global_setting.settings.debug: print(f'[CAPTAIN]{purchase_info}')


if __name__ == '__main__':
    pass
