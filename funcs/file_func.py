import os

from bilibili_api.credential import Credential

import iosetting as ios


def file_clearer(path):
    if os.path.exists(path):
        archive = os.listdir(path)
        for file in archive:
            os.remove(path + f'/{file}')


class InitialParser:
    def __init__(self):
        self.initial = ios.JsonParser.load('./files/INITIAL')

        self.id = self.initial['id']
        self.pw = self.initial['pw']
        self.sessdate = self.initial['sessdata']
        self.bili_jct = self.initial['bili_jct']
        self.buvid3 = self.initial['buvid3']
        self.ac_time_value = self.initial['ac_time_value']

    def credential_consist(self, c: Credential):
        self.sessdate = c.sessdata
        self.bili_jct = c.bili_jct
        self.buvid3 = c.buvid3
        self.id = c.ac_time_value

    def update_credential(self):
        self.initial['sessdata'] = self.sessdate
        self.initial['bili_jct'] = self.bili_jct
        self.initial['buvid3'] = self.buvid3
        self.initial['ac_time_value'] = self.ac_time_value

    def update_account(self):
        self.initial['id'] = self.id
        self.initial['pw'] = self.pw

    def get_credential(self):

        return Credential(
            sessdata=self.sessdate, bili_jct=self.bili_jct, buvid3=self.buvid3, ac_time_value=self.ac_time_value
        )

    def update(self):
        self.update_account()
        self.update_credential()

    def dump(self):
        ios.JsonParser.dump('./files/INITIAL', self.initial, mode='w')

    def update_and_dump(self):
        self.update()
        self.dump()

