import os

import iosetting as ios
import liveget as lg
import initial


def caseA():
    file_clearer('./files')
    if os.path.exists('ban_word.txt'):
        os.remove('ban_word.txt')
    initial.initial()


def file_clearer(path):
    if os.path.exists(path):
        archive = os.listdir(path)
        for file in archive:
            os.remove(path + f'/{file}')


def caseB():

    print('正在读取房间号...')
    rid = 34162
    with open('./files/settings.txt', mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip().split('=')
        if line[0] == 'rid':
            rid = int(line[1])

    print('正在初始化弹幕获取器...')
    x = lg.LiveInfoGet(rid=rid)

    print("正在启动阅读器...")
    if os.path.exists('reader.py'):
        os.startfile('reader.py')
    else:
        os.startfile('reader.exe')

    print("正在启动弹幕获取器...")
    x.living_on()


def caseC():
    while True:
        os.system('cls')
        print('|*===================================================================*|\n'
              '|*|                       DANMAKU   READER                          |*|\n'
              '|*|  main -> 查看                                        DEMO  1.3   |*|\n'
              '|*===================================================================*|\n'
              '|*|                                                                 |*|\n'
              '|*|      B(b).禁读词列表        S(s).设置文件                          |*|\n'
              '|*|                                                                 |*|\n'
              '|*|                                                                 |*|\n'
              '|*|      P(p).返回上一级                         E(e):退出             |*|\n'
              '|*|                                                                 |*|\n'
              '|*===================================================================*|'
              )
        print('>>>', end='')
        get = input()
        get = get.strip()
        label = get[0].upper()
        match label:
            case 'B': os.system('ban_word.txt')
            case 'S':
                cwd = os.getcwd()
                os.chdir(cwd+'/files')
                os.system('settings.txt')
                os.chdir(cwd)
            case 'P': return
            case 'E': exit()
            case _:
                print(f'{label}没有在列表中')


def settings():
    settings_dict = {
        'API_KEY': None,
        'SECRET_KEY': None,
        'cuid': None,
        'rid': None,
        'min_level': None
    }
    have = set()
    with open('./files/settings.txt', mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip().split('=')
        if line[0] in settings_dict:
            settings_dict[line[0]] = line[1]
    dict_key = settings_dict.keys()
    os.system('cls')
    while True:
        while True:
            print('\nS(s).保存并返回上一级\t\tP(p).不保存并返回上一级\n'
                  'E(e).保存并退出\t\tEnter.继续修改')
            label = input('>>>').strip().upper()
            if len(label) > 0:
                label = label[0]
            match label:
                case 'S':
                    settingsave(settings_dict)
                    return
                case 'P':
                    return
                case 'E':
                    settingsave(settings_dict)
                    exit()
                case '':
                    break
                case _:
                    pass
        os.system('cls')
        print("当前参数如下：")
        for key in dict_key:
            length = len(settings_dict[key])
            val = settings_dict[key]
            end = ''
            if length > 10:
                end = '...'
                val = val[0:10]
            print(f'{key}: {val}' + end)
        print("选择你要修改的值（输入首字母，如果相同则输入前两个字母，大小写不限）：\n")
        label = input('>>>').strip()
        llen = len(label)
        for i in dict_key:
            if label.upper() == i.upper()[0:llen]:
                print(f"{i}要修改为(输入E/e放弃修改)>>>", end='')
                modify = input().strip()
                if modify.upper() == 'E':
                    break
                settings_dict[i] = modify
                print(f'现在{i}为{modify}')
                break


def settingsave(dct):
    _keys = dct.keys()
    lines = []
    for i in _keys:
        line = f'{i}={dct[i]}\n'
        lines.append(line)
    with open('./files/settings.txt', mode='w', encoding='utf-8') as f:
        f.writelines(lines)
        print('保存完成，重启后生效')


def main():
    print('正在检测初始化...')
    initial.initial()
    while True:
        os.system('cls')
        print('|*===================================================================*|\n'
              '|*|                       DANMAKU   READER                          |*|\n'
              '|*|                                                     DEMO  1.3   |*|\n'
              '|*===================================================================*|\n'
              '|*|                                                                 |*|\n'
              '|*|      A(a).初始化         B(b).启动         C(c).查看               |*|\n'
              '|*|                                                                 |*|\n'
              '|*|                                                                 |*|\n'
              '|*|      S(s).设置                             E(e):退出             |*|\n'
              '|*|                                                                 |*|\n'
              '|*===================================================================*|')
        ios.print_set('Tips:如果你想直接修改文件，只需在c.查看中打开对应文件并直接修改，本程序中的所有改动会在重启后生效',
                      tag='CTRL')

        print('>>>', end='')
        get = input()
        get = get.strip()

        label = get[0].upper()
        match label:
            case 'A': caseA()
            case 'B': caseB()
            case 'C': caseC()
            case 'S': settings()
            case 'E': exit()
            case _:
                print(f'{label}没有在列表中')




if __name__ == '__main__':
    main()
