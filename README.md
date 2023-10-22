
<div align="center">

# Danmaku Reader
[![LICENSE](https://img.shields.io/badge/LICENSE-GPLv3+-red)][LICENSE]
[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org)
[![基于](https://img.shields.io/badge/基于-bilibili_api_python-green)][base]

**:warning: 注意：python版经过作者更详细的测试，会更加稳定; release版是pyinstaller打包完成的，只测试了可运行性**

</div>

--------

# 项目简介

本项目源于作者学习python的过程中，发展于b站策略更新导致的部分弹幕姬失效，并将在之后适配尽可能多的直播场景

## 历次更新的内容变迁
- 自动追赶机制：帮助你直击最新弹幕（PUSH4 发布后）
- 绝对的排外政策：可调节读取所需要的牌子等级（默认1级）
- 极端的亲外决议：当读取所需等级设为0时，会读取所有弹幕（只要他能读出来）（PUSH8发布后）
- 没有阀门制度：跳过弹幕时不看等级，一视同仁（PUSH5 发布后）
- 预设屏蔽词：符合狐宝直播需要，包含 。/ 赞 和所有个位数字（PUSH5 发布后）
- 当消息仅包含中英文常用符号时，拒绝加入消息队列（PUSH5发布后）
- 正则表达式匹配屏蔽词（PUSH7 发布后）
- 登录账号/手动输入cookie (PUSH9发布后)
- GUI界面（alpha版本发布后）

## 使用方法：（需要登录b站账号，请仔细阅读登录界面说明）

- 非打包方案
  - 通过要求文件安装必要支持`pip install -r requirements.txt`
  - 用3.9以上版本运行DanmakuReader.py

- release方案
  - 个人打包
    - 本项目给出了项目打包文件DanmakuReader.spec，只需安装`pip install pyinstaller`，并通过
      `pyinstaller DanmakuReader.spec`即可打包项目文件，打包好的程序位于 `./dist`文件夹中
  - release方案
    - 可以通过百度网盘
      > https://pan.baidu.com/s/1Xfv6NSY8QTdNOpDL7I-OBw?pwd=11my
    - 或者在GitHub页面获得最新包（GitHub一般会慢一点）


## 文件说明
- /files - 各类文件储存位置，第一次打开项目后自动创建
  * ban_words - 屏蔽词文件，json格式
  * settings - 非敏感设置信息文件，明文，json格式
  * INITIAL - 敏感信息文件（保存登录的cookie及账号密码），明文，json格式
- /logging - 日志文件夹，当前仍未正式使用

## 机制说明
* 弹幕追赶机制
  * 机制保证在队列有50个以上词时，清空队列
  * 机制保证在队列有40个以上词时，每5个词只读1个词，并在保持40个以上词5次读取后清理10个词
  * 机制保证在队列有30个以上词时，每4个词只读1个词，并在保持30个以上词10次读取后清理10个词
  * 机制保证在队列有20个以上词时，每3个词只读1个词，并在保持20个以上词15次读取后清理10个词
  * 机制保证在队列有10个以上词时，每2个词只读1个词，并在保持10个以上词20次读取后清理5个词
  * 机制保证在队列有5个以上词时，每3个词只读2个词。


## 其他说明（Q&A）

* Q:为什么没有做重置弹幕机制？
  * A:已经有弹幕追赶机制了，不用重置也会一直保持在最新弹幕（追赶机制可以完全保证在大多数时间内在读最新弹幕）


* Q:我该怎么知道这些机制都正常运行了？
  * A:在reader界面，每个机制的每次运行都会发送运行消息，该界面是重要的调试界面，如果你无意调试，可以无视这个界面的输出。


* Q:我该怎么帮助狐宝或者作者？
  * A:你可以访问本项目的github页面提issue或者在b站联系：吾名喵喵之翼。作者只要闲着看到就会回复你（大概会在每天的23点后）
  * 仓库地址：https://github.com/MeowDWing/DanmakuReader


------

## 更新计划

+ alpha 1.1： 完善设置及其他内容，修复bug（预计10月底）
+ alpha 1.2+ ： 日志方案等（预计11月底）
+ beta+ ： 更好的GUI界面（预计2024年中上）

[license]: https://github.com/MeowDWing/DanmakuReader/blob/main/LICENSE
[base]: https://github.com/Nemo2011/bilibili-api