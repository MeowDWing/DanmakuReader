import iosetting as ios
import os
import re
import main


def interface(proj_name: str, set_dict: dict, version: str, location: str, pflag: bool = False, eflag: bool = False):

    # 设置区
    items = len(set_dict.keys())
    line_int = int(items/3)
    line_rest = items % 3
    set_lines = []
    for key, value in set_dict.items():
        set_lines.append(f'{key.upper()}({key}).{value}')

    llen = len(set_lines)
    cpj_n = characters_num(proj_name)
    cver_n = characters_num(version)
    cloc_n = characters_num(location)

    # 显示区
    print(f"|*{'=' * 76}*|")
    print(f"|*|{proj_name.center(74-cpj_n)}|*|")
    print(f"|*|    {location.ljust(33-cloc_n)}{version.rjust(33-cver_n)}    |*|")
    print(f"|*{'=' * 76}*|")
    print(f"|*|{' ' * 74}|*|")

    tmp = 0
    if line_int != 0:
        for i in range(line_int):
            l1 = characters_num(set_lines[tmp])
            l2 = characters_num(set_lines[tmp+1])
            l3 = characters_num(set_lines[tmp+2])
            print(f"|*|        "
                  f"{set_lines[tmp].ljust(22-l1)}"
                  f"{set_lines[tmp+1].ljust(22-l2)}"
                  f"{set_lines[tmp+2].ljust(22-l3)}"
                  f"|*|")
            print(f"|*|{' ' * 74}|*|")
            tmp += 3
    if line_rest != 0:
        if line_rest == 1:
            print(f"|*|        {set_lines[tmp].ljust(66-characters_num(set_lines[tmp]))}|*|")
        else:
            ll2 = characters_num(set_lines[tmp])
            ll1 = characters_num(set_lines[tmp+1])
            print(f"|*|        "
                  f"{set_lines[tmp].ljust(22 - ll2)}"
                  f"{set_lines[tmp+1].ljust(44 - ll1)}"
                  f"|*|")
    print(f"|*|{' ' * 74}|*|")
    if eflag or pflag:
        print(f"|*|        {'P(p).上一级'.ljust(44-3)}{'E(e).退出'.ljust(22-2)}|*|")
        print(f"|*|{' ' * 74}|*|")

    print(f"|*{'=' * 76}*|")

    # print('|*===================================================================*|\n'
    #       '|*|                       DANMAKU   READER                          |*|\n'
    #       f'|*|  main -> 查看                                  {__VERSION__}   |*|\n'
    #       '|*===================================================================*|\n'
    #       '|*|                                                                 |*|\n'
    #       '|*|      B(b).禁读词列表        S(s).设置文件                          |*|\n'
    #       '|*|                                                                 |*|\n'
    #       '|*|                                                                 |*|\n'
    #       '|*|      P(p).返回上一级                         E(e):退出             |*|\n'
    #       '|*|                                                                 |*|\n'
    #       '|*===================================================================*|'
    #       )


def characters_num(rev: str) -> int:
    _m = re.findall("\\\\x[0-9a-f][0-9a-f]", str(rev.encode('utf-8')))
    _l = len(_m)
    return int(_l/3)


def update_content(version: str):
    with open(f'{version}.md', mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        ios.print_details(line, tag='CTRL')


if __name__ == '__main__':
    interface(
        proj_name='DanmakuReader',
        version=main.__VERSION__,
        set_dict={
            'a': '初始化',
            'b': '启动',
            'c': '查看',
            'd': '22',
            'e': '33'
        },
        location='查看',
        eflag=True,
        pflag=True
    )

