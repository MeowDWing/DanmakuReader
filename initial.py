import os


def initial():
    try:
        with open('./files/INITIAL', mode='r'):
            pass
    except FileNotFoundError:
        _initial()


def _initial():
    if not os.path.exists('./files'):
        os.mkdir('./files')

    if not os.path.exists('./audio'):
        os.mkdir('./audio')

    with open('./files/INITIAL', mode='x'):
        pass

    try:
        with open('ban_word.txt', mode='r'):
            pass
    except FileNotFoundError:
        with open('ban_word.txt', mode='w', encoding='utf-8') as f:
            f.write('$在该文件下写入的所有词会被屏蔽,每行只写一个词,只屏蔽完全一致的弹幕\n'
                    '$本文件中$（美元）符号开头的句子会被视为注释\n'
                    '$更改屏蔽词需要重启应用\n'
                    '。\n'
                    '赞\n'
                    )

    try:
        with open('./files/settings.txt', mode='r'):
            pass
    except FileNotFoundError:
        settings_initial()


def settings_initial():
    lines = [
        'API_KEY=\n',
        'SECRET_KEY=\n',
        'rid=34162\n',
    ]

    with open('./files/settings.txt', mode='w', encoding='utf-8') as f:
        f.writelines(lines)
