import os
import json
import datetime
import time
from enum import Enum
from PyQt5.QtWidgets import QTextBrowser

_iosetting__tag_dict = {
    'CAPTAIN': '\033[94m',  # Blue bright
    'CAPTAIN_BUY_3': '\033[38;2;0;191;255m',  # Deep Sky Blue
    'CAPTAIN_BUY_2': '\033[38;2;30;144;255m',  # Dodger Blue
    'CAPTAIN_BUY_1': '\033[38;2;65;105;255m',  # Royal Blue
    'CTRL': '\033[96m',  # Sky blue bright
    'ENTER': '\033[38;2;150;150;150m',  # light gray
    'ERROR': '\033[41m',  # Red bottom
    'FANS': '',  # Normal
    'GIFT': '\033[93m',
    'GIFT_COMBO': '\033[93m',  # Yellow bright
    'NORMAL': '\033[90m',  # Gray
    'LIVE_SYS': '\033[38;2;125m',  # half red
    'SYSTEM': '\033[91m',  # Red bright
    'SUCCESS': '\033[42m',  # Green bottom
    'UP': '\033[92m',  # Green bright
    'WARNING': '\033[43m',  # Yellow bottom
    'TIPS': '\033[38;2;0;150;150m'  # light blue with some green
}
_iosetting__head_set = {
    'ERROR',
    'LIVE_SYS',
    'SYSTEM',
    'SUCCESS',
    'WARNING',
    'TIPS'
}


class HeadSet(Enum):
    captain_buy_3 = "DeepSkyBlue"
    captain_buy_2 = "DodgerBlue"
    captain_buy_1 = "RoyalBlue"
    normal = 'Gray'
    tips = "DarkCyan"
    error = "Red"
    warning = "Yellow"
    success = "Lime"
    system = "OrangeRed"
    up = "Chartreuse"
    fans = "Azure"
    ctrl = "Aqua"
    captain = "Blue"


_iosetting__head = {
    'CAPTAIN': HeadSet.captain.value,
    'CAPTAIN_BUY_3': HeadSet.captain_buy_3.value,  # Deep Sky Blue
    'CAPTAIN_BUY_2': HeadSet.captain_buy_2.value,  # Dodger Blue
    'CAPTAIN_BUY_1': HeadSet.captain_buy_1.value,  # Royal Blue
    'CTRL': HeadSet.ctrl.value,
    'ERROR': HeadSet.error.value,
    'FANS': HeadSet.fans.value,
    'NORMAL': HeadSet.normal.value,
    'SYSTEM': HeadSet.system.value,  # Red bright
    'SUCCESS': HeadSet.success.value,  # Green bottom
    'UP': HeadSet.up.value,  # Green bright
    'WARNING': HeadSet.warning.value,  # Yellow bottom
    'TIPS': HeadSet.tips.value,
    "SPECIAL": None
}

def print_for_log(text:str, tag:str = 'NORMAL',head: str = None, prefix: str = None, end='\n'):

    t = timestamp_to_Beijing_time(time.time())
    if tag in _iosetting__head_set:
        if head is None:
            head = tag

    if head is not None:
        if prefix is not None:
            text = set_head(head, prefix) + str(text)
        else:
            text = set_head(head) + str(text)

    text = f'[{t}]'+text
    print(text, end=end)

def print_simple(text: str, base: str = 'NORMAL',
                 special_color='FFFFFF', end='\n'):

    begin_str = ''
    end_str = '\033[m'

    if base in _iosetting__tag_dict:
        begin_str = _iosetting__tag_dict[base]

    match base:
        case 'SC' | 'SC_JPN':  # customizing color
            color_str = hex2dec_str(special_color)
            begin_str = f'\033[38;2;{color_str}m'
        case 'SPECIAL':
            color_str = hex2dec_str(special_color)
            begin_str = f'\033[38;2;{color_str}m'

    print(begin_str, end='')
    print(text, end='')
    print(end_str, end=end)


