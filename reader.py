import time
from collections import deque

import global_setting
import re
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


        self.re_only_some_symbol = re.compile("[^?？.。,，（）()]").search
        # self.ui.append(f"<font color=cyan>本项目基于bilibili_api， 如有任何需要，请联系作者</font>"
        #                "<p></p>")

        self.player = global_setting.narrator

    def reader(self) -> None:
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
                            if self.re_only_some_symbol(c):
                                self.danmaku_queue.append(c)
                                self.danmaku_len += 1
                    else:
                        pass

                '''
                    当弹幕量大于60时会清空队列，而大于50时会自动删掉10个弹幕，所以弹幕队列的长度在绝大部分时间是必定大于50的，
                    暂停判断放在这里也是合理的
                '''
                if global_setting.read_pause:
                    self._queue.clear()
                    self.danmaku_queue.clear()
                    self.danmaku_len = 0


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
                time.sleep(3)

            if int(time.time()) % 100 == 0:
                self.danmaku_len = len(self.danmaku_queue)


    def popleft_n(self, n) -> None:
        for _ in range(n):
            self.danmaku_queue.popleft()
        self.danmaku_len = len(self.danmaku_queue)

if __name__ == '__main__':
    pass
