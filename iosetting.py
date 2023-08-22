_iosetting__tag_dict = {
    'CAPTAIN': '\033[94m',  # Blue bright
    'CAPTAIN_BUY_3': '\033[38;2;0;191;255m',  # Deep Sky Blue
    'CAPTAIN_BUY_2': '\033[38;2;30;144;255m',  # Doder Blue
    'CAPTAIN_BUY_1': '\033[38;2;65;105;255m',  # Royal Blue
    'CTRL': '\033[96m',  # Sky blue bright
    'ENTER': '\033[38;2;150;150;150m',  # light gray
    'ERROR': '\033[41m[ERROR]',  # Red bottom
    'FANS': '',  # Normal
    'GIFT': '\033[93m',
    'GIFT_COMBO': '\033[93m',  # Yellow bright
    'NORMAL': '\033[90m',  # Gray
    'LIVE_SYS': '\033[38;2;125m',  # half red
    'SYSTEM': '\033[91m',  # Red bright
    'SUCCESS': '\033[42m[SUCCESS]',  # Green bottom
    'UP': '\033[92m',  # Green bright
    'WARNING': '\033[43m[WARNING]',  # Yellow bottom
}
_iosetting__head_set = {
    'ERROR',
    'LIVE_SYS',
    'SYSTEM',
    'SUCCESS',
    'WARNING',
}


def print_set(text: str, tag: str = 'NORMAL', debug_flag: bool = False,
              head: str = None, prefix: str = None, log=False, special_color='FFFFFF', end='\n'):
    begin_str = ''
    end_str = '\033[0m'

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
    # \033[91m[SYSTEM->REPLY MODULE]xxxxxxxxx\033[m

    print(begin_str, end='')
    print(text, end='')
    print(end_str, end=end)
    if log:
        log_file = open("./logging.txt", mode='a', encoding='utf-8')
        log_file.write(text+end)
        log_file.close()


def set_head(head, prefix=None):
    if prefix is None:
        return f'[{head}]'
    else:
        return f'[{head}->{prefix}]'


def hex2dec_str(str16: str = '#FFFFFF') -> str:
    if str16[0] == '#':
        str16 = str16[1:]
    if len(str16) > 6:
        print_set('A wrong RGB color set', tag='WARNING')
        str16 = str16[0:6]
        print_set(f'new slice is {str16}', tag='WARNING')
    R_channel = '0x'+str16[0:2]
    G_channel = '0x'+str16[2:4]
    B_channel = '0x'+str16[4:]
    try:
        decR = int(R_channel, 16)
        decG = int(G_channel, 16)
        decB = int(B_channel, 16)
    except ValueError:
        print_set('You set a WRONG RGB code, color has been reset to 0x000000', tag='ERROR')
        decR = decG = decB = 0
    trans_str = str(decR)+';'+str(decG)+';'+str(decB)
    return trans_str  # str -> xx;xx;xx



