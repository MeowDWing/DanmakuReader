import os

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

        self.force_chasing_10 = 0  # 20
        self.force_chasing_20 = 0  # 15
        self.force_chasing_30 = 0  # 10
        self.force_chasing_40 = 0  # 5
        self.force_reset_limit = 50

        self.audio_path = './audio/'

        player.initial()
        self.ban_word_set = set("1234567890")
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

            if self.danmaku_len < 50:
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

            if self.danmaku_len > self.force_reset_limit:
                self.danmaku_queue.clear()
                self.danmaku_len = 0
                ios.print_set('达到最大队列额度，弹幕姬强制重置', tag='CTRL', head='SYSTEM', prefix='CHASING')
            elif self.danmaku_len > 40:
                self.tmp = 0
                self.popleft_n(4)
                self.force_chasing_40 += 1
                if self.force_chasing_40 > 5:
                    self.popleft_n(10)
                    ios.print_set('强制更新机制已减少10个弹幕', tag='CTRL', head='SYSTEM', prefix='CHASING')
                ios.print_set('队列已大于40，自动跳过80%弹幕', tag='SYSTEM', prefix='CHASING')
            elif self.danmaku_len > 30:
                self.tmp = 0
                self.popleft_n(3)
                self.force_chasing_30 += 1
                if self.force_chasing_30 > 10:
                    self.popleft_n(10)
                    ios.print_set('强制更新机制已减少10个弹幕', tag='CTRL', head='SYSTEM', prefix='CHASING')
                ios.print_set('队列已大于30，自动跳过75%弹幕', tag='SYSTEM', prefix='CHASING')
            elif self.danmaku_len > 20:
                self.tmp = 0
                self.popleft_n(2)
                self.force_chasing_20 += 1
                if self.force_chasing_20 > 15:
                    self.popleft_n(10)
                    ios.print_set('强制更新机制已减少10个弹幕', tag='CTRL', head='SYSTEM', prefix='CHASING')
                ios.print_set('队列已大于20，自动跳过66%弹幕', tag='SYSTEM', prefix='CHASING')
            elif self.danmaku_len > 10:
                self.tmp = 0
                self.popleft_n(1)
                self.force_chasing_10 += 1
                if self.force_chasing_10 > 20:
                    self.popleft_n(5)
                    ios.print_set('强制更新机制已减少5个弹幕', tag='CTRL', head='SYSTEM', prefix='CHASING')
                ios.print_set('队列已大于10，自动跳过50%弹幕', tag='SYSTEM', prefix='CHASING')
            elif self.danmaku_len > 5 and self.tmp % 3 == 0:
                self.tmp = 0
                self.popleft_n(1)
                ios.print_set('队列已大于10，自动跳过33%弹幕', tag='SYSTEM', prefix='CHASING')

            if self.danmaku_len != 0:
                now = self.danmaku_queue.popleft()
                if now == former or now in self.ban_word_set:
                    self.danmaku_len -= 1
                else:
                    ios.print_set(now+' 准备读取', tag='SYSTEM')
                    now_hash, content, payload, if_have = self.player.txt2audio(now)
                    if if_have:
                        audio_path = './audiosave/'
                    else:
                        audio_path = self.audio_path
                    self.danmaku_len -= 1
                    former = now

                    try:
                        player.play(audio_path+now_hash+'.mp3')
                        self.tmp += 1
                    except pygame.error:
                        ios.print_set('读取失败，失败资料如下', tag='ERROR')
                        ios.print_set(now, tag='ERROR')
                        ios.print_set(content, tag='ERROR')
                        ios.print_set(payload, tag='ERROR')
                        ios.print_set('如过反复出现此错误，请联系作者并发送上述信息', tag='SYSTEM')
                    if not if_have:
                        player.delete('./audio/'+now_hash+'.mp3')
            else:
                time.sleep(3)

            if int(time.time()) % 100 == 0:
                self.danmaku_len = len(self.danmaku_queue)
                ios.print_set('当前队列数量已同步', tag='SYSTEM')

    def popleft_n(self, n):
        for _ in range(n):
            self.danmaku_queue.popleft()
        self.danmaku_len = len(self.danmaku_queue)


class txtprocess:

    def __init__(self):
        self.API_KEY = None
        self.SECRET_KEY = None
        self.cuid = None
        self.audio_saver = AudioTempSave()
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
        hashm = hash(message)
        if_join = False

        if len(message) < 4:
            if_join = True

        if hashm in self.audio_saver:
            return hashm, message, None, True
        else:
            hashm, content, payload = self._txt2audio(message, if_join)
            return hashm, content, payload, False

    def _txt2audio(self, message, if_join):

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
            if if_join:
                with open('./audiosave/'+f'{hashm}.mp3', mode='wb') as f:
                    f.write(response.content)
                    self.audio_saver.audio_set.add(hashm)
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


class AudioTempSave:

    def __init__(self):
        self.audio_set = set()
        self.hash_set_initial()

    def hash_set_initial(self):
        audio_list = os.listdir('./audiosave')

        for audio_name in audio_list:
            audio_name = audio_name.strip().split('.')[0]
            self.audio_set.add(audio_name)






def main():
    read = Reader()
    read.reader()


if __name__ == '__main__':
    main()
