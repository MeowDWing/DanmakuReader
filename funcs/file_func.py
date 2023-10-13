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


class SettingsParser:
    """ settings 文件解释器 """
    def __init__(self):
        self.settings = ios.JsonParser.load('./files/settings.txt')

        self.basic = self.settings['basic_setting']
        self.rid = self.basic['rid']
        self.min_lvl = self.basic['min_level']

        self.sys = self.settings['sys_setting']
        self.login = self.sys['login']
        self.save_account = self.sys['save_account']
        self.debug = self.sys['debug']

    def to_update(self, basic_dict=None, sys_dict=None):
        if basic_dict is not None:
            self.delete_key_is_null(basic_dict)
            self.basic.update(basic_dict)

        if sys_dict is not None:
            self.delete_key_is_null(sys_dict)
            self.sys.update(sys_dict)

    def to_conform(self):
        self.basic = self.settings['basic_setting']
        self.rid = self.basic['rid']
        self.min_lvl = self.basic['min_level']

        self.sys = self.settings['sys_setting']
        self.login = self.sys['login']
        self.save_account = self.sys['save_account']
        self.debug = self.sys['debug']

    def dump(self):
        d = {
            'basic_setting': self.basic,
            'sys_setting': self.sys
        }
        self.settings.update(d)
        ios.JsonParser.dump('./files/settings.txt', self.settings, mode='w')

    def update_conform_and_dump(self, basic_dict=None, sys_dict=None):
        self.to_update(basic_dict=basic_dict, sys_dict=sys_dict)
        self.to_conform()
        self.dump()

    @staticmethod
    def basic_settings_dict_constructor(rid: str|int|None = None, min_lvl: str|int|None = None):
        """

        :param rid:
        :param min_lvl:
        :return:
        """
        return {
            'rid': int(rid),
            'min_level': int(min_lvl),
        }

    @staticmethod
    def sys_settings_dict_constructor(login: bool|None = None, save_account: bool|None = None, debug: bool|None = None):
        """

        :param login:
        :param save_account:
        :param debug:
        :return:
        """
        return {
            'login': login,
            'save_account': save_account,
            'debug': debug,
        }

    @staticmethod
    def delete_key_is_null(d: dict):
        """

        :param d:
        :return:
        """
        for key in d:
            if d[key] is None:
                d.pop(key)