import time
from collections import deque

import global_setting
import iosetting as ios
import re
from ui import launchwindow


class Reader:

    def __init__(self, global_queue: deque,
                 ui: launchwindow.Ui_Launch):
        self.danmaku_queue = deque()
        self.danmaku_len = 0
        self.tmp = 0
        self._queue = global_queue
        self.ui = ui.readtext

        self.__PREFIX = 'Reader'

        self.force_chasing_10 = 0  # 20
        self.force_chasing_20 = 0  # 15
        self.force_chasing_30 = 0  # 10
        self.force_chasing_40 = 0  # 5
        self.force_reset_limit = 50

        ban_word_set, self.re_ban_str = global_setting.ban_word.ban_list_creator()
        self.ban_word_set = set("1234567890")
        self.ban_word_set.update(ban_word_set)
        ios.display_details(f'屏蔽词列表{str(self.ban_word_set)}', tag='UP', ui=self.ui)
        ios.display_details(f"屏蔽匹配词列表{self.re_ban_str.split('|')}", tag='UP', ui=self.ui)


        self.re_only_some_symbol = re.compile("[^?？.。,，（）()]").search
        self.ui.append(f"<font color=cyan>本项目基于bilibili_api， 如有任何需要，请联系作者</font>"
                       "<p></p>")
        # ios.print_details('本项目基于bilibili_api， 如有任何需要，请联系作者，与狐宝同在\n'
        #                   '\t\t\t------from a certain member of 保狐派', tag='CTRL')
        # ios.print_details('本界面为debug界面，如果程序出现任何异常，请将本界面的错误信息发与作者', tag='TIPS')

        self.player = global_setting.narrator

    def reader(self) -> None:
        former = ''
        time.sleep(5)
        while True:

            if self.tmp > 50:
                self.tmp = 0

            # 队列加入与预处理机制
            if self.danmaku_len < 50:
                if not global_setting.thread_locked:
                    global_setting.thread_locked = True

                    while len(self._queue) > 0:
                        global_setting.thread_locked = True
                        c: str = self._queue.popleft()
                        c = c.strip()
                        re_flag = re.search(self.re_ban_str, c)

                        if re_flag is None:
                            if c not in self.ban_word_set:
                                if self.re_only_some_symbol(c):
                                    self.danmaku_queue.append(c)
                                    self.danmaku_len += 1
                                    ios.display_details(f'{c}:加入了待读队列', tag='SPECIAL', head='QUEUE',
                                                        special_color=ios.HeadSet.system.value, ui=self.ui)
                        else:
                            ios.display_details(f'屏蔽{c}由于其中含有{re_flag.group()}', special_color="Gray", ui=self.ui)

                    if global_setting.read_pause:
                        self._queue.clear()
                        self.danmaku_queue.clear()
                        self.danmaku_len = 0

                    global_setting.thread_locked = False

            # 追赶机制
            if self.danmaku_len > self.force_reset_limit:
                self.danmaku_queue.clear()
                self.danmaku_len = 0
                ios.display_details('达到最大队列额度，弹幕姬强制重置', tag='CTRL', head='SYSTEM', prefix='CHASING', ui=self.ui)

            elif self.danmaku_len > 40:
                self.tmp = 0
                self.popleft_n(4)
                self.force_chasing_40 += 1
                if self.force_chasing_40 > 5:
                    self.force_chasing_40 = 0
                    self.popleft_n(10)
                    ios.display_details('强制更新机制已减少10个弹幕', tag='CTRL', head='SYSTEM', prefix='CHASING', ui=self.ui)
                ios.display_details('队列已大于40，自动跳过80%弹幕', tag='SYSTEM', prefix='CHASING', ui=self.ui)
            elif self.danmaku_len > 30:
                self.tmp = 0
                self.popleft_n(3)
                self.force_chasing_30 += 1
                if self.force_chasing_30 > 10:
                    self.force_chasing_30 = 0
                    self.popleft_n(10)
                    ios.display_details('强制更新机制已减少10个弹幕', tag='CTRL', head='SYSTEM', prefix='CHASING', ui=self.ui)
                ios.display_details('队列已大于30，自动跳过75%弹幕', tag='SYSTEM', prefix='CHASING', ui=self.ui)
            elif self.danmaku_len > 20:
                self.tmp = 0
                self.popleft_n(2)
                self.force_chasing_20 += 1
                if self.force_chasing_20 > 15:
                    self.force_chasing_20 = 0
                    self.popleft_n(10)
                    ios.display_details('强制更新机制已减少10个弹幕', tag='CTRL', head='SYSTEM', prefix='CHASING', ui=self.ui)
                ios.display_details('队列已大于20，自动跳过66%弹幕', tag='SYSTEM', prefix='CHASING', ui=self.ui)
            elif self.danmaku_len > 10:
                self.tmp = 0
                self.popleft_n(1)
                self.force_chasing_10 += 1
                if self.force_chasing_10 > 20:
                    self.force_chasing_10 = 0
                    self.popleft_n(5)
                    ios.display_details('强制更新机制已减少5个弹幕', tag='CTRL', head='SYSTEM', prefix='CHASING', ui=self.ui)

                ios.display_details('队列已大于10，自动跳过50%弹幕', tag='SYSTEM', prefix='CHASING', ui=self.ui)
            elif self.danmaku_len > 5 and self.tmp % 3 == 0:
                self.tmp = 0
                self.popleft_n(1)
                ios.display_details('队列已大于5，自动跳过33%弹幕', tag='SYSTEM', prefix='CHASING', ui=self.ui)

            # 处理与读取机制
            if self.danmaku_len != 0:
                now = self.danmaku_queue.popleft()
                if now == former:
                    self.danmaku_len -= 1
                else:
                    ios.display_details(f"{now} 准备读取", tag="SYSTEM", ui=self.ui)
                    self.player.txt2audio(now)
                    self.danmaku_len -= 1
                    former = now

            else:
                time.sleep(3)

            if int(time.time()) % 100 == 0:
                self.danmaku_len = len(self.danmaku_queue)
                ios.display_details("当前队列已同步", tag="SYSTEM", ui=self.ui)

    def popleft_n(self, n) -> None:
        for _ in range(n):
            self.danmaku_queue.popleft()
        self.danmaku_len = len(self.danmaku_queue)

if __name__ == '__main__':
    pass
