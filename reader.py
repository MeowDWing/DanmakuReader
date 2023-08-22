import requests
import pygame
import audioplay as player
import time
from collections import deque
import iosetting as ios
from urllib.parse import urlencode


class Reader:

    def __init__(self):
        self.danmaku_queue = deque()
        self.danmaku_len = 0
        self.tmp = 0
        player.initial()
        self.ban_word_set = set()
        self.ban_word_set_initial()
        ios.print_set('本项目基于bilibili_api， 如有任何需要，请联系作者，与狐宝同在\n'
                      '\t\t\t------from a certain member of 保狐派', tag='CTRL')

        self.player = txtprocess()

    def ban_word_set_initial(self):
        try:
            with open('ban_word.txt', mode='r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError('文件不存在')

        for line in lines:
            line = line.strip()
            if line[0] != '$':
                self.ban_word_set.add(line)
        ios.print_set(f'屏蔽词列表{str(self.ban_word_set)}', tag='UP')

    def reader(self):
        former = ''
        print('[read]wait initial')
        time.sleep(5)
        with open('./files/danmaku.txt', mode='w', encoding='utf-8'):
            pass
        while True:
            if self.tmp > 50:
                self.tmp = 0

            if self.danmaku_len < 60:
                with open('./files/danmaku.txt', mode='r', encoding='utf-8') as f:
                    lines = f.readlines()
                with open('./files/danmaku.txt', mode='w', encoding='utf-8'):
                    pass
                if len(lines) != 0:
                    for line in lines:
                        line = line.strip()
                        self.danmaku_queue.append(line)
                        self.danmaku_len += 1
                        ios.print_set(line+':加入了待读队列', tag='SPECIAL', head='QUEUE', special_color='#50FF50')

            if self.danmaku_len > 50:
                self.tmp = 0
                self.danmaku_queue.popleft()
                self.danmaku_queue.popleft()
                self.danmaku_queue.popleft()
                self.danmaku_queue.popleft()
                self.danmaku_len -= 4
                ios.print_set('队列已大于50，自动跳过80%弹幕', tag='SYSTEM', prefix='CHASING')
            elif self.danmaku_len > 40:
                self.tmp = 0
                self.danmaku_queue.popleft()
                self.danmaku_queue.popleft()
                self.danmaku_queue.popleft()
                self.danmaku_len -= 3
                ios.print_set('队列已大于40，自动跳过75%弹幕', tag='SYSTEM', prefix='CHASING')
            elif self.danmaku_len > 20:
                self.tmp = 0
                self.danmaku_queue.popleft()
                self.danmaku_len -= 1
                ios.print_set('队列已大于20，自动跳过50%弹幕', tag='SYSTEM', prefix='CHASING')
            elif self.danmaku_len > 10 and self.tmp % 4 == 0:
                self.danmaku_queue.popleft()
                self.danmaku_len -= 1
                ios.print_set('队列已大于10，自动跳过20%弹幕', tag='SYSTEM', prefix='CHASING')

            if self.danmaku_len != 0:
                now = self.danmaku_queue.popleft()
                if now == former or now in self.ban_word_set:
                    self.danmaku_len -= 1
                else:
                    ios.print_set(now+' 准备读取', tag='SYSTEM')
                    now_hash, content, payload = self.player.txt2audio(now)
                    self.danmaku_len -= 1
                    former = now

                    try:
                        player.play('./audio/'+now_hash+'.mp3')
                        self.tmp += 1
                    except pygame.error:
                        ios.print_set('读取失败，失败资料如下', tag='ERROR')
                        ios.print_set(now, tag='ERROR')
                        ios.print_set(content, tag='ERROR')
                        ios.print_set(payload, tag='ERROR')
                        ios.print_set('如过反复出现此错误，请联系作者并发送上述信息', tag='SYSTEM')

                    player.delete('./audio/'+now_hash+'.mp3')
            else:
                time.sleep(3)

            if int(time.time()) % 100 == 0:
                self.danmaku_len = len(self.danmaku_queue)
                ios.print_set('当前队列数量已同步', tag='SYSTEM')


class txtprocess:

    def __init__(self):
        self.API_KEY = None
        self.SECRET_KEY = None
        self.cuid = None
        with open('./files/settings.txt', mode='r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().split('=')
                if line[0] == 'API_KEY':
                    self.API_KEY = line[1]
                elif line[0] == 'SECRET_KEY':
                    self.SECRET_KEY = line[1]
                elif line[0] == 'cuid':
                    self.cuid = line[1]

    def txt2audio(self, message):

        url = "https://tsn.baidu.com/text2audio"
        tok = self.get_access_token()
        payload_dict = {
            'tex': message,
            'lan': 'zh',
            'cuid': self.cuid,
            'ctp': '1',
            'spd': '11',
            'pit': '7',
            'vol': '5',
            'per': '0',
            'aue': '3',
            'tok': tok
        }
        payload = urlencode(payload_dict)

        # payload = 'tex='+f'{message}'+'&lan=zh&cuid=PhVV06OsEfgN63VbSL0xIkM8OZFZQ5Rg&ctp=1&spd=11&pit=7&vol=5&per=0&aue=3'
        #                               '&tok=' + self.get_access_token()

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*'
        }
        hashm = hash(message)

        response = requests.request("POST", url, headers=headers, data=payload)

        # print(response.text)
        if type(response.content) == 'dict':
            ios.print_set(f'{message} may trans to audio unsuccessfully')
            return 'bad'
        else:
            with open('./audio/'+f'{hashm}'+'.mp3', mode='wb') as f:
                f.write(response.content)

        return str(hashm), response.content, payload

    def get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.API_KEY, "client_secret": self.SECRET_KEY}
        return str(requests.post(url, params=params).json().get("access_token"))


def main():
    read = Reader()
    read.reader()


if __name__ == '__main__':
    main()