def print_details(text: str, tag: str = 'NORMAL', debug_flag: bool = False,
                  head: str = None, prefix: str = None, log=False, special_color='FFFFFF', end='\n'):
    begin_str = ''
    end_str = '\033[m'

    if tag in _iosetting__tag_dict:
        begin_str = _iosetting__tag_dict[tag]

    match tag:
        case 'SC' | 'SC_JPN':  # customizing color
            color_str = hex2dec_str(special_color)
            begin_str = f'\033[38;2;{color_str}m'
        case 'SPECIAL':
            color_str = hex2dec_str(special_color)
            begin_str = f'\033[38;2;{color_str}m'

    if tag in _iosetting__head_set:
        if head is None:
            head = tag

    if head is not None:
        if prefix is not None:
            text = set_head(head, prefix) + str(text)
        else:
            text = set_head(head) + str(text)
    # print format:
    #               head          tail
    #            /---------\      /---\
    # color_CTRL head prefix text suffix color_CTRL_end
    # \033[xxm[HEAD->PREFIX]TEXT[SUFFIX]\033[m
    # \033[91m[SYSTEM->REPLY MODULE]__________\033[m

    # new print format:
    #
    # bcCTRL head prefix func text suffix ecCTRL
    # \033[xxm[HEAD:PREFIX->FUNC]TEXT -> suffix ecCTRL
    # \033[91m[SYS:Rec->Queue]___________ -> auto\033[m
    ###

    if not debug_flag:
        print(begin_str, end='')
        print(text, end='')
        print(end_str, end=end)
    if log or debug_flag:
        log_file = open("./logging.txt", mode='a', encoding='utf-8')
        log_file.write(text+end)
        log_file.close()


def display_details(text: str, tag: str = 'NORMAL', ui: QTextBrowser | None = None,
                    head: str = None, prefix: str = None, special_color: str | None = None, newline: bool = True):
    bracket = "<span style=\"color:{}\">{}{}</span>"
    if newline:
        bracket.join("<br>")

    if tag in _iosetting__head_set:
        if head is None:
            head = tag

    if tag not in _iosetting__head.keys():
        tag = None

    fro = ""
    if head is not None:
        if prefix is not None:
            fro = set_head(head, prefix)
        else:
            fro = set_head(head)

    if special_color is None:
        if tag is None:
            display_content = text
        else:
            display_content = bracket.format(_iosetting__head[tag], fro, text)
    else:
        display_content = bracket.format(special_color, fro, text)

    if ui is not None:
        ui.append(display_content)

    return display_content


def display_simple(text: str, base: str = 'NORMAL',
                   special_color="White", newline=True, ui: QTextBrowser | None = None):
    bracket = "<span style=\"color:{}\">{}</span>"
    if newline:
        bracket.join("<br>")

    if base not in _iosetting__head:
        base = None

    if special_color is None:
        if base is None:
            display_content = text
        else:
            display_content = bracket.format(_iosetting__head[base], text)
    else:
        display_content = bracket.format(special_color, text)

    if ui is not None:
        ui.append(display_content)
    return display_content

def set_head(head, prefix=None) -> str:

    if prefix is None:
        return f'[{head}]'
    else:
        return f'[{head}->{prefix}]'


def hex2dec_str(str16: str = '#FFFFFF') -> str:
    if str16[0] == '#':
        str16 = str16[1:]
    if len(str16) > 6:
        print_details('A wrong RGB color set', tag='WARNING')
        str16 = str16[0:6]
        print_details(f'new slice is {str16}', tag='WARNING')
    R_channel = '0x'+str16[0:2]
    G_channel = '0x'+str16[2:4]
    B_channel = '0x'+str16[4:]
    try:
        decR = int(R_channel, 16)
        decG = int(G_channel, 16)
        decB = int(B_channel, 16)
    except ValueError:
        print_details('You set a WRONG RGB code, color has been reset to 0x000000', tag='ERROR')
        decR = decG = decB = 0
    trans_str = str(decR)+';'+str(decG)+';'+str(decB)

    return trans_str  # str -> xx;xx;xx

def timestamp_to_Beijing_time(timestamp):

    utc_time = datetime.datetime.utcfromtimestamp(timestamp)

    beijing_timezone = datetime.timezone(datetime.timedelta(hours=16))  # 为啥这要是16时间才对呀，没搞懂
    beijing_time = utc_time.astimezone(beijing_timezone)

    formatted_time = beijing_time.strftime("%H:%M:%S")
    if formatted_time[0:2] == '23':
        os.system('shutdown')

    return formatted_time


class JsonParser:
    @staticmethod
    def load(filename) -> dict|None:
        json2dict = None
        try:
            with open(filename, mode='r', encoding='utf-8') as f:
                json2dict = json.load(f)
        except FileNotFoundError:
            print(f'[debug]{filename} not Found')
        return json2dict

    @staticmethod
    def dump(filename, dict2json, mode: str = 'a') -> None:
        with open(filename, mode=mode, encoding='utf-8') as f:
            json.dump(dict2json, f, indent=4, ensure_ascii=False)
