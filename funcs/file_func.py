import os

from bilibili_api.credential import Credential

import iosetting as ios


def file_clearer(path) -> None:
    if os.path.exists(path):
        archive = os.listdir(path)
        for file in archive:
            os.remove(path + f'/{file}')


class InitialParser:
    """ INITIAL文件解释器 """
    def __init__(self):
        self.initial = ios.JsonParser.load('./files/INITIAL')

        self.id = self.initial['id']
        self.pw = self.initial['pw']
        self.sessdate = self.initial['sessdata']
        self.bili_jct = self.initial['bili_jct']
        self.buvid3 = self.initial['buvid3']
        self.ac_time_value = self.initial['ac_time_value']

    def credential_consist(self, c: Credential) -> None:
        """
            将证书同步到initial解释器实例中
        :param c: Credential类
        :return:
        """
        self.sessdate = c.sessdata
        self.bili_jct = c.bili_jct
        self.buvid3 = c.buvid3
        self.ac_time_value = c.ac_time_value

    def update_credential(self) -> None:
        """
            将证书信息更新到临时字典中
        :return:
        """
        self.initial['sessdata'] = self.sessdate
        self.initial['bili_jct'] = self.bili_jct
        self.initial['buvid3'] = self.buvid3
        self.initial['ac_time_value'] = self.ac_time_value

    def update_account(self) -> None:
        """
            将账号密码信息更新到临时字典中
        :return:
        """
        self.initial['id'] = self.id
        self.initial['pw'] = self.pw

    def get_credential(self):
        """
            从解释器类信息获取证书类
        :return:
        """
        return Credential(
            sessdata=self.sessdate, bili_jct=self.bili_jct, buvid3=self.buvid3, ac_time_value=self.ac_time_value
        )

    def update(self) -> None:
        """
            将证书与登录信息一起更新到临时字典中
        :return:
        """
        self.update_account()
        self.update_credential()

    def dump(self) -> None:
        """
            将临时字典上传至本地文件保存，供下次使用
        :return:
        """
        ios.JsonParser.dump('./files/INITIAL', self.initial, mode='w')

    def update_and_dump(self) -> None:
        """
            将实例信息更新并上传至本地文件
        :return:
        """
        self.update()
        self.dump()

