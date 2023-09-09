import time
from collections import deque
import iosetting as ios
import pyttsx3
import re
import multiprocessing


class Reader:

    def __init__(self, global_queue: multiprocessing.Queue):
        self.danmaku_queue = deque()
        self.danmaku_len = 0
        self.tmp = 0
        self._queue = global_queue

        self.__PREFIX = 'Reader'

        self.force_chasing_10 = 0  # 20
        self.force_chasing_20 = 0  # 15
        self.force_chasing_30 = 0  # 10
        self.force_chasing_40 = 0  # 5
        self.force_reset_limit = 50

        self.ban_word_set = set("1234567890")
        self.re_ban_str = ''
        self.ban_word_set_initial()
        self.re_only_some_symbol = re.compile("[^?？.。,，（）()]").search
        ios.print_details('本项目基于bilibili_api， 如有任何需要，请联系作者，与狐宝同在\n'
                          '\t\t\t------from a certain member of 保狐派', tag='CTRL')
        ios.print_details('本界面为debug界面，如果程序出现任何异常，请将本界面的错误信息发与作者', tag='TIPS')

        self.player = TxtProcess()

    def ban_word_set_initial(self):
        try:
            with open('ban_word.txt', mode='r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError('文件不存在')

        for line in lines:
            line = line.strip()
            if line[0] != '$':
                if line[0] == '-':
                    line = line[1:]
                    self.re_ban_str = self.re_ban_str + line + '|'
                else:
                    self.ban_word_set.add(line)

        self.re_ban_str = self.re_ban_str[:-1]
        if len(self.re_ban_str) == 0:
            self.re_ban_str = '$没有屏蔽词'
        ios.print_details(f'屏蔽词列表{str(self.ban_word_set)}', tag='UP')
        ios.print_details(f"屏蔽匹配词列表{self.re_ban_str.split('|')}", tag='UP')

    def reader(self):
        former = ''
        print('[read]wait initial')
        time.sleep(5)
        while True:

            if self.tmp > 50:
                self.tmp = 0

            # 队列加入与预处理机制
            if self.danmaku_len < 50:
                while not self._queue.empty():
                    c: str = self._queue.get()
                    c = c.strip()
                    re_flag = re.search(self.re_ban_str, c)

                    if re_flag is None:
                        if c not in self.ban_word_set:
                            if self.re_only_some_symbol(c):
                                self.danmaku_queue.append(c)
                                self.danmaku_len += 1
                                ios.print_details(c + ':加入了待读队列', tag='SPECIAL', head='QUEUE',
                                                  special_color='#50FF50')
                            else:
                                ios.print_details(f'检测到{c}中仅包含符号，拒绝加入队列')
                    else:
                        ios.print_details(f'屏蔽{c}由于其中含有{re_flag.group()}')

            # 追赶机制
            if self.danmaku_len > self.force_reset_limit:
                self.danmaku_queue.clear()
                self.danmaku_len = 0
                ios.print_details('达到最大队列额度，弹幕姬强制重置', tag='CTRL', head='SYSTEM', prefix='CHASING')
            elif self.danmaku_len > 40:
                self.tmp = 0
                self.popleft_n(4)
                self.force_chasing_40 += 1
                if self.force_chasing_40 > 5:
                    self.force_chasing_40 = 0
                    self.popleft_n(10)
                    ios.print_details('强制更新机制已减少10个弹幕', tag='CTRL', head='SYSTEM', prefix='CHASING')
                ios.print_details('队列已大于40，自动跳过80%弹幕', tag='SYSTEM', prefix='CHASING')
            elif self.danmaku_len > 30:
                self.tmp = 0
                self.popleft_n(3)
                self.force_chasing_30 += 1
                if self.force_chasing_30 > 10:
                    self.force_chasing_30 = 0
                    self.popleft_n(10)
                    ios.print_details('强制更新机制已减少10个弹幕', tag='CTRL', head='SYSTEM', prefix='CHASING')
                ios.print_details('队列已大于30，自动跳过75%弹幕', tag='SYSTEM', prefix='CHASING')
            elif self.danmaku_len > 20:
                self.tmp = 0
                self.popleft_n(2)
                self.force_chasing_20 += 1
                if self.force_chasing_20 > 15:
                    self.force_chasing_20 = 0
                    self.popleft_n(10)
                    ios.print_details('强制更新机制已减少10个弹幕', tag='CTRL', head='SYSTEM', prefix='CHASING')
                ios.print_details('队列已大于20，自动跳过66%弹幕', tag='SYSTEM', prefix='CHASING')
            elif self.danmaku_len > 10:
                self.tmp = 0
                self.popleft_n(1)
                self.force_chasing_10 += 1
                if self.force_chasing_10 > 20:
                    self.force_chasing_10 = 0
                    self.popleft_n(5)
                    ios.print_details('强制更新机制已减少5个弹幕', tag='CTRL', head='SYSTEM', prefix='CHASING')
                ios.print_details('队列已大于10，自动跳过50%弹幕', tag='SYSTEM', prefix='CHASING')
            elif self.danmaku_len > 5 and self.tmp % 3 == 0:
                self.tmp = 0
                self.popleft_n(1)
                ios.print_details('队列已大于5，自动跳过33%弹幕', tag='SYSTEM', prefix='CHASING')

            # 处理与读取机制
            if self.danmaku_len != 0:
                now = self.danmaku_queue.popleft()
                if now == former:
                    self.danmaku_len -= 1
                else:
                    ios.print_details(now + ' 准备读取', tag='SYSTEM')
                    self.player.txt2audio(now)
                    self.danmaku_len -= 1
                    former = now

            else:
                time.sleep(3)

            if int(time.time()) % 100 == 0:
                self.danmaku_len = len(self.danmaku_queue)
                ios.print_details('当前队列数量已同步', tag='SYSTEM')

    def popleft_n(self, n):
        for _ in range(n):
            self.danmaku_queue.popleft()
        self.danmaku_len = len(self.danmaku_queue)


class TxtProcess:

    def __init__(self):
        self.say_engin = pyttsx3.init()
        self.say_engin.setProperty('rate', 250)
        self.say_engin.setProperty('volume', 1)
        voices = self.say_engin.getProperty('voices')
        self.say_engin.setProperty('voice', voices[0].id)

    def txt2audio(self, message: str):
        self.say_engin.say(message)
        self.say_engin.runAndWait()
        self.say_engin.stop()


if __name__ == '__main__':
    pass
